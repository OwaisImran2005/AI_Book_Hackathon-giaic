"""
Test suite for retrieval functionality
Validates the retrieval pipeline handles "no match" and "exact match" scenarios correctly
"""
import pytest
import os
from unittest.mock import Mock, patch
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from retrieve import retrieve, embed_query, search_qdrant, retrieve_with_validation


def test_embed_query_with_valid_input():
    """Test that embed_query generates embeddings for valid input"""
    # This test would require actual API keys to run properly
    # For now, we'll test the error handling
    with pytest.raises(ValueError):
        # Test with empty query
        embed_query("")


def test_retrieve_with_empty_query():
    """Test that retrieve function handles empty queries properly"""
    with pytest.raises(ValueError):
        retrieve("")


def test_retrieve_with_whitespace_query():
    """Test that retrieve function handles whitespace-only queries properly"""
    with pytest.raises(ValueError):
        retrieve("   ")


@patch('retrieve.embed_query')
@patch('retrieve.search_qdrant')
def test_retrieve_with_mocked_dependencies(mock_search, mock_embed):
    """Test retrieve function with mocked dependencies"""
    # Mock the embedding function
    mock_embed.return_value = [0.1, 0.2, 0.3]

    # Mock the search function
    mock_results = [
        {
            'id': 'test-id-1',
            'text': 'This is a test result',
            'source_url': 'http://example.com',
            'similarity_score': 0.8,
            'metadata': {'chunk_index': 0},
            'embedding_model': 'test-model'
        }
    ]
    mock_search.return_value = mock_results

    # Test retrieve function
    results = retrieve("test query", top_k=1)

    # Verify the results
    assert len(results) == 1
    assert results[0]['text'] == 'This is a test result'
    assert results[0]['similarity_score'] == 0.8

    # Verify that the functions were called
    mock_embed.assert_called_once_with("test query")
    mock_search.assert_called_once_with([0.1, 0.2, 0.3], 1)


@patch('retrieve.embed_query')
@patch('retrieve.search_qdrant')
def test_retrieve_with_no_match_scenario(mock_search, mock_embed):
    """Test 'no match' scenario where search returns no results"""
    # Mock the embedding function
    mock_embed.return_value = [0.1, 0.2, 0.3]

    # Mock the search function to return empty results
    mock_search.return_value = []

    # Test retrieve function
    results = retrieve("unusual random query that should not match anything", top_k=5)

    # Verify the results
    assert len(results) == 0

    # Verify that the functions were called
    mock_embed.assert_called_once_with("unusual random query that should not match anything")
    mock_search.assert_called_once_with([0.1, 0.2, 0.3], 5)


@patch('retrieve.embed_query')
@patch('retrieve.search_qdrant')
def test_retrieve_with_low_similarity_filtering(mock_search, mock_embed):
    """Test that results with low similarity scores are filtered out"""
    # Mock the embedding function
    mock_embed.return_value = [0.1, 0.2, 0.3]

    # Mock the search function to return results with low similarity scores
    mock_results = [
        {
            'id': 'test-id-1',
            'text': 'Low similarity result',
            'source_url': 'http://example.com',
            'similarity_score': 0.1,  # Below default threshold of 0.3
            'metadata': {'chunk_index': 0},
            'embedding_model': 'test-model'
        },
        {
            'id': 'test-id-2',
            'text': 'High similarity result',
            'source_url': 'http://example.com',
            'similarity_score': 0.8,  # Above default threshold
            'metadata': {'chunk_index': 1},
            'embedding_model': 'test-model'
        }
    ]
    mock_search.return_value = mock_results

    # Test retrieve function
    results = retrieve("test query", top_k=5, similarity_threshold=0.3)

    # Verify that only the high similarity result is returned
    assert len(results) == 1
    assert results[0]['similarity_score'] == 0.8
    assert results[0]['text'] == 'High similarity result'

    # Verify that the functions were called
    mock_embed.assert_called_once_with("test query")
    mock_search.assert_called_once_with([0.1, 0.2, 0.3], 5)


def test_retrieve_with_validation():
    """Test retrieve_with_validation function"""
    with pytest.raises(ValueError):
        # Test with empty query
        retrieve_with_validation("")


@patch('retrieve.retrieve')
def test_retrieve_with_validation_calls_retrieve(mock_retrieve):
    """Test that retrieve_with_validation calls the retrieve function"""
    mock_retrieve.return_value = [
        {
            'id': 'test-id',
            'text': 'Test result',
            'source_url': 'http://example.com',
            'similarity_score': 0.8,
            'metadata': {'chunk_index': 0},
            'embedding_model': 'test-model'
        }
    ]

    # Test retrieve_with_validation function
    results = retrieve_with_validation("test query", top_k=1)

    # Verify the results
    assert len(results) == 1
    assert results[0]['text'] == 'Test result'

    # Verify that the retrieve function was called
    mock_retrieve.assert_called_once_with("test query", 1)


@patch('retrieve.embed_query')
@patch('retrieve.search_qdrant')
def test_exact_match_scenario(mock_search, mock_embed):
    """Test 'exact match' scenario where search returns high similarity results"""
    # Mock the embedding function
    mock_embed.return_value = [0.5, 0.6, 0.7]

    # Mock the search function to return results with high similarity scores
    mock_results = [
        {
            'id': 'exact-match-id',
            'text': 'This is the exact content we are looking for',
            'source_url': 'http://example.com/exact-match',
            'similarity_score': 0.95,  # High similarity score
            'metadata': {'chunk_index': 0},
            'embedding_model': 'embed-english-v3.0'
        },
        {
            'id': 'partial-match-id',
            'text': 'This is partially related content',
            'source_url': 'http://example.com/partial-match',
            'similarity_score': 0.75,  # Good similarity score
            'metadata': {'chunk_index': 1},
            'embedding_model': 'embed-english-v3.0'
        }
    ]
    mock_search.return_value = mock_results

    # Test retrieve function with a query that should match the content
    results = retrieve("exact content", top_k=2)

    # Verify the results
    assert len(results) == 2
    assert results[0]['similarity_score'] == 0.95
    assert "exact" in results[0]['text'].lower()

    # Verify that the functions were called
    mock_embed.assert_called_once_with("exact content")
    mock_search.assert_called_once_with([0.5, 0.6, 0.7], 2)


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__])