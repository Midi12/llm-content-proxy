"""
Google Cloud Function entry point for website content extraction.
"""

import logging
import traceback
from flask import jsonify, Request
import functions_framework
import sys
import os

# Add parent directory to path to import core package
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.extractor import ContentExtractor

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize extractor outside the function to reuse it across invocations
extractor = ContentExtractor()

@functions_framework.http
def extract_content(request: Request):
    """
    HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using make_response.
    """
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    
    # Get the URL from the query parameter
    link = request.args.get('link')
    
    if not link:
        return (jsonify({'error': 'Missing "link" query parameter'}), 400, headers)
    
    try:
        # Extract content from the URL
        result = extractor.extract_from_url(link)
        return (jsonify(result), 200, headers)
    except ValueError as e:
        return (jsonify({'error': str(e)}), 400, headers)
    except Exception as e:
        logger.error(f"Error processing URL {link}: {str(e)}")
        logger.error(traceback.format_exc())
        return (jsonify({'error': f"Error extracting content: {str(e)}"}), 500, headers)

# For local testing
if __name__ == "__main__":
    from flask import Flask, request
    
    app = Flask(__name__)
    
    @app.route('/', methods=['GET'])
    def test_function():
        return extract_content(request)
    
    app.run(host='0.0.0.0', port=8080)