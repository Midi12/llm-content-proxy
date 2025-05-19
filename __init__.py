"""
Website content extractor package.
This package provides functionality to extract the main content from web pages.
"""

from .core.extractor import ContentExtractor
from .server.app import create_app, run_server

__version__ = "1.0.0"
__all__ = ["ContentExtractor", "create_app", "run_server"]