import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class OllamaClient:
    def __init__(self, model: str = None, base_url: str = None):
        """
        Initialize the OllamaClient with optional model and base_url parameters.
        Defaults are loaded from Django settings if not provided.

        Args:
            model (str, optional): Name of the Ollama model to use.
            base_url (str, optional): Base URL for the Ollama API endpoint.
        """
        self.model = model or settings.OLLAMA_MODEL
        self.base_url = base_url or f"{settings.OLLAMA_URL}/api/generate"

    def generate(self, prompt: str, stream: bool = False, timeout: int = 15) -> str | None:
        """
        Send a prompt to the Ollama API to generate a response.

        Args:
            prompt (str): The prompt string to send to the Ollama model.
            stream (bool): Whether to stream the response (default False).
            timeout (int): HTTP request timeout in seconds (default 15).

        Returns:
            str | None: The generated response text if successful, else None.
        """
        try:
            response = requests.post(
                self.base_url,
                json={"model": self.model, "prompt": prompt, "stream": stream},
                timeout=timeout,
            )
            # Raise an HTTPError if the request returned an unsuccessful status code
            response.raise_for_status()

            # Extract the 'response' field from JSON and strip whitespace
            result = response.json().get("response", "").strip()

            logger.info("Ollama response: %s", result)
            return result

        except requests.RequestException as e:
            # Log the exception details
            logger.error("OllamaClient error: %s", str(e))
            return None
