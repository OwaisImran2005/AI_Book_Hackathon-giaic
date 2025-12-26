# API Contract: RAG Pipeline Phase 1

## Pipeline Entry Point

### Function: `main()`
- **Purpose**: Execute the complete RAG pipeline from crawling to verification
- **Input**: None (reads configuration from environment variables)
- **Output**: Success/failure status with detailed logging
- **Side Effects**: Creates vector embeddings in Qdrant Cloud

## Core Functions

### Function: `get_urls()`
- **Purpose**: Retrieve list of Docusaurus book URLs to process
- **Input**: None
- **Output**: List of valid URLs to crawl
- **Errors**: Network errors, invalid URL formats

### Function: `chunk_text(content)`
- **Purpose**: Clean and split content into semantic chunks
- **Input**: Raw text content from crawled pages
- **Output**: List of content chunks with metadata
- **Errors**: Content parsing errors

### Function: `embed_data(text_chunks)`
- **Purpose**: Generate vector embeddings for content chunks
- **Input**: List of text chunks
- **Output**: List of vector embeddings with associated metadata
- **Errors**: API rate limits, authentication failures

### Function: `store_vectors(embeddings)`
- **Purpose**: Store vector embeddings in Qdrant Cloud
- **Input**: List of embeddings with metadata
- **Output**: Success/failure status for each stored vector
- **Errors**: Database connection issues, invalid data formats

## Configuration Contract

### Environment Variables
- `COHERE_API_KEY`: Required for embedding generation
- `QDRANT_API_KEY`: Required for vector storage
- `QDRANT_URL`: Required for connecting to Qdrant Cloud