"""
Hello User Lambda function handler with path parameter.
"""
import json
from typing import Dict, Any


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler function that returns a personalized hello message.

    Args:
        event: Lambda event object containing request data
        context: Lambda context object

    Returns:
        Dict containing statusCode, headers, and body with personalized message
    """
    print(f"Received event: {json.dumps(event)}")
    
    # Extract user from path parameters
    path_parameters = event.get("pathParameters", {}) or {}
    user = path_parameters.get("user", "Guest")
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({
            "message": f"Hello, {user}!",
            "function": "hello-user-function",
            "user": user,
            "request_id": context.request_id if hasattr(context, 'request_id') else 'N/A'
        })
    }
