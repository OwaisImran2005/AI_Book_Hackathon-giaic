"""
FastAPI Backend for RAG Pipeline Phase 4: FastAPI Backend and Frontend Integration

This module implements a FastAPI application that exposes the OpenAI agent
from Phase 3 via REST API endpoints. It includes CORS configuration for
Docusaurus integration and a POST /chat endpoint for agent interactions.
"""
import os
import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging

# Import models
from pydantic import BaseModel
from .models import ChatRequest, ChatResponse

# Import agent integration
from .agent_integration import process_agent_query

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

# Configure CORS middleware to allow requests from Docusaurus (localhost:3000 and 3001)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ],  # Docusaurus ports
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
    top_k: Optional[int] = 3  # Number of results to return from RAG


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    query: str
    response: str
    sources: Optional[list] = None
    status: str  # "success" or "error"


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    POST /chat endpoint that accepts queries and returns agent responses
    based on the RAG pipeline.
    """
    try:
        logger.info(f"Received chat request: {request.query}")

        # Process the query using the agent integration
        result = await process_agent_query(request.query, request.top_k)

        logger.info(f"Agent response generated successfully")

        return ChatResponse(
            query=request.query,
            response=result["response"],
            sources=result["sources"],
            status=result["status"]
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