# Standalone Server Setup

This guide covers how to set up and run the Website Content Extractor as a standalone server.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- virtualenv (optional but recommended)

## Installation

1. Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/Midi12/llm-content-proxy.git
cd llm-content-proxy
```

2. Create and activate a virtual environment (optional but recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. Install the package:

```bash
pip install -e .
```

## Running the Server

### Method 1: Using the Command-Line Entry Point

After installation, you can run the server using the provided command-line entry point:

```bash
llm-content-proxy
```

This will start the server on `0.0.0.0:8000`.

### Method 2: Using Python Directly

You can also run the server directly using Python:

```bash
python -m server.app
```

### Method 3: Using Your Own Script

Create a custom script to run the server with specific settings:

```python
# server_script.py
from llm_content_proxy import run_server

if __name__ == "__main__":
    run_server(host="127.0.0.1", port=5000)
```

Then run it with:

```bash
python server_script.py
```

## Usage

Once the server is running, you can access the API endpoint:

```
GET http://localhost:8000/?link=https://example.com
```

You can test it using `curl`:

```bash
curl "http://localhost:8000/?link=https://example.com"
```

Or using any HTTP client.

## Docker Deployment

You can also run the server using Docker:

1. Create a Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy package files
COPY . .

# Install dependencies
RUN pip install -e .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["llm-content-proxy"]
```

2. Build the Docker image:

```bash
docker build -t llm-content-proxy .
```

3. Run the container:

```bash
docker run -p 8000:8000 llm-content-proxy
```

## Production Deployment

For production use, consider:

1. Using a production ASGI server like Gunicorn with Uvicorn workers:

```bash
pip install gunicorn
gunicorn llm_content_proxy.server.app:create_app\(\) -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

2. Setting up a reverse proxy like Nginx in front of the application

3. Adding authentication to protect the API

4. Implementing rate limiting to prevent abuse

5. Setting up monitoring and health checks

## Troubleshooting

- If you get a "Port already in use" error, change the port using the `port` parameter.
- If you get module import errors, ensure you're running the commands from the project root directory.
- If you see connection errors, check your firewall settings.