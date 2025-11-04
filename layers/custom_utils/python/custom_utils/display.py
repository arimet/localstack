"""
Display utilities module.
"""


def display_something() -> str:
    """
    Display and return a specific message.
    
    Returns:
        str: The message "This message comes from a package (via a Lambda Layer)"
    """
    message = "This message comes from a package (via a Lambda Layer)"
    print(message)
    return message
