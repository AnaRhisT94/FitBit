'''
This file sets up the FastAPI application and defines the API endpoints.
'''
import logging
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .agent import get_agent_executor, llm

# --- Pydantic Models for API ---
class QueryRequest(BaseModel):
    query: str
    session_id: str = "default_session"
    user_id: str

class QueryResponse(BaseModel):
    answer: str

# --- FastAPI Application ---
app = FastAPI(
    title="Fitbit Conversational AI POC (LangChain ReAct Agent)",
    version="2.0.0"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    if not llm:
        logger.warning("LLM client not available. The /query endpoint will fail.")
    else:
        logger.info("Service started successfully with LLM client initialized.")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Handles user queries using a stateful LangChain agent."""
    if not llm:
        raise HTTPException(status_code=500, detail="LLM not initialized.")

    try:
        start_time = time.time()
        agent_executor = get_agent_executor(request.session_id, request.user_id)
        response = await agent_executor.ainvoke({"input": request.query})
        answer = response.get("output", "I'm not sure how to answer that.")
        duration = time.time() - start_time
        logger.info(f"Agent response time: {duration:.2f} seconds")
        return QueryResponse(answer=answer)
    except Exception as e:
        logger.error(f"Error during agent execution: {e}")
        raise HTTPException(status_code=500, detail=f"Agent failed to process request: {e}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "llm_initialized": llm is not None}