import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class Copilot:
    def __init__(self, model: str = None, base_url: str = None):
        """
        Initialize Copilot with optional model name and Ollama API base URL.
        Defaults are taken from Django settings.
        """
        self.model = model or settings.OLLAMA_MODEL
        self.base_url = base_url or f"{settings.OLLAMA_URL}/api/generate"

    def extract_task_title(self, message: str, timeout: int = 15) -> str | None:
        """
        Extract a concise task title from a Microsoft Teams message using the Ollama API.

        Args:
            message (str): The message text to extract the task title from.
            timeout (int): Request timeout in seconds (default 15).

        Returns:
            str | None: Extracted task title or None if no task found or on error.
        """
        prompt = f"""
        You are a project assistant. Given the following Microsoft Teams message, extract a concise task title. 
        If the message does not describe a task, respond with "None".

        Message:
        "{message}"

        Only return the task title or "None".
        """

        try:
            response = requests.post(
                self.base_url,
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=timeout,
            )
            response.raise_for_status()
            result = response.json().get("response", "").strip()
            logger.info("Copilot extracted task title: %s", result)
            return None if result.lower() == "none" else result
        except requests.RequestException as e:
            logger.error("Copilot request failed: %s", e)
            return None
