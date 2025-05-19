#!/bin/bash

# Azure Functions Deployment Script for LLM Content Proxy

# Set variables - customize these for your environment
RESOURCE_GROUP="llm-content-proxy-rg"
LOCATION="eastus"
STORAGE_ACCOUNT="llmcontentproxystorage"
FUNCTION_APP="llm-content-proxy"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "Azure CLI not found. Please install it first."
    exit 1
fi

# Check if Azure Functions Core Tools are installed
if ! command -v func &> /dev/null; then
    echo "Azure Functions Core Tools not found. Please install them first."
    exit 1
fi

# Create temporary deployment directory
TEMP_DIR=$(mktemp -d)
echo "Created temporary directory: $TEMP_DIR"

# Copy necessary files
echo "Copying necessary files..."
mkdir -p $TEMP_DIR/llm_content_proxy/core
cp ../../../llm_content_proxy/core/extractor.py $TEMP_DIR/llm_content_proxy/core/
cp ../../../llm_content_proxy/core/__init__.py $TEMP_DIR/llm_content_proxy/core/
cp function_app.py $TEMP_DIR/
cp function.json $TEMP_DIR/
cp host.json $TEMP_DIR/
cp requirements.txt $TEMP_DIR/

# Change to temporary directory
cd $TEMP_DIR
echo "Changed to temporary directory: $TEMP_DIR"

# Login to Azure (if not already logged in)
echo "Checking Azure login status..."
az account show > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Please login to Azure:"
    az login
fi

# Create resource group
echo "Creating resource group '$RESOURCE_GROUP' in location '$LOCATION'..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create storage account
echo "Creating storage account '$STORAGE_ACCOUNT'..."
az storage account create --name $STORAGE_ACCOUNT --location $LOCATION --resource-group $RESOURCE_GROUP --sku Standard_LRS

# Create function app
echo "Creating function app '$FUNCTION_APP'..."
az functionapp create --name $FUNCTION_APP --storage-account $STORAGE_ACCOUNT --consumption-plan-location $LOCATION --resource-group $RESOURCE_GROUP --runtime python --runtime-version 3.9 --functions-version 4

# Wait for function app to be ready
echo "Waiting for function app to be ready..."
sleep 30

# Deploy the function
echo "Deploying the function..."
func azure functionapp publish $FUNCTION_APP --python

# Get the function URL
FUNCTION_URL="https://$FUNCTION_APP.azurewebsites.net/api/extract"
echo "=================================="
echo "Function deployed successfully!"
echo "You can access it at: ${FUNCTION_URL}?link=https://example.com"
echo "=================================="

# Clean up
cd -
rm -rf $TEMP_DIR
echo "Cleaned up temporary directory"