# API Contract: RAG Pipeline Phase 2 - Retrieval Logic

## Function: `embed_query(query_text: str) -> List[float]`
- **Purpose**: Generate vector embedding for input text query using Cohere API
- **Input**: Text string to be embedded
- **Output**: Float array representing the embedding vector
- **Errors**: Raises exception if Cohere API call fails
- **Side Effects**: Makes external API call to Cohere service

## Function: `search_qdrant(query_embedding: List[float], top_k: int = 3) -> List[Dict]`
- **Purpose**: Search Qdrant vector database for similar content chunks
- **Input**: Query embedding vector and number of top results to return
- **Output**: List of dictionaries containing text chunks, similarity scores, and metadata
- **Errors**: Raises exception if Qdrant connection fails
- **Side Effects**: Queries existing Qdrant collection from Phase 1

## Function: `retrieve(query_text: str, top_k: int = 3) -> Dict`
- **Purpose**: High-level retrieval function that combines embedding and search
- **Input**: Text query and number of top results to return
- **Output**: Dictionary containing query, results, and metadata
- **Errors**: Propagates errors from embed_query or search_qdrant
- **Side Effects**: Makes external API calls and queries database

## Configuration Contract
- `COHERE_API_KEY`: Required for embedding generation
- `QDRANT_API_KEY`: Required for vector database access
- `QDRANT_URL`: Required for connecting to Qdrant Cloud