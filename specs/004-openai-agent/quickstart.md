# Quickstart: RAG Pipeline Phase 3: OpenAI Agent Integration

## Setup

1. **Install dependencies**: Make sure you have the required dependencies:
   ```bash
   pip install openai python-dotenv
   ```

2. **Verify Phase 2 completion**: Ensure the retrieval logic from Phase 2 is working properly with populated vector database

3. **Configure environment**: Ensure the following environment variables are set in your `.env` file:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_URL=your_qdrant_cluster_url_here
   ```

## Usage

1. **Run the agent directly**:
   ```bash
   python agent.py
   ```

2. **Interact with the agent**:
   - Enter your questions in the console when prompted
   - The agent will decide whether to use the RAG tool based on your query
   - Responses will include documentation-specific information when relevant
   - Type "quit" or "exit" to end the session

3. **Example interactions**:
   - Documentation-specific query: "What are the best practices for API design?"
   - General query: "What is Python?"
   - Mixed query: "How do I use the retrieval function in Python?"

## Testing

1. **Test the agent's tool usage**:
   - Ask documentation-specific questions to verify RAG tool usage
   - Ask general questions to verify the agent uses general knowledge appropriately
   - Verify responses include relevant context from the vector database

2. **Validate error handling**:
   - Test with unavailable services to ensure graceful degradation
   - Verify fallback responses work when tools are unavailable

## Verification

- Check that the agent uses the RAG tool for documentation-specific queries
- Verify that responses are context-aware and accurate
- Confirm that the console interface provides a good testing experience
- Validate that error handling works gracefully