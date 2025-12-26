"""
RAG Pipeline Phase 4: FastAPI Backend and Frontend Integration

This module implements a FastAPI application that serves the AI agent
from agent.py via a REST API endpoint. It includes CORS configuration
for localhost integration and a POST /chat endpoint for agent interactions.
"""
import os
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import logging

# Import the agent from agent.py
from agent import create_agent
from agents import Runner

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="RAG Pipeline API",
    description="API for RAG Pipeline Phase 4: FastAPI Backend and Frontend Integration",
    version="1.0.0"
)

# Configure CORS middleware to allow requests from localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Docusaurus default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers that might be needed for error handling
    expose_headers=["Access-Control-Allow-Origin"]
)

# Pydantic models for request/response
class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    query: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    query: str
    response: str
    status: str  # "success" or "error"


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    POST /chat endpoint that accepts queries and returns agent responses
    based on the RAG pipeline.
    """
    try:
        logger.info(f"Received chat request: {request.query}")

        # Create the agent
        agent = create_agent()

        # Run the agent with the user query
        result = await Runner.run(agent, request.query)

        # Extract the final output from the agent result
        response_text = result.final_output if hasattr(result, 'final_output') else str(result)

        logger.info(f"Agent response generated successfully")

        return ChatResponse(
            query=request.query,
            response=response_text,
            status="success"
        )
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "RAG Pipeline API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)