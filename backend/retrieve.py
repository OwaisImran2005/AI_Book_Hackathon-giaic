"""
RAG Pipeline Phase 2: Retrieval Logic and Pipeline Testing

This module implements retrieval functionality that:
1. Accepts text queries
2. Generates embeddings using Cohere API
3. Searches Qdrant vector database for relevant content chunks
4. Returns results with similarity scores for debugging
"""
import os
import logging
import time
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance, SearchRequest
import uuid

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_environment_variables():
    """
    Get required environment variables with validation
    """
    required_vars = ['COHERE_API_KEY', 'QDRANT_API_KEY', 'QDRANT_URL']
    env_vars = {}

    for var in required_vars:
        value = os.getenv(var)
        if not value:
            raise ValueError(f"Required environment variable {var} is not set")
        env_vars[var] = value

    return env_vars


def embed_query(query: str) -> List[float]:
    """
    Generate embedding for a text query using Cohere API
    """
    if not query or len(query.strip()) == 0:
        raise ValueError("Query cannot be empty")

    # Get Cohere API key from environment
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set")

    # Initialize Cohere client
    co = cohere.Client(cohere_api_key)

    try:
        # Generate embedding using Cohere
        response = co.embed(
            texts=[query],
            model="embed-english-v3.0",  # Using the same model as in Phase 1
            input_type="search_query"  # Specify the input type for better embeddings
        )

        # Return the embedding vector
        embedding = response.embeddings[0]
        logger.info(f"Successfully generated embedding for query: {query[:50]}...")
        return embedding

    except cohere.CohereError as e:
        logger.error(f"Cohere API error generating embedding for query: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error generating embedding for query: {str(e)}")
        raise


