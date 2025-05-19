# LLM Content Proxy

A Python package for extracting the main content from web pages. Can be used as a standalone server or deployed as a cloud function (GCP, AWS or Azure).

Primary purpose was to proxify blog articles content to LLM for summarizing or analysis.

## Features

- Extract the main textual content from web pages
- Remove unwanted elements like ads, navigation, headers, etc.
- Simple REST API to access this functionality
- Multiple deployment options:
  - Standalone FastAPI server
  - Google Cloud Function
  - AWS Lambda
  - Azure Functions

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/llm_content_proxy.git
cd llm_content_proxy

# Install the base package
pip install -e .

# For GCP development
pip install -e ".[gcp]"

# For AWS development
pip install -e ".[aws]"

# For AWS development
pip install -e ".[azure]"

# For development tools (testing, linting)
pip install -e ".[dev]"
```

## Usage

### As a Python Package

```python
from llm_content_proxy import ContentExtractor

# Create an extractor instance
extractor = ContentExtractor()

# Extract content from a URL
result = extractor.extract_from_url("https://example.com/article")

# Access the extracted content
print(f"Title: {result['title']}")
print(f"Content: {result['content']}")
print(f"Word count: {result['word_count']}")
```

### Running the Standalone Server

```bash
# Method 1: Using the command-line entry point
llm-content-proxy

# Method 2: Using Python directly
python -m server.app
```

Then access the API at: `http://localhost:8000/?link=https://example.com`

### Deployment Options

This package supports multiple deployment options:

1. **Standalone Server**: Run as a FastAPI application on your own server
2. **Google Cloud Functions**: Deploy as a serverless function on GCP
3. **AWS Lambda**: Deploy as a serverless function on AWS
4. **Azure Functions**: Deploy as a serverless function on Azure

See the setup documentation for each option:

- [Standalone Server Setup](SETUP_STANDALONE.md)
- [Google Cloud Functions Setup](SETUP_GCP.md)
- [AWS Lambda Setup](SETUP_AWS.md)
- [Azure Functions Setup](SETUP_AZURE.md)

## API Usage

Once deployed, you can access the API at:

```
GET /?link=https://example.com/article
```

The response will be a JSON object with the following structure:

```json
{
  "title": "Article Title",
  "content": "The main content of the article...",
  "url": "https://example.com/article",
  "word_count": 1234
}
```

## Example LLM Integration

To use this with an LLM, you can format your prompts like:

```
Summarize the following article from {url}:

{content}
```

## Configuration

The server listens on all interfaces (0.0.0.0) on port 8000 by default. You can modify this when running the server:

```python
from llm_content_proxy import run_server

# Run on a different host and port
run_server(host="127.0.0.1", port=5000)
```

## Requirements

- Python 3.7+
- Common requirements:
  - requests
  - beautifulsoup4
- Standalone server:
  - fastapi
  - uvicorn
  - pydantic
- GCP:
  - functions-framework
- AWS:
  - boto3 (for deployment)

## License

WTF