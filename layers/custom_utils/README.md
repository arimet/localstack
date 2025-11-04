# Custom Utils Lambda Layer

This Lambda layer provides custom utility functions for use across all Lambda functions in the application.

## Structure

```
layers/custom_utils/
├── python/
│   └── custom_utils/
│       ├── __init__.py
│       └── display.py
└── README.md
```

## Functions

### `display_something()`

Prints and returns the message: "This message comes from a package (via a Lambda Layer)"

**Usage:**

```python
from custom_utils import display_something

def lambda_handler(event, context):
    message = display_something()
    # message will contain: "This message comes from a package (via a Lambda Layer)"
    # The function also prints the message to CloudWatch logs
```

## Layer Structure

Lambda layers for Python must follow this directory structure:
- `python/` - The root directory for Python dependencies
- `custom_utils/` - The module name that can be imported

## Deployment

The layer is automatically deployed when you run:

```bash
make deploy
```

## Viewing Layers

To list all deployed Lambda layers:

```bash
make list-layers
```

## Notes

- The layer is compatible with Python 3.10, 3.11, and 3.12
- All Lambda functions in this stack automatically have access to this layer
- The layer is included via the SAM template using `!Ref CustomUtilsLayer`
