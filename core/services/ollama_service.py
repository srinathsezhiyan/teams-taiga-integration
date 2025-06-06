from core.services.ollama_client import OllamaClient


class Ollama:
    # System prompt template instructing the model on what to generate
    SYSTEM_PROMPT = (
        "You are a project management assistant. Given a task title, generate:\n"
        "- A clear and detailed task description\n"
        "- 3–5 meaningful subtasks\n\n"
        "Respond in this format:\n"
        "Description: <description>\n"
        "Subtasks:\n- <subtask1>\n- <subtask2>\n..."
    )

    def __init__(self, llm_client: OllamaClient = None):
        """
        Initialize Ollama service with an optional OllamaClient instance.
        If no client is provided, a default one is created.
        
        Args:
            llm_client (OllamaClient, optional): Instance of OllamaClient to interact with the API.
        """
        self.llm_client = llm_client or OllamaClient()

    def enhance_task_description(self, title: str):
        """
        Enhance a given task title by generating a detailed description and subtasks.

        Args:
            title (str): The task title to enhance.

        Returns:
            tuple: A tuple containing:
                - description (str): Detailed task description.
                - subtasks (list): List of meaningful subtasks.
        """
        prompt = self._build_prompt(title)
        output = self.llm_client.generate(prompt)

        # If no output received from the client, return empty values
        if not output:
            return "", []

        description, subtasks = self._parse_response(output)
        return description, subtasks

    def _build_prompt(self, title: str) -> str:
        """
        Construct the prompt sent to the language model by combining system prompt and task title.

        Args:
            title (str): The task title.

        Returns:
            str: The full prompt string.
        """
        return f'{self.SYSTEM_PROMPT}\n\nTask Title:\n"{title}"'

    def _parse_response(self, output: str):
        """
        Parse the model's response to separate the description and the subtasks.

        Args:
            output (str): Raw response string from the model.

        Returns:
            tuple: Parsed description string and list of subtasks.
        """
        description = ""
        subtasks = []

        # Check if the response contains subtasks section
        if "Subtasks:" in output:
            parts = output.split("Subtasks:")
            # Extract and clean the description part
            description = parts[0].replace("Description:", "").strip()

            # Extract subtasks lines, cleaning leading "- " and whitespace
            subtasks_raw = parts[1].strip().split("\n")
            subtasks = [
                line.strip("- ").strip() for line in subtasks_raw if line.strip()
            ]
        else:
            # If no subtasks section found, treat entire output as description
            description = output.strip()

        return description, subtasks
