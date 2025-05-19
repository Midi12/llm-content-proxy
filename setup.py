"""
Setup script for the llm_content_proxy package.
"""

from setuptools import setup, find_packages

setup(
    name="llm_content_proxy",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for extracting content from websites",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/llm-content-proxy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.3",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.0",
    ],
    extras_require={
        "gcp": ["functions-framework>=3.0.0"],
        "azure": ["azure-functions>=1.15.0"],
        "aws": ["boto3>=1.18.0"],
        "dev": ["pytest>=6.0.0", "black>=21.5b2", "flake8>=3.9.2"],
    },
    entry_points={
        "console_scripts": [
            "llm-content-proxy=server.app:run_server",
        ],
    },
)