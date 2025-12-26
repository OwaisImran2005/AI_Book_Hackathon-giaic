"""
RAG Pipeline Phase 3: OpenAI Agent Integration

This module implements an OpenAI agent that wraps the retrieval logic from Phase 2
as a tool function and connects it to the OpenAI Agent using the Agents SDK.
The agent will use the OpenAI SDK with GPT-4o or GPT-4o-mini model to process
user queries, decide when to invoke the RAG tool, and generate context-aware
responses based on retrieved documentation content.
"""
import os
import json
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
import asyncio
from backend.retrieve import search_qdrant
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

ROUTER_API_KEY = "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"

client = AsyncOpenAI(
    api_key=ROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

third_party_model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="mistralai/devstral-2512:free"
)

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




    # required_vars = ['OPENAI_API_KEY']
    # env_vars = {}

    # # for var in required_vars:
    #     value = os.getenv(var)
    #     if not value:
    #         raise ValueError(f"Required environment variable {var} is not set")
    #     env_vars[var] = value

    # return env_vars






@function_tool
def retrieve_documentation(query: str, top_k: int = 3) -> Dict[str, Any]:
    """
    Search the documentation database for relevant information.

    Args:
        query: The search query to find relevant documentation
        top_k: Number of results to return (default 3)
    """
    try:
        # Import the embedding function from retrieve module
        from backend.retrieve import embed_query

        # Embed the query
        query_embedding = embed_query(query)

        # Search the Qdrant database
        results = search_qdrant(query_embedding, top_k=top_k)

        return {
            "status": "success",
            "results": results,
            "query": query
        }
    except Exception as e:
        logger.error(f"Error calling RAG function: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "query": query
        }


def create_agent():
    """
    Create an OpenAI Agent with the RAG tool
    """
    agent = Agent(
        name="Documentation Assistant",
        instructions="""
        You are an AI assistant with access to documentation. Your primary function is to help users by providing accurate information based on documentation when appropriate.

        - When a user asks a question that might be related to documentation, use the 'retrieve_documentation' tool to search for relevant information
        - Only use the tool when you think the question requires specific documentation knowledge
        - For general knowledge questions, respond using your general knowledge without using the tool
        - When you receive documentation results, incorporate the relevant information into your response
        - Always be clear about what information comes from the documentation versus your general knowledge
        - If the documentation doesn't contain relevant information, acknowledge this and respond based on your general knowledge
        """,
        model=third_party_model,
        tools=[retrieve_documentation]
    )
    logger.info("Agent created successfully")
    return agent


async def chat_with_agent():
    """
    Main interactive console loop for the agent
    """
    logger.info("Initializing OpenAI Agent with RAG Tool Integration...")

    try:
        # Get environment variables
        env_vars = get_environment_variables()
        logger.info("Environment variables loaded successfully")

        # Create the agent
        agent = create_agent()

        logger.info("Agent is ready! Type 'quit' or 'exit' to end the session.")

        while True:
            # Get user input
            user_input = input("\nYou: ").strip()

            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Agent: Goodbye!")
                break

            if not user_input:
                continue

            try:
                # Run the agent with the user input
                result = await Runner.run(agent, user_input)

                # Display the agent's response
                print(f"\nAgent: {result.final_output}")

            except Exception as e:
                logger.error(f"Error processing query: {str(e)}")
                print(f"Agent: Sorry, I encountered an error processing your request: {str(e)}")

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")


def main():
    """
    Main function to run the agent
    """
    asyncio.run(chat_with_agent())


if __name__ == "__main__":
    main()