.PHONY: help install build deploy invoke test clean start-localstack stop-localstack status

# Default target
.DEFAULT_GOAL := help

# Variables
STACK_NAME = localstack-sam-app
AWS_REGION = eu-west-1
LOCALSTACK_ENDPOINT = http://localhost:4566

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies with Poetry
	@echo "Installing dependencies..."
	poetry install
	@echo "Installation complete!"

start-localstack: ## Start LocalStack with Docker Compose
	@echo "Starting LocalStack..."
	docker compose up -d
	@echo "Waiting for LocalStack to be ready..."
	@sleep 10
	@curl -s $(LOCALSTACK_ENDPOINT)/_localstack/health | grep -q "running" && echo "LocalStack is ready!" || echo "LocalStack might not be ready yet"

stop-localstack: ## Stop LocalStack
	@echo "Stopping LocalStack..."
	docker compose down

status: ## Check LocalStack status
	@echo "Checking LocalStack status..."
	@curl -s $(LOCALSTACK_ENDPOINT)/_localstack/health | python3 -m json.tool || echo "LocalStack is not running"

build: ## Build SAM application
	@echo "Building SAM application..."
	poetry run samlocal build

deploy: build ## Deploy to LocalStack
	@echo "Deploying to LocalStack..."
	poetry run samlocal deploy \
		--config-env localstack \
		--no-confirm-changeset \
		--no-fail-on-empty-changeset \
		--resolve-s3

list-functions: ## List all deployed Lambda functions
	@echo "Listing Lambda functions..."
	@poetry run awslocal lambda list-functions --region $(AWS_REGION) --query 'Functions[*].[FunctionName,Runtime,LastModified]' --output table

list-layers: ## List all deployed Lambda layers
	@echo "Listing Lambda layers..."
	@poetry run awslocal lambda list-layers --region $(AWS_REGION) --query 'Layers[*].[LayerName,LatestMatchingVersion.LayerVersionArn]' --output table

invoke-hello: ## Invoke Hello World function
	@echo "Invoking Hello World function..."
	@poetry run awslocal lambda invoke \
		--function-name hello-world-function \
		--region $(AWS_REGION) \
		--cli-binary-format raw-in-base64-out \
		--log-type Tail \
		--query 'LogResult' \
		--output text /tmp/response.json | base64 -d
	@echo "\nResponse:"
	@cat /tmp/response.json | python3 -m json.tool

invoke-hello-with-name: ## Invoke Hello World function with name parameter (usage: make invoke-hello-with-name NAME=Alice)
	@echo "Invoking Hello World function with name=$(NAME)..."
	@echo '{"queryStringParameters": {"name": "$(NAME)"}}' > /tmp/event.json
	@poetry run awslocal lambda invoke \
		--function-name hello-world-function \
		--region $(AWS_REGION) \
		--cli-binary-format raw-in-base64-out \
		--payload file:///tmp/event.json \
		--log-type Tail \
		--query 'LogResult' \
		--output text /tmp/response.json | base64 -d
	@echo "\nResponse:"
	@cat /tmp/response.json | python3 -m json.tool
	@rm /tmp/event.json

invoke-hello-custom: ## Invoke with custom event (usage: make invoke-hello-custom EVENT='{"queryStringParameters":{"name":"Bob"}}')
	@echo "Invoking Hello World function with custom event..."
	@echo '$(EVENT)' > /tmp/event.json
	@poetry run awslocal lambda invoke \
		--function-name hello-world-function \
		--region $(AWS_REGION) \
		--cli-binary-format raw-in-base64-out \
		--payload file:///tmp/event.json \
		--log-type Tail \
		--query 'LogResult' \
		--output text /tmp/response.json | base64 -d
	@echo "\nResponse:"
	@cat /tmp/response.json | python3 -m json.tool
	@rm /tmp/event.json

test: ## Run tests (placeholder)
	@echo "Running tests..."
	poetry run pytest tests/ -v

clean: ## Clean build artifacts
	@echo "Cleaning build artifacts..."
	rm -rf .aws-sam
	rm -rf .pytest_cache
	rm -rf **/__pycache__
	rm -rf **/.pytest_cache
	rm -f /tmp/response.json
	docker compose down -v

full-deploy: start-localstack deploy list-functions ## Start LocalStack and deploy everything
	@echo "Full deployment complete!"

quick-test: invoke-hello invoke-hello-with-name ## Quick test all functions
	@echo "All functions tested!"
