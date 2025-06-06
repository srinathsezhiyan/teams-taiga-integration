# core/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.services.copilot_service import Copilot
from core.services.ollama_service import Ollama
from core.services.taiga_service import TaigaAPIClient


class TeamsMessageView(APIView):
    """
    API endpoint to handle incoming messages from Microsoft Teams.
    It processes the message to extract a task title, check for duplicates,
    enhance the task description using an LLM, and create a new task in Taiga.
    """
    def post(self, request):
        try:
            # Extract the 'message' field from the incoming JSON payload
            message = request.data.get("message")
            if not message:
                # Return 400 if no message provided in the request
                return Response(
                    {"error": "No message provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

			# Initialize service clients
            copilot = Copilot()
            ollama = Ollama()
            taiga = TaigaAPIClient()
            
			# Extract task title from the message using Copilot
            title = copilot.extract_task_title(message)

            if not title:
                # If no task title is extracted, return 200 with a message
                return Response(
                    {"info": "No actionable task found."}, status=status.HTTP_200_OK
                )

			# Check if the task already exists in Taiga
            if taiga.task_exists(title):
                # If the task already exists, return 200 with an info message
                return Response(
                    {"info": "Task already exists in Taiga."}, status=status.HTTP_200_OK
                )

			# Enhance the task description and extract subtasks using Ollama
            description, subtasks = ollama.enhance_task_description(title)
            if not description or not subtasks:
				# If no description or subtasks are generated, return 200 with a message
                return Response(
					{"info": "No description or subtasks generated for the task."},
					status=status.HTTP_200_OK,
				)
            # Create the task in Taiga with the provided title, description, and subtasks
            created = taiga.create_task(title, description)

			# If the task creation is successful, return 201 with the task details
            return Response(
                {
                    "message": "Task created successfully.",
                    "task": created,
                    "subtasks": subtasks,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
