"""
Agent integration module for connecting the existing agent functionality to the API
"""
import asyncio
import sys
import os
from typing import Dict, Any, Optional
from agents import Runner

# Add the project root to the path so we can import from the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agent import create_agent
from backend.retrieve import retrieve
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def process_agent_query(query: str, top_k: int = 3) -> Dict[str, Any]:
    """
    Process a query using the existing agent functionality
    """
    try:
        logger.info(f"Processing agent query: {query}")

        # Get retrieval results using the existing RAG pipeline
        retrieval_results = get_retrieval_results(query, top_k)
        if retrieval_results["status"] == "success":
            logger.info(f"Retrieved {len(retrieval_results['results'])} results for query")
        else:
            logger.warning(f"Retrieval failed: {retrieval_results.get('error', 'Unknown error')}")

        # Create the agent
        agent = create_agent()

        # Run the agent with the user query
        result = await Runner.run(agent, query)

        # Extract the final output from the agent result
        response_text = result.final_output if hasattr(result, 'final_output') else str(result)

        logger.info(f"Agent processed query successfully")

        # Return sources from the retrieval results
        sources = retrieval_results.get("results", [])
        return {
            "query": query,
            "response": response_text,
            "sources": sources,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error processing agent query: {str(e)}")
        return {
            "query": query,
            "response": f"Error processing query: {str(e)}",
            "sources": [],
            "status": "error"
        }


def get_retrieval_results(query: str, top_k: int = 3) -> Dict[str, Any]:
    """
    Get retrieval results using the existing RAG pipeline
    """
    try:
        logger.info(f"Retrieving results for query: {query}")

        # Use the existing retrieve function from backend/retrieve.py
        results = retrieve(query, top_k=top_k)

        logger.info(f"Retrieved {len(results)} results")

        return {
            "query": query,
            "results": results,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error retrieving results: {str(e)}")
        return {
            "query": query,
            "results": [],
            "status": "error",
            "error": str(e)
        }