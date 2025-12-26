# Quickstart: RAG Pipeline Phase 2

## Setup

1. **Ensure Phase 1 is complete**: Make sure the vector database from Phase 1 is populated with documents
2. **Verify environment**: Ensure the following environment variables are set in your `.env` file:
   ```bash
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_URL=your_qdrant_cluster_url_here
   ```

3. **Install dependencies**: Make sure you have the required dependencies:
   ```bash
   pip install cohere qdrant-client python-dotenv
   ```

## Usage

1. **Run the retrieval module directly**:
   ```bash
   python backend/retrieve.py
   ```
   This will execute the main function with a sample query and display the top 3 results with their similarity scores.

2. **Use the retrieval functions programmatically**:
   ```python
   from backend.retrieve import embed_query, search_qdrant

   query_text = "Your query here"
   query_embedding = embed_query(query_text)
   results = search_qdrant(query_embedding, top_k=3)
   ```

## Testing

1. **Run the retrieval tests**:
   ```bash
   pytest backend/tests/test_retrieve.py
   ```

2. **Validate "no match" scenarios**:
   - Execute queries that should return no relevant results
   - Verify appropriate responses are returned

3. **Validate "exact match" scenarios**:
   - Execute queries that should match known content
   - Verify highly relevant results with high similarity scores are returned

## Verification

- Check that retrieval returns results within sub-second response time
- Verify that similarity scores are above 0.7 threshold for relevant matches
- Confirm that console logging displays retrieved context clearly
- Validate that the system handles error conditions gracefully