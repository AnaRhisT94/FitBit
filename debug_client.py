import requests
import uuid
import json
from src.fitbit_agent.service import QueryRequest  # Add this import

# Configuration
BASE_URL = "http://localhost:8000"

def start_debug_session():
    """
    Starts an interactive command-line session to debug the Fitbit agent.
    
    This client maintains a single session ID for the entire conversation,
    allowing you to test the agent's conversational memory.
    
    You can set breakpoints in this script using your IDE's debugger to:
    - Inspect the `payload` before it's sent.
    - Inspect the `response` object after it's received from the server.
    """
    session_id = str(uuid.uuid4())
    print("--- Starting Interactive Debug Session ---")
    print(f"Session ID: {session_id}")
    print("Type 'exit' or 'quit' to end the session.")
    print("-" * 38)

    # First, check if the service is healthy
    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        health_response.raise_for_status()
        if not health_response.json().get("llm_initialized"):
            print("WARNING: LLM is not initialized on the server. Queries will fail.")
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Service is not reachable at {BASE_URL}. Please ensure it's running.")
        print(f"Details: {e}")
        return

    while True:
        try:
            # Get user input from the command line
            query = "How did I sleep last night?" #input("> You: ")
            user_id = "alex_fitbit"

            if query.lower() in ["exit", "quit"]:
                print("Ending session. Goodbye!")
                break

            # This is a great place for a breakpoint to inspect the `payload`
            payload = QueryRequest(
                query=query,
                session_id=session_id,
                user_id=user_id
            ).model_dump()  # Convert Pydantic model to dict

            response = requests.post(
                f"{BASE_URL}/query",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()

            # This is a great place for a breakpoint to inspect the `response`
            data = response.json()
            answer = data.get("answer", "Error: No answer found in response.")

            print(f"\n< Assistant: {answer}\n")

        except requests.exceptions.RequestException as e:
            print(f"ERROR: An error occurred while communicating with the service: {e}")
        except KeyboardInterrupt:
            print("\nEnding session. Goodbye!")
            break

if __name__ == "__main__":
    start_debug_session()