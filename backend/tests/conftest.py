"""
Pytest configuration and shared fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from app import create_app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def sample_chat_request():
    """Sample chat request for testing."""
    return {
        "message": "How do I care for a succulent?",
        "stream": False
    }

