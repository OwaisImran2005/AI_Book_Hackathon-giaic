# Quickstart: RAG Pipeline Phase 1

## Setup

1. **Create the backend directory:**
   ```bash
   mkdir backend
   cd backend
   ```

2. **Initialize uv project:**
   ```bash
   uv init
   ```

3. **Install dependencies:**
   ```bash
   uv add langchain qdrant-client cohere beautifulsoup4 requests python-dotenv pytest
   ```

4. **Create .env file with API keys:**
   ```bash
   # .env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_URL=your_qdrant_cluster_url_here
   ```

## Usage

1. **Run the pipeline:**
   ```bash
   python main.py
   ```

2. **The pipeline will execute in sequence:**
   - `get_urls()`: Fetch list of Docusaurus book URLs
   - `chunk_text()`: Clean and split content into semantic chunks
   - `embed_data()`: Generate vector embeddings using Cohere
   - `store_vectors()`: Upsert vectors to Qdrant Cloud
   - Verification: Query Qdrant to confirm successful storage

## Configuration

- Add your Docusaurus book URLs to the script's URL list
- Adjust chunk size parameters as needed
- Configure Qdrant collection settings in the script

## Testing

Run the tests to verify functionality:
```bash
pytest tests/
```