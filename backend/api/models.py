"""
Pydantic models for FastAPI API endpoints
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    query: str
    top_k: Optional[int] = 3  # Number of results to return from RAG


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    query: str
    response: str
    sources: Optional[List[Dict[str, Any]]] = []
    status: str  # "success" or "error"
    metadata: Optional[Dict[str, Any]] = {}


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str
    service: str