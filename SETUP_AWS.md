# AWS Lambda Setup

This guide covers how to deploy the Website Content Extractor as an AWS Lambda function with API Gateway.

## Prerequisites

- Python 3.7 or higher
- AWS CLI installed and configured
- AWS SAM CLI installed (for easier deployments)
- An AWS account
- Basic familiarity with AWS Lambda and API Gateway

## Installation

1. Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/Midi12/llm-content-proxy.git
cd llm-content-proxy
```

2. Install the package with AWS dependencies:

```bash
pip install -e ".[aws]"
```

## Local Testing

You can test the Lambda function locally before deployment:

```bash
cd llm-content-proxy/impl/aws
python lambda_function.py
```

This will run a test event that simulates an API Gateway request and output the result.

## Deployment

### Method 1: Using AWS SAM

The AWS Serverless Application Model (SAM) makes it easy to deploy Lambda functions:

1. Navigate to the AWS cloud function directory:

```bash
cd llm-content-proxy/impl/aws
```

2. Build the SAM application:

```bash
# Create a temporary deployment directory
mkdir -p build
cd build

# Copy necessary files
mkdir -p llm-content-proxy/core
cp ../../../llm-content-proxy/core/extractor.py llm-content-proxy/core/
cp ../../../llm-content-proxy/core/__init__.py llm-content-proxy/core/
cp ../lambda_function.py .
cp ../requirements.txt .
cp ../template.yaml .

# Install dependencies in a directory for deployment
pip install -r requirements.txt -t .

# Package the application
sam package \
    --template-file template.yaml \
    --output-template-file packaged.yaml \
    --s3-bucket your-s3-bucket-name

# Deploy the application
sam deploy \
    --template-file packaged.yaml \
    --stack-name llm-content-proxy \
    --capabilities CAPABILITY_IAM
```

3. Get the API Gateway endpoint URL:

```bash
aws cloudformation describe-stacks \
    --stack-name llm-content-proxy \
    --query 'Stacks[0].Outputs[?OutputKey==`ContentExtractorApi`].OutputValue' \
    --output text
```

### Method 2: Using the AWS Console

1. Create a deployment package:

```bash
# Create a temporary deployment directory
mkdir -p /tmp/lambda-deploy
cd /tmp/lambda-deploy

# Copy necessary files
mkdir -p llm-content-proxy/core
cp /path/to/llm-content-proxy/core/extractor.py llm-content-proxy/core/
cp /path/to/llm-content-proxy/core/__init__.py llm-content-proxy/core/
cp /path/to/llm-content-proxy/impl/aws/lambda_function.py .
cp /path/to/llm-content-proxy/impl/aws/requirements.txt .

# Install dependencies in the deployment directory
pip install -r requirements.txt -t .

# Create a zip file
zip -r lambda_package.zip .
```

2. Go to the AWS Lambda Console:
   - Create a new function
   - Choose "Author from scratch"
   - Name: `llm-content-proxy`
   - Runtime: Python 3.9
   - Architecture: x86_64
   - Permissions: Create a new role with basic Lambda permissions

3. Upload the zip file:
   - In the function code section, upload the `lambda_package.zip` file
   - Set the handler to: `lambda_function.lambda_handler`

4. Configure the function:
   - Memory: 512 MB
   - Timeout: 30 seconds

5. Add an API Gateway trigger:
   - Create a new API Gateway
   - REST API
   - Security: Open (or configure as needed)

### Method 3: Using the Deployment Script

For convenience, a deployment script is provided:

1. Navigate to the AWS Lambda directory:

```bash
cd llm-content-proxy/impl/aws
```

2. Create a deployment script:

```bash
#!/bin/bash

# Set variables
STACK_NAME="llm-content-proxy"
S3_BUCKET="your-s3-bucket-name"

# Create temporary deployment directory
TEMP_DIR=$(mktemp -d)
echo "Created temporary directory: $TEMP_DIR"

# Copy necessary files
mkdir -p $TEMP_DIR/llm-content-proxy/core
cp ../../../llm-content-proxy/core/extractor.py $TEMP_DIR/llm-content-proxy/core/
cp ../../../llm-content-proxy/core/__init__.py $TEMP_DIR/llm-content-proxy/core/
cp lambda_function.py $TEMP_DIR/
cp requirements.txt $TEMP_DIR/
cp template.yaml $TEMP_DIR/

# Change to temporary directory
cd $TEMP_DIR

# Install dependencies in the deployment directory
pip install -r requirements.txt -t .

# Package the application
sam package \
    --template-file template.yaml \
    --output-template-file packaged.yaml \
    --s3-bucket $S3_BUCKET

# Deploy the application
sam deploy \
    --template-file packaged.yaml \
    --stack-name $STACK_NAME \
    --capabilities CAPABILITY_IAM

# Get the API Gateway endpoint URL
API_URL=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs[?OutputKey==`ContentExtractorApi`].OutputValue' \
    --output text)
echo "Function deployed successfully!"
echo "You can access it at: ${API_URL}?link=https://example.com"

# Clean up
cd -
rm -rf $TEMP_DIR
echo "Cleaned up temporary directory"
```

3. Make it executable and run it:

```bash
chmod +x deploy.sh
./deploy.sh
```

## Usage

Once deployed, you can access the function at:

```
GET https://API_ID.execute-api.REGION.amazonaws.com/Prod/?link=https://example.com
```

You can test it using `curl`:

```bash
curl "https://API_ID.execute-api.REGION.amazonaws.com/Prod/?link=https://example.com"
```

## Custom Domain (Optional)

For a cleaner URL, you can set up a custom domain:

1. In API Gateway, go to "Custom Domain Names"
2. Create a new domain with your registered domain
3. Set up the required certificates
4. Create a base path mapping to your API
5. Configure DNS with your domain provider

## Production Considerations

For production use, consider:

1. **Authentication**: Add authentication using API Gateway authorizers
2. **Rate Limiting**: Configure usage plans and API keys
3. **Caching**: Enable API Gateway caching
4. **Monitoring**: Set up CloudWatch alarms and dashboards
5. **Error Logging**: Configure detailed error logging
6. **Concurrency**: Configure provisioned concurrency for stable performance

## Cost Optimization

AWS Lambda and API Gateway have pay-per-use pricing:

- Lambda: $0.20 per million requests + $0.0000166667 per GB-second
- API Gateway: $3.50 per million requests

To optimize costs:

- Use the smallest memory setting that works for your function
- Implement caching to reduce function invocations
- Consider reserved concurrency for predictable workloads

## Troubleshooting

- If deployment fails, check the CloudFormation events
- If you get permission errors, check your IAM roles
- If the function returns errors, check the CloudWatch logs
- If API Gateway isn't working, check the integration configuration