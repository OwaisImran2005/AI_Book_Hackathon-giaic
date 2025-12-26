# Data Model: RAG Pipeline Phase 1

## Entities

### Content Chunk
- **id**: string (auto-generated UUID)
- **text**: string (the actual content text, max 1000 tokens)
- **source_url**: string (URL where content was extracted from)
- **metadata**: object (additional metadata like page title, headings, etc.)
- **created_at**: timestamp (when chunk was created)

### Vector Embedding
- **id**: string (corresponds to content chunk ID)
- **vector**: array<float> (numerical representation from Cohere embedding)
- **text**: string (original text content)
- **source_url**: string (URL of original document)
- **metadata**: object (additional metadata for search context)

### Crawled Document
- **url**: string (source URL)
- **title**: string (page title)
- **content**: string (raw extracted content)
- **status**: enum (success, failed, partial)
- **crawl_timestamp**: timestamp (when crawling occurred)
- **error_message**: string (if status is failed)

## Relationships
- One Crawled Document → Many Content Chunks (document gets chunked into multiple pieces)
- One Content Chunk → One Vector Embedding (each chunk gets one embedding)

## Validation Rules
- Content Chunk text must be between 100-1000 tokens
- Source URLs must be valid and accessible
- Vector embeddings must have consistent dimensions (as per Cohere model)
- Metadata must be serializable to JSON format

## State Transitions
- Crawled Document: pending → processing → success/failed
- Content Chunk: created → embedded → stored