import uvicorn
from src.fitbit_agent.service import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,  # Set to False for debugging
        workers=1,     # Single worker for debugging
    ) 