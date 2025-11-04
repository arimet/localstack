"""
Hello POST Lambda function handler with request body.
"""
import json
from typing import Dict, Any


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler function that processes POST requests.

    Args:
        event: Lambda event object containing request data
        context: Lambda context object

    Returns:
        Dict containing statusCode, headers, and body with response
    """
    print(f"Received event: {json.dumps(event)}")
    
    # Parse request body
    try:
        body = json.loads(event.get("body", "{}"))
        name = body.get("name", "Guest")
        message = body.get("message", "")
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({
                "error": "Invalid JSON in request body"
            })
        }
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({
            "message": f"Hello, {name}!",
            "function": "hello-post-function",
            "received_message": message,
            "request_id": context.request_id if hasattr(context, 'request_id') else 'N/A'
        })
    }
