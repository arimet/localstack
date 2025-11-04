"""
User greeting Lambda function demonstrating Lambda Layers integration.

This example shows how to build a simple yet professional Lambda function
that uses custom utilities from a Lambda Layer.
"""
import json
from typing import Dict, Any
from custom_utils import format_response, get_greeting


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler that returns a personalized greeting.

    Args:
        event: Lambda event object (contains queryStringParameters)
        context: Lambda context object

    Returns:
        API Gateway response with greeting message
    """
    # Extract the name from query parameters (defaults to "World")
    query_params = event.get("queryStringParameters") or {}
    name = query_params.get("name", "World")
    
    # Use the custom layer function to generate greeting
    greeting_message = get_greeting(name)
    
    # Prepare response data
    response_data = {
        "message": greeting_message,
        "user": name,
        "source": "Lambda Layer Integration Example",
        "request_id": context.request_id
    }
    
    # Use custom layer utility to format the response
    return format_response(200, response_data)
