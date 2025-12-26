import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the backend directory to the path so we can import main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import main


def test_embed_data_function_exists():
    """Test that the embed_data function exists"""
    assert hasattr(main, 'embed_data'), "embed_data function should exist in main module"
    assert callable(main.embed_data), "embed_data should be callable"


def test_embed_data_returns_list():
    """Test that embed_data returns a list"""
    # This will be updated after the function is implemented
    pass


def test_embed_data_with_empty_list():
    """Test embed_data with empty input list"""
    result = main.embed_data([])
    assert result == []