import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the backend directory to the path so we can import main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import main


def test_get_urls_function_exists():
    """Test that the get_urls function exists"""
    assert hasattr(main, 'get_urls'), "get_urls function should exist in main module"
    assert callable(main.get_urls), "get_urls should be callable"


def test_get_urls_returns_list():
    """Test that get_urls returns a list"""
    # This will be updated after the function is implemented
    pass


def test_crawl_single_url_function_exists():
    """Test that the crawl_single_url function exists"""
    assert hasattr(main, 'crawl_single_url'), "crawl_single_url function should exist in main module"
    assert callable(main.crawl_single_url), "crawl_single_url should be callable"


def test_crawl_single_url_returns_dict():
    """Test that crawl_single_url returns a dictionary"""
    # This will be updated after the function is implemented
    pass


def test_crawl_single_url_with_invalid_url():
    """Test crawling with an invalid URL"""
    # Testing with an actual invalid URL that we know will fail
    result = main.crawl_single_url("http://this-url-definitely-does-not-exist-12345.com")
    # The result might be success or failure depending on DNS behavior, so we just check it returns a dict
    assert isinstance(result, dict)
    assert 'url' in result
    assert 'status' in result