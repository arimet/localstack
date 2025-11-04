# LocalStack SAM Lambda Project

A complete AWS SAM project with Python Lambda functions running on LocalStack, managed with Poetry and Docker.

## 🚀 Features

- **AWS SAM**: Infrastructure as Code for serverless applications
- **LocalStack**: Local AWS cloud emulator for development
- **Python 3.11**: Modern Python with type hints
- **Poetry**: Dependency management and packaging
- **Docker**: Containerized LocalStack environment
- **Multiple Lambda Functions**: Examples of GET and POST endpoints

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.12+
- Poetry
- AWS CLI
- AWS SAM CLI
- awslocal (LocalStack AWS CLI wrapper)
- samlocal (LocalStack SAM CLI wrapper)

### Installation Commands

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install AWS CLI
pip install awscli

# Install AWS SAM CLI (via Poetry dev dependencies or globally)
pip install aws-sam-cli

# Install LocalStack wrappers
pip install awscli-local[ver1]
```

## 🏗️ Project Structure

```
.
├── docker-compose.yml          # LocalStack container configuration
├── template.yaml               # SAM template defining Lambda functions
├── samconfig.toml             # SAM configuration file
├── pyproject.toml             # Poetry dependencies and project config
├── Makefile                   # Convenient commands for development
├── README.md                  # This file
├── layers/
│   └── custom_utils/          # Lambda layer with custom utilities
│       ├── python/
│       │   └── custom_utils/
│       │       ├── __init__.py
│       │       └── display.py
│       └── README.md
└── src/
    └── handlers/
        ├── hello_world/       # Simple GET endpoint
        │   └── app.py
        ├── hello_user/        # GET with path parameter
        │   └── app.py
        └── hello_post/        # POST endpoint
            └── app.py
```

## 🛠️ Setup

### 1. Install Dependencies

```bash
make install
```

This will install all Python dependencies using Poetry.

### 2. Start LocalStack

```bash
make start-localstack
```

This starts LocalStack in a Docker container with all required AWS services.

### 3. Build and Deploy

```bash
make build
make deploy
```

Or use the combined command:

```bash
make full-deploy
```

## 📝 Lambda Functions

All Lambda functions have access to the **custom-utils-layer** which provides shared utilities.

### 1. Hello World Function
- **Endpoint**: GET `/hello`
- **Description**: Simple hello world response
- **Layer Functions**: Uses `display_something()` from custom_utils

### 2. Hello User Function
- **Endpoint**: GET `/hello/{user}`
- **Description**: Personalized greeting with path parameter
- **Layer Functions**: Uses `display_something()` from custom_utils

### 3. Hello POST Function
- **Endpoint**: POST `/hello`
- **Description**: Processes JSON body with name and message
- **Layer Functions**: Uses `display_something()` from custom_utils

## 📦 Lambda Layers

### Custom Utils Layer
Located in `layers/custom_utils/`, this layer provides shared functionality across all Lambda functions.

**Available Functions:**
- `display_something()`: Prints and returns "This message comes from a package (via a Lambda Layer)"

**Usage in Lambda:**
```python
from custom_utils import display_something

def lambda_handler(event, context):
    message = display_something()
    # Use the message in your response
```

See `layers/custom_utils/README.md` for more details.

## 🧪 Testing

### Check LocalStack Status

```bash
make status
```

### List Deployed Functions

```bash
make list-functions
```

### List Deployed Layers

```bash
make list-layers
```

### Invoke Lambda Functions

```bash
# Invoke Hello World
make invoke-hello

# Invoke Hello User
make invoke-hello-user

# Invoke Hello POST
make invoke-hello-post

# Test all functions
make quick-test
```

### Direct AWS CLI Invocation

```bash
# Hello World
aws --endpoint-url=http://localhost:4566 lambda invoke \
  --function-name hello-world-function \
  --region eu-west-1 \
  response.json

# Hello User with path parameter
aws --endpoint-url=http://localhost:4566 lambda invoke \
  --function-name hello-user-function \
  --region eu-west-1 \
  --payload '{"pathParameters":{"user":"John"}}' \
  response.json

# Hello POST with JSON body
aws --endpoint-url=http://localhost:4566 lambda invoke \
  --function-name hello-post-function \
  --region eu-west-1 \
  --payload '{"body":"{\"name\":\"Jane\",\"message\":\"Hi there\"}"}' \
  response.json
```

## 🔧 Available Make Commands

Run `make help` to see all available commands:

- `make install` - Install dependencies with Poetry
- `make start-localstack` - Start LocalStack container
- `make stop-localstack` - Stop LocalStack container
- `make status` - Check LocalStack health status
- `make build` - Build SAM application
- `make deploy` - Deploy to LocalStack
- `make list-functions` - List all Lambda functions
- `make list-layers` - List all Lambda layers
- `make invoke-hello` - Test Hello World function
- `make invoke-hello-user` - Test Hello User function
- `make invoke-hello-post` - Test Hello POST function
- `make test` - Run pytest tests
- `make clean` - Clean build artifacts
- `make full-deploy` - Start LocalStack and deploy
- `make quick-test` - Test all functions

## 🐳 Docker Configuration

LocalStack is configured with:
- **Port 4566**: Main LocalStack gateway
- **Services**: Lambda, API Gateway, S3, CloudFormation, STS, IAM, CloudWatch Logs
- **Executor**: docker-reuse (faster Lambda execution)
- **Debug Mode**: Enabled for detailed logs

## 📦 Poetry Configuration

Dependencies are managed in `pyproject.toml`:
- **Runtime**: boto3
- **Development**: pytest, black, mypy, ruff, aws-sam-cli

## 🔄 Development Workflow

1. Make changes to Lambda function code in `src/handlers/`
2. Build: `make build`
3. Deploy: `make deploy`
4. Test: `make invoke-hello` (or other invoke commands)
5. View logs in terminal

## 🧹 Cleanup

```bash
# Stop LocalStack and remove containers
make stop-localstack

# Clean build artifacts and containers
make clean
```

## 📚 Additional Resources

- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
- [LocalStack Documentation](https://docs.localstack.cloud/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [AWS Lambda Python Documentation](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.
