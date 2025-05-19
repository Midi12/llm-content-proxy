"""
Azure Functions implementation for website content extraction.
"""

import logging
import traceback
import sys
import os
import json
import azure.functions as func

# Add parent directory to path to import core package
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.extractor import ContentExtractor

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize extractor outside the function to reuse it across invocations
extractor = ContentExtractor()

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function HTTP trigger.
    
    Args:
        req: The HTTP request object
        
    Returns:
        An HTTP response with the extraction results or error message
    """
    # Set CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json"
    }
    
    # Handle OPTIONS request (preflight)
    if req.method == "OPTIONS":
        return func.HttpResponse(
            status_code=204,
            headers=headers
        )
    
    # Get the URL from query parameters
    link = req.params.get('link')
    
    if not link:
        return func.HttpResponse(
            json.dumps({"error": "Missing 'link' query parameter"}),
            status_code=400,
            headers=headers
        )
    
    try:
        # Extract content from the URL
        result = extractor.extract_from_url(link)
        
        # Return successful response
        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            headers=headers
        )
    
    except ValueError as e:
        logger.error(f"Invalid URL: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=400,
            headers=headers
        )
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        logger.error(traceback.format_exc())
        return func.HttpResponse(
            json.dumps({"error": f"Error extracting content: {str(e)}"}),
            status_code=500,
            headers=headers
        )

# For local testing
if __name__ == "__main__":
    # Simulate a function call locally
    class MockRequest:
        def __init__(self, params=None, method="GET"):
            self.params = params or {}
            self.method = method
    
    # Test with a sample URL
    test_req = MockRequest(params={"link": "https://example.com"})
    response = main(test_req)
    print(f"Status code: {response.status_code}")
    print(f"Body: {response.get_body().decode()}")