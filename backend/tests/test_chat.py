"""
Tests for chat endpoints.
"""

import pytest
from unittest.mock import Mock, patch


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_chat_endpoint_success(client, sample_chat_request):
    """Test successful chat request."""
    with patch("app.services.chat_service.ChatService.generate_response") as mock_generate:
        mock_generate.return_value = "Succulents need minimal watering..."

        response = client.post("/api/v1/chat", json=sample_chat_request)
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data
        assert data["reply"] == "Succulents need minimal watering..."


def test_chat_endpoint_empty_message(client):
    """Test chat endpoint with empty message."""
    response = client.post("/api/v1/chat", json={"message": ""})
    assert response.status_code == 422  # Validation error


def test_chat_endpoint_long_message(client):
    """Test chat endpoint with message exceeding max length."""
    long_message = "a" * 1001  # Exceeds max_length=1000
    response = client.post("/api/v1/chat", json={"message": long_message})
    assert response.status_code == 422  # Validation error