def search_qdrant(query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search Qdrant vector database for relevant content chunks
    """
    # Get Qdrant configuration from environment
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")

    if not qdrant_api_key or not qdrant_url:
        raise ValueError("QDRANT_API_KEY and QDRANT_URL environment variables must be set")

    try:
        # Initialize Qdrant client
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            prefer_grpc=True
        )

        # Define collection name (same as used in Phase 1)
        collection_name = "rag_pipeline_docs"

        # Search for similar vectors
        search_results = client.query_points(
            collection_name=collection_name,
            query=query_embedding,
            limit=top_k,
            with_payload=True
        )

        # Format results - handling the new Qdrant query_points result format
        formatted_results = []
        # query_points returns a NamedTuple with points attribute containing the actual results
        search_points = search_results.points if hasattr(search_results, 'points') else search_results
        for result in search_points:
            formatted_result = {
                'id': result.id,
                'text': result.payload.get('text', '') if result.payload else '',
                'source_url': result.payload.get('source_url', '') if result.payload else '',
                'similarity_score': result.score,
                'metadata': result.payload.get('metadata', {}) if result.payload else {},
                'embedding_model': result.payload.get('embedding_model', 'unknown') if result.payload else 'unknown'
            }
            formatted_results.append(formatted_result)

        logger.info(f"Found {len(formatted_results)} results for query embedding")
        return formatted_results

    except Exception as e:
        logger.error(f"Error searching Qdrant: {str(e)}")
        raise


def process_and_format_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Process and format search results for output
    """
    if not results:
        logger.info("No results to process")
        return []

    processed_results = []
    for result in results:
        processed_result = {
            'id': result.get('id'),
            'text': result.get('text', '')[:500] + "..." if len(result.get('text', '')) > 500 else result.get('text', ''),
            'source_url': result.get('source_url', ''),
            'similarity_score': round(result.get('similarity_score', 0), 4),
            'metadata': result.get('metadata', {}),
            'embedding_model': result.get('embedding_model', 'unknown')
        }
        processed_results.append(processed_result)

    logger.info(f"Processed {len(processed_results)} results for output")
    return processed_results


def retrieve(query: str, top_k: int = 5, similarity_threshold: float = 0.3) -> List[Dict[str, Any]]:
    """
    Main retrieval function that accepts text queries and searches the Qdrant vector database
    """
    if not query or len(query.strip()) == 0:
        raise ValueError("Query cannot be empty")

    logger.info(f"Starting retrieval for query: {query}")

    start_time = time.time()

    try:
        # Log query details
        logger.info(f"Query length: {len(query)} characters, top_k: {top_k}, threshold: {similarity_threshold}")

        # Step 1: Embed the query
        query_embedding = embed_query(query)

        # Step 2: Search Qdrant for similar content
        raw_results = search_qdrant(query_embedding, top_k)

        # Step 3: Filter results based on similarity threshold
        filtered_results = []
        for result in raw_results:
            if result['similarity_score'] >= similarity_threshold:
                filtered_results.append(result)
            else:
                logger.debug(f"Filtered out result with low similarity score: {result['similarity_score']}")

        # Step 4: Process and format results
        formatted_results = process_and_format_results(filtered_results)

        total_time = time.time() - start_time

        # Log retrieval summary
        logger.info(f"Retrieval completed in {total_time:.2f}s")
        logger.info(f"Found {len(formatted_results)} results above threshold {similarity_threshold}")
        if formatted_results:
            logger.info(f"Highest similarity score: {max(r['similarity_score'] for r in formatted_results):.4f}")
            logger.info(f"Lowest similarity score: {min(r['similarity_score'] for r in formatted_results):.4f}")

        # Log detailed results info
        for i, result in enumerate(formatted_results):
            logger.info(f"Result {i+1}: Score={result['similarity_score']}, URL={result['source_url']}")

        return formatted_results

    except Exception as e:
        logger.error(f"Error during retrieval: {str(e)}")
        raise


def retrieve_with_validation(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve function with validation that the results are semantically relevant to the input query
    """
    if not query or len(query.strip()) == 0:
        raise ValueError("Query cannot be empty")

    results = retrieve(query, top_k)

    # Validate semantic relevance (basic validation)
    for result in results:
        text = result.get('text', '').lower()
        query_lower = query.lower()

        # Simple validation: check if query terms appear in result text (with some tolerance)
        query_words = query_lower.split()
        matching_words = [word for word in query_words if word in text]

        if len(query_words) > 0:
            relevance_ratio = len(matching_words) / len(query_words)
            logger.debug(f"Relevance check for '{query[:30]}...': {len(matching_words)}/{len(query_words)} words matched ({relevance_ratio:.2f})")

    return results


def test_retrieval():
    """
    Test function to validate retrieval quality with 'no match' and 'exact match' scenarios
    """
    logger.info("Starting retrieval quality tests...")

    # Test 1: "No match" scenario
    logger.info("Test 1: Testing 'no match' scenario")
    try:
        no_match_query = "asdasdasdasdasdasdasdasdasdasd"  # Random string unlikely to match
        no_match_results = retrieve(no_match_query, top_k=3)

        logger.info(f"No match query results: {len(no_match_results)} results found")
        for i, result in enumerate(no_match_results):
            logger.info(f"  Result {i+1}: Score={result['similarity_score']}, Text='{result['text'][:100]}...'")

    except Exception as e:
        logger.error(f"Error in 'no match' test: {str(e)}")

    # Test 2: Simple query (if we have data in the database)
    logger.info("Test 2: Testing with a simple query")
    try:
        simple_query = "documentation"
        simple_results = retrieve(simple_query, top_k=3)

        logger.info(f"Simple query results: {len(simple_results)} results found")
        for i, result in enumerate(simple_results):
            logger.info(f"  Result {i+1}: Score={result['similarity_score']}, Text='{result['text'][:100]}...'")

    except Exception as e:
        logger.error(f"Error in simple query test: {str(e)}")

    logger.info("Retrieval quality tests completed")


if __name__ == "__main__":
    # Example usage
    try:
        # Get environment variables
        env_vars = get_environment_variables()
        logger.info("Environment variables loaded successfully")

        # Run test
        test_retrieval()

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")