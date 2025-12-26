"""
RAG Pipeline Phase 1: Data Ingestion and Vector Indexing

This script implements a pipeline that:
1. Crawls Docusaurus book URLs
2. Extracts and cleans content
3. Chunks content semantically
4. Generates embeddings using Cohere API
5. Stores vectors with metadata in Qdrant Cloud
"""
import os
import logging
import requests
import time
import asyncio
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
import uuid
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def exponential_backoff_retry(max_retries: int = 3, base_delay: float = 1.0):
    """
    Decorator to implement exponential backoff retry mechanism
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if retries == max_retries - 1:
                        raise e
                    delay = base_delay * (2 ** retries)
                    logger.warning(f"Attempt {retries + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
                    retries += 1
            return None
        return wrapper
    return decorator


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


# Placeholder for the main functions that will be implemented
def get_urls() -> List[str]:
    """
    Fetch list of Docusaurus book URLs by parsing sitemap.xml
    """
    # Allow URLs to be specified via environment variable
    urls_env = os.getenv("DOCUSAURUS_URLS")
    if urls_env:
        # If the URL is a sitemap, process it, otherwise return as is
        urls = [url.strip() for url in urls_env.split(",")]

        # Check if any of the URLs is a sitemap
        all_urls = []
        for url in urls:
            if url.endswith('/sitemap.xml'):
                sitemap_urls = extract_urls_from_sitemap(url)
                all_urls.extend(sitemap_urls)
            else:
                all_urls.append(url)

        return all_urls

    # Default to a list of common Docusaurus documentation sites
    default_urls = [
        "https://docusaurus.io/docs",
        "https://reactjs.org/docs",
        # Add more default URLs or load from config
    ]

    return default_urls


def extract_urls_from_sitemap(sitemap_url: str) -> List[str]:
    """
    Extract all URLs from a sitemap.xml file
    """
    try:
        logger.info(f"Fetching sitemap from: {sitemap_url}")
        response = requests.get(sitemap_url, timeout=30)
        response.raise_for_status()

        from xml.etree import ElementTree as ET
        root = ET.fromstring(response.content)

        urls = []
        # Handle both regular sitemap and sitemap index
        if root.tag.endswith('sitemapindex'):
            # This is a sitemap index, need to fetch individual sitemaps
            for sitemap in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                sitemap_loc = sitemap.text.strip()
                urls.extend(extract_urls_from_sitemap(sitemap_loc))
        else:
            # This is a regular sitemap with URLs
            for url_element in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                url = url_element.text.strip()
                # Filter for documentation pages
                if '/docs/' in url or url.endswith('/docs') or url.endswith('/docs/'):
                    urls.append(url)

        logger.info(f"Extracted {len(urls)} URLs from sitemap")
        return urls

    except Exception as e:
        logger.error(f"Error parsing sitemap {sitemap_url}: {str(e)}")
        # Fallback to just the base URL if sitemap fails
        base_url = sitemap_url.replace('/sitemap.xml', '')
        return [base_url]


@exponential_backoff_retry(max_retries=3, base_delay=1.0)
def crawl_single_url(url: str) -> Dict[str, Any]:
    """
    Crawl a single URL and extract content
    """
    try:
        logger.info(f"Starting crawl for URL: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract main content from Docusaurus-specific selectors
        # Docusaurus typically stores main content in elements with class 'main-wrapper' or similar
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='container')

        if not main_content:
            # Fallback: try to find content in common content containers
            main_content = soup.find('div', {'role': 'main'}) or soup.find('div', class_='docItemContainer')

        # If still no content found, use body
        if not main_content:
            main_content = soup.find('body')

        if main_content:
            # Extract text content, removing extra whitespace
            content = main_content.get_text(separator=' ', strip=True)
        else:
            content = ""

        # Extract page title
        title = soup.find('title')
        page_title = title.get_text().strip() if title else "No Title"

        result = {
            'url': url,
            'title': page_title,
            'content': content,
            'status': 'success',
            'crawl_timestamp': time.time()
        }

        logger.info(f"Successfully crawled URL: {url}")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to crawl URL {url}: {str(e)}")
        return {
            'url': url,
            'title': 'Error',
            'content': '',
            'status': 'failed',
            'error_message': str(e),
            'crawl_timestamp': time.time()
        }
    except Exception as e:
        logger.error(f"Unexpected error crawling URL {url}: {str(e)}")
        return {
            'url': url,
            'title': 'Error',
            'content': '',
            'status': 'failed',
            'error_message': str(e),
            'crawl_timestamp': time.time()
        }


def chunk_text(content: str) -> List[Dict[str, Any]]:
    """
    Split content into semantic chunks using langchain's RecursiveCharacterTextSplitter
    """
    if not content or len(content.strip()) == 0:
        return []

    # Get configuration from environment variables with defaults
    chunk_size = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "100"))

    # Use langchain's RecursiveCharacterTextSplitter for semantic chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,  # Configurable chunk size: 500-1000 tokens as specified
        chunk_overlap=chunk_overlap,  # Configurable overlap to maintain context
        length_function=len,
        is_separator_regex=False,
    )

    # Split the content into chunks
    chunks = text_splitter.split_text(content)

    # Create chunk objects with metadata
    chunked_content = []
    for i, chunk in enumerate(chunks):
        chunk_obj = {
            'id': str(uuid.uuid4()),
            'text': chunk.strip(),
            'source_url': '',  # Will be set when processing crawled content
            'metadata': {
                'chunk_index': i,
                'total_chunks': len(chunks),
                'created_at': time.time()
            }
        }
        chunked_content.append(chunk_obj)

    logger.info(f"Content split into {len(chunked_content)} chunks")
    return chunked_content


@exponential_backoff_retry(max_retries=3, base_delay=1.0)
def embed_data(text_chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate embeddings for text chunks using Cohere API
    """
    if not text_chunks:
        logger.info("No text chunks to embed")
        return []

    # Get Cohere API key from environment
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set")

    # Initialize Cohere client
    co = cohere.Client(cohere_api_key)

    # Extract texts for embedding (limit batch size for API)
    batch_size = 96  # Cohere's recommended batch size
    all_embeddings = []

    for i in range(0, len(text_chunks), batch_size):
        batch = text_chunks[i:i + batch_size]
        texts = [chunk['text'] for chunk in batch]

        try:
            # Generate embeddings using Cohere
            response = co.embed(
                texts=texts,
                model="embed-english-v3.0",  # Using a reliable Cohere embedding model
                input_type="search_document"  # Specify the input type for better embeddings
            )

            # Add embeddings to chunks
            for j, chunk in enumerate(batch):
                embedding_data = {
                    'id': chunk['id'],
                    'text': chunk['text'],
                    'source_url': chunk.get('source_url', ''),
                    'vector': response.embeddings[j],
                    'metadata': chunk.get('metadata', {}),
                    'embedding_model': 'embed-english-v3.0'
                }
                all_embeddings.append(embedding_data)

            logger.info(f"Embedded batch {i//batch_size + 1}/{(len(text_chunks)-1)//batch_size + 1}")

        except Exception as e:
            logger.error(f"Error embedding batch {i//batch_size + 1}: {str(e)}")
            # Return partial results if some batches succeeded
            if i == 0:  # If the first batch failed, raise the error
                raise e

    logger.info(f"Successfully embedded {len(all_embeddings)} text chunks")
    return all_embeddings


