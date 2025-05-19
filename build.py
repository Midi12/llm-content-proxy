#!/usr/bin/env python
"""
Build script for LLM Content Proxy.
Combines the core module with cloud function handlers to create a single file bundle.
"""

import argparse
import os
import sys
import shutil
import re
from pathlib import Path
import importlib.util

def main():
    parser = argparse.ArgumentParser(description="Build LLM Content Proxy for cloud deployment")
    parser.add_argument("--provider", choices=["gcp", "aws", "azure"], required=True, 
                        help="Cloud provider (gcp, aws, or azure)")
    parser.add_argument("--output", default="./build", 
                        help="Output directory (default: ./build)")
    parser.add_argument("--core-path", default="core/extractor.py",
                        help="Path to core extractor.py (default: ./core/extractor.py)")
    parser.add_argument("--impl-path", default='impl',
                        help="Path to implementation directory (default: ./impl)")
    args = parser.parse_args()
    
    # Get absolute paths
    script_dir = Path(__file__).parent.absolute()
    output_dir = Path(args.output).absolute()
    
    # Set default core path if not provided
    core_path = Path(args.core_path).absolute()
    
    # Set default implementation path if not provided
    impl_path = Path(args.impl_path).absolute()
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Verify core extractor exists
    if not core_path.exists():
        print(f"Error: Core extractor not found at {core_path}")
        sys.exit(1)
    
    # Verify implementation directory exists
    if not impl_path.exists():
        print(f"Error: Implementation directory not found at {impl_path}")
        sys.exit(1)
    
    # Read core extractor code
    print(f"Reading core extractor from {core_path}")
    with open(core_path, 'r', encoding='utf-8') as file:
        extractor_code = file.read()
    
    # Build bundle for the specified provider
    print(f"Building bundle for {args.provider.upper()}...")
    if args.provider == "gcp":
        output_dir = output_dir / "gcp"
        output_dir.mkdir(parents=True, exist_ok=True)
        bundle_gcp(extractor_code, impl_path, output_dir)
    elif args.provider == "aws":
        output_dir = output_dir / "aws"
        output_dir.mkdir(parents=True, exist_ok=True)
        bundle_aws(extractor_code, impl_path, output_dir)
    elif args.provider == "azure":
        output_dir = output_dir / "azure"
        output_dir.mkdir(parents=True, exist_ok=True)
        bundle_azure(extractor_code, impl_path, output_dir)
    
    print(f"\nBundle created successfully in {output_dir}")
    print(f"You can now deploy these files to your {args.provider.upper()} environment.")

def extract_imports(code):
    """Extract import statements from the code."""
    imports = []
    lines = code.split('\n')
    
    for line in lines:
        if line.startswith('import ') or line.startswith('from '):
            # Skip common imports that might be added by the template
            if 'logging' not in line and '__future__' not in line:
                imports.append(line)
    
    return '\n'.join(imports)

def extract_class_code(code):
    """Extract the ContentExtractor class code."""
    pattern = re.compile(r'class ContentExtractor.*?(?=^# End of ContentExtractor|$)', 
                         re.DOTALL | re.MULTILINE)
    match = pattern.search(code)
    
    if not match:
        # Try alternative approach - find class and everything after it
        lines = code.split('\n')
        start_idx = None
        
        for i, line in enumerate(lines):
            if line.startswith('class ContentExtractor'):
                start_idx = i
                break
        
        if start_idx is not None:
            return '\n'.join(lines[start_idx:])
    
    return match.group(0) if match else None

def read_file(impl_path, filename):
    """Read a file from the implementation directories."""
    implementation_path = impl_path / filename
    
    if not implementation_path.exists():
        print(f"Error: Template file not found: {implementation_path}")
        sys.exit(1)
    
    with open(implementation_path, 'r', encoding='utf-8') as file:
        return file.read()

def bundle_gcp(extractor_code, impl_path, output_dir):
    template = read_file(impl_path, "gcp/main.py")
    
    bundle_content = extractor_code
    bundle_content += "\n\n"
    bundle_content += template
    bundle_content += "\n\n"
    
    # Write the bundled file
    main_path = output_dir / "main.py"
    with open(main_path, 'w', encoding='utf-8') as file:
        file.write(bundle_content)
    
    # Copy requirements.txt
    requirements_path = output_dir / "requirements.txt"
    requirements = read_file(impl_path, "gcp/requirements.txt")
    with open(requirements_path, 'w', encoding='utf-8') as file:
        file.write(requirements)
    
    print(f"Created: {main_path}")
    print(f"Created: {output_dir / 'requirements.txt'}")

def bundle_aws(extractor_code, impl_path, output_dir):
    """Create an AWS Lambda bundle."""
    # Read the AWS template
    template = read_file(impl_path, "aws/lambda_function.py")
    
    # Combine extractor code with the template
    bundle_content = extractor_code
    bundle_content += "\n\n"
    bundle_content += template
    bundle_content += "\n\n"
    
    # Write the bundled file
    lambda_path = output_dir / "lambda_function.py"
    with open(lambda_path, 'w', encoding='utf-8') as file:
      file.write(bundle_content)
    
    # Copy requirements.txt
    requirements_path = output_dir / "requirements.txt"
    requirements = read_file(impl_path, "aws/requirements.txt")
    with open(requirements_path, 'w', encoding='utf-8') as file:
      file.write(requirements)
    
    # Copy any additional AWS config files if they exist
    for filename in ["template.yaml", "samconfig.toml"]:
      template_file = impl_path / "aws" / filename
      if template_file.exists():
        shutil.copy(template_file, output_dir / filename)
    
    print(f"Created: {lambda_path}")
    print(f"Created: {output_dir / 'requirements.txt'}")

def bundle_azure(extractor_code, impl_path, output_dir):
    """Create an Azure Function bundle."""
    # Read the Azure template
    template = read_file(impl_path, "azure/function_app.py")
    
    # Combine extractor code with the template
    bundle_content = extractor_code
    bundle_content += "\n\n"
    bundle_content += template
    bundle_content += "\n\n"
    
    # Write the bundled file
    function_path = output_dir / "function_app.py"
    with open(function_path, 'w', encoding='utf-8') as file:
      file.write(bundle_content)
    
    # Copy requirements.txt
    requirements_path = output_dir / "requirements.txt"
    requirements = read_file(impl_path, "azure/requirements.txt")
    with open(requirements_path, 'w', encoding='utf-8') as file:
      file.write(requirements)
    
    # Copy any additional Azure config files if they exist
    for filename in ["function.json", "host.json"]:
      template_file = impl_path / "azure" / filename
      if template_file.exists():
        shutil.copy(template_file, output_dir / filename)
    
    print(f"Created: {function_path}")
    print(f"Created: {output_dir / 'requirements.txt'}")

if __name__ == "__main__":
    main()