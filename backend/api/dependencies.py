"""
API dependencies and error handling for FastAPI application
"""
from typing import Callable, Awaitable
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def handle_request_exceptions(request: Request, call_next: Callable[[Request], Awaitable]) -> JSONResponse:
    """
    Global exception handler for API requests
    """
    try:
        response = await call_next(request)
        return response
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unhandled exception in request: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(e)}"}
        )


def validate_query(query: str) -> bool:
    """
    Validate the query string
    """
    if not query or len(query.strip()) == 0:
        return False
    if len(query) > 1000:  # Arbitrary limit, can be adjusted
        return False
    return True


def sanitize_query(query: str) -> str:
    """
    Sanitize the query string
    """
    # Remove any potentially harmful characters if needed
    # For now, just strip whitespace
    return query.strip()


def get_agent_config():
    """
    Get configuration for the agent
    """
    # This could include model selection, temperature settings, etc.
    return {
        "model": "mistralai/devstral-2512:free",
        "temperature": 0.7,
        "top_k": 3
    }