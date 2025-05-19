"""
FastAPI server for website content extraction.
This provides a standalone HTTP server with API endpoints.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl
import traceback

from core.extractor import ContentExtractor

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Website Content Extractor API",
    description="API for extracting main content from web pages",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize content extractor
extractor = ContentExtractor()

class ExtractionResponse(BaseModel):
    """Model for extraction response."""
    title: str
    content: str
    url: str
    word_count: int

@app.get("/", response_model=ExtractionResponse)
async def extract_content(link: AnyHttpUrl = Query(..., description="URL of the webpage to extract content from")):
    """
    Extract the main content from the provided URL.
    
    Args:
        link: URL of the webpage to extract content from
        
    Returns:
        JSON object containing the extracted title, content, original URL, and word count.
    """
    try:
        result = extractor.extract_from_url(str(link))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing URL {link}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error extracting content: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

def create_app():
    """Create and return the FastAPI app."""
    return app

def run_server(host="0.0.0.0", port=8000):
    """Run the FastAPI server."""
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run_server()