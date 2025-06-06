import requests
from django.conf import settings


class TaigaAPIClient:
    # Base URL for Taiga API, stripped of trailing slash for consistency
    BASE_URL = settings.TAIGA_URL.rstrip("/")

    def __init__(self, username=None, password=None, project_slug=None):
        """
        Initialize the Taiga API client with authentication credentials and project slug.
        Defaults are taken from Django settings if not provided.

        Args:
            username (str, optional): Taiga username for authentication.
            password (str, optional): Taiga password for authentication.
            project_slug (str, optional): Project identifier slug in Taiga.
        """
        self.username = username or settings.TAIGA_USERNAME
        self.password = password or settings.TAIGA_PASSWORD
        self.project_slug = project_slug or settings.TAIGA_PROJECT_SLUG
        self._auth_token = None  # Cache for auth token
        self._project_id = None  # Cache for project ID

    def _get_headers(self):
        """
        Prepare HTTP headers including the Authorization token for API requests.

        Returns:
            dict: Headers including Bearer token and content-type.
        """
        return {
            "Authorization": f"Bearer {self.get_token()}",
            "Content-Type": "application/json",
        }

    def get_token(self):
        """
        Retrieve and cache the authentication token.
        If already cached, return the cached token.

        Returns:
            str: Authentication token (JWT).
        """
        if self._auth_token:
            return self._auth_token

        response = requests.post(
            f"{self.BASE_URL}/auth",
            json={
                "type": "normal",
                "username": self.username,
                "password": self.password,
            },
        )
        response.raise_for_status()  # Raise exception for HTTP errors
        self._auth_token = response.json().get("auth_token")
        return self._auth_token

    def get_project_id(self):
        """
        Retrieve and cache the project ID by querying the project slug.
        If cached, return the cached project ID.

        Returns:
            int: Project ID for the configured project slug.
        """
        if self._project_id:
            return self._project_id

        response = requests.get(
            f"{self.BASE_URL}/projects/by_slug?slug={self.project_slug}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        self._project_id = response.json()["id"]
        return self._project_id

    def task_exists(self, title: str) -> bool:
        """
        Check if a task with the given title already exists in the project backlog.

        Args:
            title (str): Task title to check for existence.

        Returns:
            bool: True if task exists, False otherwise.
        """
        project_id = self.get_project_id()
        response = requests.get(
            f"{self.BASE_URL}/userstories?project={project_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        existing_titles = [story["subject"].lower() for story in response.json()]
        return title.lower() in existing_titles

    def create_task(self, title: str, description: str, priority: int = 3):
        """
        Create a new task (user story) in Taiga with given title, description, and priority.

        Args:
            title (str): Task title.
            description (str): Detailed description of the task.
            priority (int, optional): Priority of the task (default is 3).

        Returns:
            dict: JSON response representing the created task.
        """
        payload = {
            "project": self.get_project_id(),
            "subject": title,
            "description": description,
            "priority": priority,
        }

        response = requests.post(
            f"{self.BASE_URL}/userstories", json=payload, headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
