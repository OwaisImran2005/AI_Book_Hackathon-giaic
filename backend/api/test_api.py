"""
Test file for the FastAPI backend API
"""
import asyncio
import pytest
from fastapi.testclient import TestClient
from .main import app
import json


def test_health_endpoint():
    """Test the health check endpoint"""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert response.json()["service"] == "RAG Pipeline API"


def test_chat_endpoint():
    """Test the chat endpoint with a simple query"""
    with TestClient(app) as client:
        # Test with a simple query
        test_data = {
            "query": "What is RAG?",
            "top_k": 3
        }

        response = client.post("/chat", json=test_data)

        # Check that the response is successful
        assert response.status_code == 200

        # Check that the response has the expected structure
        data = response.json()
        assert "query" in data
        assert "response" in data
        assert "sources" in data
        assert "status" in data

        # Check that the query matches what we sent
        assert data["query"] == test_data["query"]

        # Check that the status is success
        assert data["status"] == "success"


def test_chat_endpoint_empty_query():
    """Test the chat endpoint with an empty query"""
    with TestClient(app) as client:
        # Test with an empty query
        test_data = {
            "query": "",
            "top_k": 3
        }

        response = client.post("/chat", json=test_data)

        # Should return an error for empty query
        assert response.status_code == 500


def test_chat_endpoint_missing_query():
    """Test the chat endpoint with missing query field"""
    with TestClient(app) as client:
        # Test with missing query field
        test_data = {
            "top_k": 3
        }

        response = client.post("/chat", json=test_data)

        # Should return validation error
        assert response.status_code == 422  # Unprocessable Entity


if __name__ == "__main__":
    # Run the tests
    test_health_endpoint()
    print("✓ Health endpoint test passed")

    test_chat_endpoint()
    print("✓ Chat endpoint test passed")

    test_chat_endpoint_empty_query()
    print("✓ Chat endpoint empty query test passed")

    test_chat_endpoint_missing_query()
    print("✓ Chat endpoint missing query test passed")

    print("\nAll tests passed!")