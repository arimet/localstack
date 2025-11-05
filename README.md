# LocalStack SAM Lambda Project

A complete AWS SAM project with Python Lambda functions running on LocalStack, managed with Poetry and Docker.

## 🚀 Features

- **AWS SAM**: Infrastructure as Code for serverless applications
- **LocalStack**: Local AWS cloud emulator for development
- **Python 3.12**: Modern Python with type hints
- **Poetry**: Dependency management and packaging
- **Docker**: Containerized LocalStack environment
- **Multiple Lambda Functions**: Examples of GET and POST endpoints

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.12+
- Poetry
- AWS CLI
- AWS SAM CLI

## 🛠️ Setup

```bash
make install          # Install dependencies
make start-localstack # Start LocalStack
make full-deploy      # Build and deploy
```

## 📝 Lambda Functions

Lambda functions have access to the **custom-utils-layer** which provides shared utilities.

### 1. Hello World Function

- **Endpoint**: GET `/hello`
- **Description**: Simple hello world response

```bash
make invoke-hello-with-name NAME="Anthony"
```

## 📦 Lambda Layers

### Custom Utils Layer

Located in `layers/custom_utils/`, this layer provides shared functionality across all Lambda functions.

```python
from custom_utils import get_greeting

def lambda_handler(event, context):
    message = get_greeting()
```

## 🧹 Cleanup

```bash
make stop-localstack  # Stop LocalStack
make clean            # Clean build artifacts
```
