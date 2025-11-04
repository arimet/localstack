#!/bin/bash
# Configure AWS CLI to use LocalStack

echo "Configuring AWS CLI for LocalStack..."

# Set LocalStack profile
aws configure set aws_access_key_id test --profile localstack
aws configure set aws_secret_access_key test --profile localstack
aws configure set region us-east-1 --profile localstack
aws configure set output json --profile localstack

# Set endpoint URL for LocalStack
aws configure set endpoint_url http://localhost:4566 --profile localstack

echo "LocalStack profile configured!"
echo "Use: aws --profile localstack <command>"
