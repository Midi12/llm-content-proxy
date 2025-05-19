"""
AWS Lambda function for website content extraction.
"""

import json
import logging
import traceback
import sys
import os

# Add parent directory to path to import core package
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.extractor import ContentExtractor

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize extractor outside the handler to reuse it across invocations
extractor = ContentExtractor()

def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    
    Args:
        event (dict): Event data
        context (object): Lambda context
        
    Returns:
        dict: API Gateway response
    """
    # Log the event for debugging
    logger.info(f"Received event: {json.dumps(event)}")
    
    # Set response headers with CORS
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "GET"
    }
    
    # Handle OPTIONS request (preflight)
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 204,
            'headers': headers,
            'body': ''
        }
    
    try:
        # Extract the link parameter
        if 'queryStringParameters' in event and event['queryStringParameters'] and 'link' in event['queryStringParameters']:
            link = event['queryStringParameters']['link']
        else:
            logger.error("Missing 'link' query parameter")
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({"error": "Missing 'link' query parameter"})
            }
        
        # Extract content from the URL
        result = extractor.extract_from_url(link)
        
        # Return successful response
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(result)
        }
    
    except ValueError as e:
        logger.error(f"Invalid URL: {str(e)}")
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({"error": str(e)})
        }
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({"error": f"Error extracting content: {str(e)}"})
        }

# For local testing
if __name__ == "__main__":
    # Simulate API Gateway event
    test_event = {
        'httpMethod': 'GET',
        'queryStringParameters': {
            'link': 'https://example.com'
        }
    }
    
    # Test the handler
    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2))