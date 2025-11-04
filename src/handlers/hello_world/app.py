"""
Simple Hello World Lambda function handler.
"""
import json
from typing import Dict, Any
from custom_utils import display_something


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler function that returns a simple hello world message.

    Args:
        event: Lambda event object containing request data
        context: Lambda context object

    Returns:
        Dict containing statusCode, headers, and body with hello message
    """
    print(f"Received event: {json.dumps(event)}")
    
    # Call the layer function
    layer_message = display_something()
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({
            "message": "Hello from LocalStack Lambda!",
            "function": "hello-world-function",
            "layer_message": layer_message,
            "request_id": context.request_id if hasattr(context, 'request_id') else 'N/A'
        })
    }