def store_vectors(embeddings: List[Dict[str, Any]]) -> bool:
    """
    Store embeddings in Qdrant Cloud with metadata
    """
    if not embeddings:
        logger.info("No embeddings to store")
        return True

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

        # Define collection name
        collection_name = "rag_pipeline_docs"

        # Check if collection exists, create if it doesn't
        collection_exists = False
        try:
            client.get_collection(collection_name)
            collection_exists = True
        except:
            # Collection doesn't exist, need to create it
            pass

        if not collection_exists:
            # Get vector size from first embedding to configure collection
            vector_size = len(embeddings[0]['vector'])

            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            logger.info(f"Created new Qdrant collection: {collection_name}")

        # Process embeddings in smaller batches to avoid timeout
        batch_size = 50  # Smaller batch size to avoid timeouts
        total_embeddings = len(embeddings)

        for i in range(0, total_embeddings, batch_size):
            batch = embeddings[i:i + batch_size]

            # Prepare points for upsert
            points = []
            for embedding_data in batch:
                point = PointStruct(
                    id=embedding_data['id'],
                    vector=embedding_data['vector'],
                    payload={
                        'text': embedding_data['text'],
                        'source_url': embedding_data['source_url'],
                        'metadata': embedding_data['metadata'],
                        'embedding_model': embedding_data.get('embedding_model', 'unknown')
                    }
                )
                points.append(point)

            # Upsert vectors to Qdrant
            client.upsert(
                collection_name=collection_name,
                points=points
            )

            logger.info(f"Stored batch {i//batch_size + 1}/{(total_embeddings-1)//batch_size + 1} ({len(batch)} embeddings)")

        logger.info(f"Successfully stored {total_embeddings} embeddings in Qdrant collection: {collection_name}")

        # Verify that the vectors were stored by checking the collection count
        collection_info = client.get_collection(collection_name)
        stored_count = collection_info.points_count
        logger.info(f"Verification: Qdrant collection '{collection_name}' now contains {stored_count} vectors")

        return True

    except Exception as e:
        logger.error(f"Error storing vectors in Qdrant: {str(e)}")
        return False


