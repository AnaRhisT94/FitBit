Fitbit Conversational AI Framework
This repository contains a Proof of Concept (POC) for a conversational AI assistant for Fitbit, built using FastAPI and LangChain. The assistant is designed to provide personalized health insights based on user data.

Project Structure
The project is organized in a modular src layout to separate concerns, making it scalable and maintainable:

fitbit_conversational_ai/
├── .gitignore
├── README.md
├── .env.example
├── debug_client.py
├── requirements.txt
├── run_server.py
├── notebooks/
│   └── fitbit_poc_notebook.ipynb
├── src/
│   └── fitbit_agent/
│       ├── __init__.py
│       ├── agent.py
│       ├── service.py
│       └── tools.py
└── tests/
    └── test_tools.py

src/fitbit_agent/: Contains the core application logic.

service.py: The FastAPI web service and API endpoints.

agent.py: The core LangChain agent logic, prompt, and memory management.

tools.py: The tools the agent can use and the mock data store.

notebooks/: Contains the Jupyter notebook for interacting with the agent.

tests/: Contains unit tests for the application components.

debug_client.py: An interactive command-line client for debugging.

run_server.py: A simple script to run the production server.

Setup Instructions
Follow these steps to get the project running locally.

1. Clone the Repository
git clone <your_repository_url>
cd fitbit_conversational_ai

2. Create and Activate a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

# Create the virtual environment
python -m venv venv

# Activate it (on macOS/Linux)
source venv/bin/activate

# Or on Windows
venv\Scripts\activate

3. Install Dependencies
Install all the required Python packages from the requirements.txt file.

pip install -r requirements.txt

4. Set Up Environment Variables
The application requires an Anthropic API key to function.

Copy the example .env.example file to a new file named .env.

Open the .env file and add your Anthropic API key.

cp .env.example .env
# Now, edit the .env file with your text editor

Your .env file should look like this:

ANTHROPIC_API_KEY="sk-ant-api03-..."

How to Run the Application
1. Start the FastAPI Service
You can run the server in two modes:

Development Mode (with auto-reload):
This is best for development, as the server will automatically restart when you make code changes.

uvicorn src.fitbit_agent.service:app --reload

Production/Debug Mode:
Use the provided run_server.py script.

python run_server.py

Once the server is running, it will be accessible at http://localhost:8000.

2. Interact with the Agent
You have two clients to choose from:

Jupyter Notebook (Recommended for Demonstration):

Start Jupyter Lab or Jupyter Notebook:

jupyter lab

Navigate to and open notebooks/fitbit_poc_notebook.ipynb.

Run the cells in the notebook to have a guided conversation with the assistant.

Interactive Debug Client:
For a continuous, command-line conversation, run the debug_client.py script.

python debug_client.py

Type your questions and press Enter. Type exit to quit.

Important: While interacting with a client, check the terminal where the Uvicorn server is running. You will see the agent's detailed "thoughts" and actions printed in the logs, which is excellent for debugging.

How to Run Tests
The project includes unit tests to ensure the tools function correctly. To run the tests, execute the following command from the root directory:

python -m unittest discover tests
