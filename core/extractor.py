"""
Core module for extracting content from web pages.
This provides the fundamental extraction logic independent of delivery method.
"""

import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContentExtractor:
    """Class for extracting main content from web pages."""
    
    def __init__(self, user_agent=None):
        """
        Initialize the content extractor.
        
        Args:
            user_agent (str, optional): Custom user agent string. Defaults to a standard browser.
        """
        self.session = requests.Session()
        
        # Set a user agent to avoid being blocked by some websites
        default_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        self.session.headers.update({
            'User-Agent': user_agent or default_user_agent
        })
    
    def validate_url(self, url):
        """
        Validate if the given string is a proper URL.
        
        Args:
            url (str): The URL to validate
            
        Returns:
            bool: True if valid URL, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def fetch_page(self, url, timeout=10):
        """
        Fetch the web page content.
        
        Args:
            url (str): The URL to fetch
            timeout (int, optional): Request timeout in seconds. Defaults to 10.
            
        Returns:
            str: The HTML content of the page
            
        Raises:
            ValueError: If the URL is invalid
            requests.exceptions.RequestException: If the request fails
        """
        if not self.validate_url(url):
            raise ValueError(f"Invalid URL: {url}")
        
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            raise
    
    def extract_content(self, html, url):
        """
        Extract the main content from HTML.
        
        Args:
            html (str): HTML content of the page
            url (str): Original URL (for reference)
            
        Returns:
            dict: Dictionary containing title, content, URL and word count
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove unwanted elements
        for element in soup.select('script, style, nav, footer, header, aside, iframe, .ad, .ads, .advertisement'):
            element.extract()
        
        # Get the title
        title = soup.title.string if soup.title else "No title found"
        
        # Extract main content - this is a simplified approach
        # Different websites have different structures, so this is a best-effort approach
        
        # Try to find main content by common article containers
        main_content = None
        
        # Look for article tags
        article = soup.find('article')
        if article:
            main_content = article
        
        # If no article tag, look for common content containers
        if not main_content:
            for selector in ['main', '.content', '#content', '.post', '.article', '.post-content', '.entry-content']:
                main_content = soup.select_one(selector)
                if main_content:
                    break
        
        # If still no main content, use the body with nav/header/footer removed
        if not main_content:
            main_content = soup.body
        
        # If we have main content, extract all paragraphs
        text_content = ""
        if main_content:
            # Get all paragraphs
            paragraphs = main_content.find_all('p')
            if paragraphs:
                text_content = "\n\n".join([p.get_text().strip() for p in paragraphs])
            else:
                # If no paragraphs, just get the text
                text_content = main_content.get_text().strip()
        
        # Fallback: if we still have no content, get all paragraphs from the body
        if not text_content and soup.body:
            paragraphs = soup.body.find_all('p')
            text_content = "\n\n".join([p.get_text().strip() for p in paragraphs])
        
        return {
            "title": title,
            "content": text_content,
            "url": url,
            "word_count": len(text_content.split()) if text_content else 0
        }
    
    def extract_from_url(self, url):
        """
        Extract content from a given URL.
        
        Args:
            url (str): The URL to extract content from
            
        Returns:
            dict: Dictionary containing title, content, URL and word count
        """
        logger.info(f"Extracting content from URL: {url}")
        html = self.fetch_page(url)
        return self.extract_content(html, url)