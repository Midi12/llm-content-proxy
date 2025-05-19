# Google Cloud Functions Setup

This guide covers how to deploy the Website Content Extractor as a Google Cloud Function.

## Prerequisites

- Python 3.7 or higher
- Google Cloud SDK (gcloud) installed and configured
- A Google Cloud Platform account with billing enabled
- Basic familiarity with Google Cloud Platform

## Installation

1. Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/Midi12/llm-content-proxy.git
cd llm-content-proxy
```

2. Install the package with GCP dependencies:

```bash
pip install -e ".[gcp]"
```

## Local Testing

You can test the cloud function locally before deployment:

```bash
cd llm-content-proxy/impl/gcp
python main.py
```

This will run a small Flask app on port 8080 that simulates the cloud function. You can test it with:

```bash
curl "http://localhost:8080/?link=https://example.com"
```

## Deployment

### Method 1: Using the Google Cloud Console

1. Go to the Google Cloud Console: https://console.cloud.google.com/
2. Navigate to Cloud Functions
3. Click "Create Function"
4. Configure the function:
   - Name: `llm-content-proxy`
   - Region: Choose your preferred region
   - Trigger: HTTP
   - Authentication: Allow unauthenticated invocations (or secure as needed)
   - Runtime: Python 3.9
5. In the next step, upload the source code or use inline editor:
   - Entry point: `extract_content`
   - Runtime environment variables: (none required)
   - Copy the code from `llm-content-proxy/impl/gcp/main.py`
   - Create a `requirements.txt` file with the contents from `llm-content-proxy/impl/gcp/requirements.txt`
   - Make sure to include the core extractor code as well
6. Click "Deploy"

### Method 2: Using the gcloud CLI

For streamlined deployment, you can use the following commands:

1. Prepare the deployment package:

```bash
# Create a temp directory for deployment
mkdir -p /tmp/function-deploy
cd /tmp/function-deploy

# Copy the core extractor code
mkdir -p llm-content-proxy/core
cp /path/to/llm-content-proxy/core/extractor.py llm-content-proxy/core/
cp /path/to/llm-content-proxy/core/__init__.py llm-content-proxy/core/

# Copy the cloud function code
cp /path/to/llm-content-proxy/impl/gcp/main.py .
cp /path/to/llm-content-proxy/impl/gcp/requirements.txt .
```

2. Deploy the function:

```bash
# Deploy the function
gcloud functions deploy llm-content-proxy \
  --gen2 \
  --runtime=python310 \
  --region=us-central1 \
  --source=. \
  --entry-point=extract_content \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=60s \
  --memory=512MB
```

3. Get the function URL:

```bash
gcloud functions describe llm-content-proxy \
  --region=us-central1 \
  --format="value(serviceConfig.uri)"
```

### Method 3: Using the Deployment Script

For convenience, a deployment script is provided:

1. Navigate to the GCP cloud function directory:

```bash
cd llm-content-proxy/impl/gcp
```

2. Create a deployment script:

```bash
#!/bin/bash

# Set your GCP project ID
PROJECT_ID="your-project-id"

# Set the region
REGION="us-central1"

# Set function name
FUNCTION_NAME="llm-content-proxy"

# Create temporary deployment directory
TEMP_DIR=$(mktemp -d)
echo "Created temporary directory: $TEMP_DIR"

# Copy necessary files
mkdir -p $TEMP_DIR/llm-content-proxy/core
cp ../../../llm-content-proxy/core/extractor.py $TEMP_DIR/llm-content-proxy/core/
cp ../../../llm-content-proxy/core/__init__.py $TEMP_DIR/llm-content-proxy/core/
cp main.py $TEMP_DIR/
cp requirements.txt $TEMP_DIR/

# Change to temporary directory
cd $TEMP_DIR

# Deploy the function
gcloud functions deploy $FUNCTION_NAME \
  --gen2 \
  --runtime=python310 \
  --region=$REGION \
  --source=. \
  --entry-point=extract_content \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=60s \
  --memory=512MB

# Get the function URL
FUNCTION_URL=$(gcloud functions describe $FUNCTION_NAME --region=$REGION --format="value(serviceConfig.uri)")
echo "Function deployed successfully!"
echo "You can access it at: $FUNCTION_URL?link=https://example.com"

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
GET https://REGION-PROJECT_ID.cloudfunctions.net/llm-content-proxy?link=https://example.com
```

You can test it using `curl`:

```bash
curl "https://REGION-PROJECT_ID.cloudfunctions.net/llm-content-proxy?link=https://example.com"
```

## Production Considerations

For production use, consider:

1. **Authentication**: Add authentication to protect your function if needed
2. **Rate Limiting**: Implement a rate limiter to prevent abuse
3. **Caching**: Add caching to improve performance and reduce costs
4. **Monitoring**: Set up Cloud Monitoring to track usage and errors
5. **Error Logging**: Configure detailed error logging
6. **Timeout and Memory**: Adjust timeout and memory based on your needs

## Cost Optimization

Google Cloud Functions has a generous free tier, but costs can add up with high usage:

- Use the smallest memory setting that works for your function (128MB might be sufficient)
- Implement caching to reduce function invocations
- Configure concurrency limits to control costs

## Troubleshooting

- If deployment fails, check the error message in the Cloud Console
- If you get a "Permission denied" error, ensure your gcloud CLI is properly authenticated
- If the function times out, increase the timeout setting
- For other issues, check the Cloud Functions logs in the Google Cloud Console