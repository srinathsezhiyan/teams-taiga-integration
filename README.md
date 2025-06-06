# Teams-Taiga Integration

## Overview
This project integrates Microsoft Teams with Taiga, enabling automatic creation of tasks in Taiga based on messages posted in Teams. It leverages AI models (via Ollama and Copilot services) to extract task titles and enrich task descriptions with meaningful subtasks.

---

## Features
- Extracts concise task titles from Teams messages using AI  
- Checks for duplicate tasks in Taiga before creation  
- Enhances task descriptions with detailed information and subtasks  
- Uses microservices architecture for modular and scalable design  
- Integrates with Taiga's REST API for project and task management  

---

## Tech Stack
- **Backend:** Python, Django, Django REST Framework  
- **AI Services:** Ollama LLM, Copilot  
- **API Integration:** Taiga API  
- **Deployment:** Docker, AWS (optional)  

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/srinathsezhiyan/teams-taiga-integration.git
cd teams-taiga-integration
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
You can either create a `.env` file or directly add these variables in `settings.py`:

```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama2
TAIGA_URL=https://api.taiga.io/api/v1
TAIGA_USERNAME=your-username
TAIGA_PASSWORD=your-password
TAIGA_PROJECT_SLUG=your-project-slug
```

### 5. Run migrations and start server
```bash
python manage.py migrate
python manage.py runserver
```

---

## API Usage

Send a POST request to:
```
/api/teams/message/
```

With this JSON payload:
```json
{
  "message": "Can we track UI redesign for dashboard this sprint?"
}
```

### Response Example:
```json
{
  "message": "Task created successfully.",
  "task": {
    "id": 123,
    "subject": "UI redesign for dashboard",
    "description": "..."
  },
  "subtasks": [
    "Define UI components",
    "Create mockups",
    "Implement responsive layout"
  ]
}
```

---

## Project Structure

```
teams-taiga-integration/
├── core/
│   ├── views.py                - API View
│   ├── services/
│   │   ├── copilot_service.py  - Uses LLM to extract task titles
│   │   ├── ollama_service.py   - Generates descriptions & subtasks
│   │   ├── taiga_service.py    - Integrates with Taiga API
│   │   └── ollama_client.py    - Wrapper for Ollama LLM API
├── requirements.txt            - Python dependencies
├── manage.py                   - Django management script
└── README.md                   - Project documentation
```

---

## Development Notes

- Ensure Ollama server is running locally or accessible via the `OLLAMA_URL`.
- Make sure your Taiga credentials and project slug are valid.
- For production, configure logging and secure secrets properly.

---

## Contributing

Feel free to fork the repository and submit a pull request. All improvements are welcome!

---

## License

This project is licensed under the MIT License.

---

## Author

**Srinath Sezhiyan**  
GitHub: [srinathsezhiyan](https://github.com/srinathsezhiyan)  
Email: srisezhiyan@gmail.com
