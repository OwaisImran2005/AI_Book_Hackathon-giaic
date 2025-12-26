# Data Model: RAG Pipeline Phase 2

## Entities

### Query Embedding
- **text**: string (the original query text)
- **vector**: array<float> (numerical representation from Cohere embedding)
- **embedding_model**: string (identifier for the model used)
- **timestamp**: datetime (when the embedding was generated)

### Search Result
- **id**: string (corresponds to the original document chunk ID in Qdrant)
- **score**: float (similarity score from 0.0 to 1.0)
- **text**: string (the retrieved text content)
- **source_url**: string (URL of the original document)
- **metadata**: object (additional metadata from the Qdrant payload)

### Retrieval Response
- **query**: string (the original query text)
- **results**: array<Search Result> (top matching results ordered by score)
- **query_embedding**: Query Embedding (the embedded query)
- **timestamp**: datetime (when the retrieval was performed)
- **execution_time_ms**: float (time taken for the retrieval operation)

## Relationships
- One Query Embedding → Many Search Results (through similarity matching)
- One Retrieval Response → One Query Embedding + Many Search Results

## Validation Rules
- Similarity scores must be between 0.0 and 1.0
- Query text must not be empty or exceed maximum length limits
- Search results must be ordered by descending similarity score
- Metadata must be serializable to JSON format

## State Transitions
- Query: received → embedded → searched → results returned
- Search Result: candidate → scored → ranked → returned