def verify_qdrant_data(collection_name: str = "rag_pipeline_docs") -> bool:
    """
    Verify that data exists in Qdrant cluster by checking collection count
    """
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")

    if not qdrant_api_key or not qdrant_url:
        raise ValueError("QDRANT_API_KEY and QDRANT_URL environment variables must be set")

    try:
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            prefer_grpc=True
        )

        # Get collection info
        collection_info = client.get_collection(collection_name)
        point_count = collection_info.points_count

        logger.info(f"Verification: Found {point_count} vectors in collection '{collection_name}'")

        # Return True if there are vectors in the collection
        return point_count > 0

    except Exception as e:
        logger.error(f"Error verifying data in Qdrant: {str(e)}")
        return False


def main():
    """
    Main entry point for the RAG pipeline
    Orchestrates the full pipeline: scrape -> chunk -> embed -> upsert -> verify
    """
    start_time = time.time()
    logger.info("Starting RAG Pipeline Phase 1: Data Ingestion and Vector Indexing")

    try:
        # Get environment variables
        env_vars = get_environment_variables()
        logger.info("Environment variables loaded successfully")

        # Step 1: Get URLs to process
        urls_start = time.time()
        urls = get_urls()
        urls_time = time.time() - urls_start
        logger.info(f"Processing {len(urls)} URLs: {urls} (took {urls_time:.2f}s)")

        all_chunks = []
        # Step 2: Crawl and extract content from each URL
        crawl_start = time.time()
        for url in urls:
            logger.info(f"Processing URL: {url}")
            crawled_data = crawl_single_url(url)

            if crawled_data['status'] == 'success':
                # Add source URL to the chunking process
                content = crawled_data['content']
                # Process the content into chunks
                chunks = chunk_text(content)
                # Update source URL for each chunk
                for chunk in chunks:
                    chunk['source_url'] = url
                all_chunks.extend(chunks)
                logger.info(f"Extracted and chunked content from {url}, got {len(chunks)} chunks")
            else:
                logger.error(f"Failed to crawl {url}: {crawled_data.get('error_message', 'Unknown error')}")
        crawl_time = time.time() - crawl_start

        if not all_chunks:
            logger.warning("No content chunks were generated from the URLs")
            return

        logger.info(f"Total content chunks generated: {len(all_chunks)} (crawl took {crawl_time:.2f}s)")

        # Step 3: Generate embeddings for all chunks
        logger.info("Starting embedding generation...")
        embed_start = time.time()
        embeddings = embed_data(all_chunks)
        embed_time = time.time() - embed_start
        logger.info(f"Generated embeddings for {len(embeddings)} chunks (took {embed_time:.2f}s)")

        # Step 4: Store embeddings in Qdrant
        logger.info("Storing embeddings in Qdrant...")
        store_start = time.time()
        success = store_vectors(embeddings)
        store_time = time.time() - store_start

        if success:
            logger.info(f"Embeddings successfully stored in Qdrant (took {store_time:.2f}s)")

            # Step 5: Verify that data exists in Qdrant
            logger.info("Verifying data in Qdrant...")
            verify_start = time.time()
            verification_result = verify_qdrant_data()
            verify_time = time.time() - verify_start

            if verification_result:
                total_time = time.time() - start_time
                logger.info("✅ SUCCESS: RAG Pipeline completed successfully!")
                logger.info("✅ Data verification confirmed: vectors exist in Qdrant cluster")
                logger.info(f"📈 Performance Summary:")
                logger.info(f"  - URL retrieval: {urls_time:.2f}s")
                logger.info(f"  - Crawling: {crawl_time:.2f}s")
                logger.info(f"  - Embedding: {embed_time:.2f}s")
                logger.info(f"  - Storage: {store_time:.2f}s")
                logger.info(f"  - Verification: {verify_time:.2f}s")
                logger.info(f"  - Total: {total_time:.2f}s")
            else:
                logger.error("❌ VERIFICATION FAILED: No vectors found in Qdrant cluster")
        else:
            logger.error("❌ FAILED: Could not store embeddings in Qdrant")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()
