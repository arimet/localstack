"""
Shared utilities for Lambda functions.

This module provides reusable functions that can be shared across
multiple Lambda functions using Lambda Layers.
"""
import json
from typing import Dict, Any


def format_response(status_code: int, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format a standardized API Gateway response.
    
    Args:
        status_code: HTTP status code (e.g., 200, 400, 500)
        data: Response payload to be serialized as JSON
    
    Returns:
        Formatted response for API Gateway
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(data)
    }


def get_greeting(name: str) -> str:
    """
    Generate a personalized greeting message.
    
    Args:
        name: The name of the person to greet
    
    Returns:
        Personalized greeting string
    """
    return f"Hello, {name}! Welcome to our serverless application built with LocalStack."
