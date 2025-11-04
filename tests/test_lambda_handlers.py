"""
Unit tests for Lambda handler functions.
"""
import json
import pytest
from typing import Any, Dict


class MockContext:
    """Mock Lambda context for testing."""
    request_id = "test-request-id"
    function_name = "test-function"
    function_version = "$LATEST"
    invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test-function"
    memory_limit_in_mb = 256
    aws_request_id = "test-request-id"


@pytest.fixture
def mock_context() -> MockContext:
    """Fixture providing a mock Lambda context."""
    return MockContext()


class TestHelloWorldHandler:
    """Tests for the Hello World Lambda handler."""

    def test_lambda_handler_returns_200(self, mock_context: MockContext) -> None:
        """Test that the handler returns a 200 status code."""
        from src.handlers.hello_world.app import lambda_handler

        event: Dict[str, Any] = {}
        response = lambda_handler(event, mock_context)

        assert response["statusCode"] == 200

    def test_lambda_handler_returns_json(self, mock_context: MockContext) -> None:
        """Test that the handler returns valid JSON."""
        from src.handlers.hello_world.app import lambda_handler

        event: Dict[str, Any] = {}
        response = lambda_handler(event, mock_context)

        body = json.loads(response["body"])
        assert "message" in body
        assert body["message"] == "Hello from LocalStack Lambda!"


class TestHelloUserHandler:
    """Tests for the Hello User Lambda handler."""

    def test_lambda_handler_with_user_parameter(self, mock_context: MockContext) -> None:
        """Test handler with user path parameter."""
        from src.handlers.hello_user.app import lambda_handler

        event: Dict[str, Any] = {
            "pathParameters": {"user": "TestUser"}
        }
        response = lambda_handler(event, mock_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["message"] == "Hello, TestUser!"
        assert body["user"] == "TestUser"

    def test_lambda_handler_without_user_parameter(self, mock_context: MockContext) -> None:
        """Test handler defaults to Guest when no user parameter."""
        from src.handlers.hello_user.app import lambda_handler

        event: Dict[str, Any] = {}
        response = lambda_handler(event, mock_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["message"] == "Hello, Guest!"


class TestHelloPostHandler:
    """Tests for the Hello POST Lambda handler."""

    def test_lambda_handler_with_valid_json(self, mock_context: MockContext) -> None:
        """Test handler with valid JSON body."""
        from src.handlers.hello_post.app import lambda_handler

        event: Dict[str, Any] = {
            "body": json.dumps({"name": "TestUser", "message": "Hello World"})
        }
        response = lambda_handler(event, mock_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["message"] == "Hello, TestUser!"
        assert body["received_message"] == "Hello World"

    def test_lambda_handler_with_invalid_json(self, mock_context: MockContext) -> None:
        """Test handler with invalid JSON body."""
        from src.handlers.hello_post.app import lambda_handler

        event: Dict[str, Any] = {
            "body": "invalid json"
        }
        response = lambda_handler(event, mock_context)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "error" in body

    def test_lambda_handler_without_body(self, mock_context: MockContext) -> None:
        """Test handler defaults when no body provided."""
        from src.handlers.hello_post.app import lambda_handler

        event: Dict[str, Any] = {}
        response = lambda_handler(event, mock_context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["message"] == "Hello, Guest!"
