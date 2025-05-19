# Azure Functions Setup

This guide covers how to deploy the LLM Content Proxy as an Azure Function.

## Prerequisites

- Python 3.7 or higher
- Azure CLI installed and configured
- Azure Functions Core Tools
- An Azure account
- Basic familiarity with Azure Functions

## Installation

1. Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/llm-content-proxy.git
cd llm-content-proxy
```

2. Install the package with Azure dependencies:

```bash
pip install -e .
pip install azure-functions
```

## Local Testing

You can test the Azure Function locally before deployment:

```bash
cd llm_content_proxy/impl/azure
python function_app.py
```

This will simulate a function call and output the response.

For a more complete local testing experience, use the Azure Functions Core Tools:

```bash
# Install the Azure Functions Core Tools if not already installed
npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Run the function locally
func start
```

You can test it using `curl`:

```bash
curl "http://localhost:7071/api/extract?link=https://example.com"
```

## Deployment

### Method 1: Using Visual Studio Code

1. Install the Azure Functions extension for VS Code
2. Open the azure folder in VS Code
3. Sign in to Azure
4. Click the "Deploy to Function App" button
5. Follow the prompts to create or select a Function App

### Method 2: Using Azure CLI

1. Prepare the deployment package:

```bash
# Create a temporary deployment directory
mkdir -p azure-deploy
cd azure-deploy

# Copy necessary files
mkdir -p llm_content_proxy/core
cp /path/to/llm_content_proxy/core/extractor.py llm_content_proxy/core/
cp /path/to/llm_content_proxy/core/__init__.py llm_content_proxy/core/
cp /path/to/llm_content_proxy/impl/azure/function_app.py .
cp /path/to/llm_content_proxy/impl/azure/function.json .
cp /path/to/llm_content_proxy/impl/azure/host.json .
cp /path/to/llm_content_proxy/impl/azure/requirements.txt .
```

2. Create a Function App in Azure:

```bash
# Set variables
RESOURCE_GROUP="llm-content-proxy-rg"
LOCATION="eastus"
STORAGE_ACCOUNT="llmcontentproxystorage"
FUNCTION_APP="llm-content-proxy"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create storage account
az storage account create --name $STORAGE_ACCOUNT --location $LOCATION --resource-group $RESOURCE_GROUP --sku Standard_LRS

# Create function app
az functionapp create --name $FUNCTION_APP --storage-account $STORAGE_ACCOUNT --consumption-plan-location $LOCATION --resource-group $RESOURCE_GROUP --runtime python --runtime-version 3.9 --functions-version 4
```

3. Deploy the Function:

```bash
# Deploy the function code
func azure functionapp publish $FUNCTION_APP --python
```

### Method 3: Using the Deployment Script

For convenience, a deployment script is provided:

1. Navigate to the Azure function directory:

```bash
cd llm_content_proxy/impl/azure
```

2. Create a deployment script:

```bash
#!/bin/bash

# Set variables
RESOURCE_GROUP="llm-content-proxy-rg"
LOCATION="eastus"
STORAGE_ACCOUNT="llmcontentproxystorage"
FUNCTION_APP="llm-content-proxy"

# Create temporary deployment directory
TEMP_DIR=$(mktemp -d)
echo "Created temporary directory: $TEMP_DIR"

# Copy necessary files
mkdir -p $TEMP_DIR/llm_content_proxy/core
cp ../../../llm_content_proxy/core/extractor.py $TEMP_DIR/llm_content_proxy/core/
cp ../../../llm_content_proxy/core/__init__.py $TEMP_DIR/llm_content_proxy/core/
cp function_app.py $TEMP_DIR/
cp function.json $TEMP_DIR/
cp host.json $TEMP_DIR/
cp requirements.txt $TEMP_DIR/

# Change to temporary directory
cd $TEMP_DIR

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create storage account
az storage account create --name $STORAGE_ACCOUNT --location $LOCATION --resource-group $RESOURCE_GROUP --sku Standard_LRS

# Create function app
az functionapp create --name $FUNCTION_APP --storage-account $STORAGE_ACCOUNT --consumption-plan-location $LOCATION --resource-group $RESOURCE_GROUP --runtime python --runtime-version 3.9 --functions-version 4

# Deploy the function
func azure functionapp publish $FUNCTION_APP --python

# Get the function URL
FUNCTION_URL="https://$FUNCTION_APP.azurewebsites.net/api/extract"
echo "Function deployed successfully!"
echo "You can access it at: ${FUNCTION_URL}?link=https://example.com"

# Clean up
cd -
rm -rf $TEMP_DIR
echo "Cleaned up temporary directory"
```

3. Make it executable and run it:

```bash
chmod +x deploy.sh
./deploy.sh
```

## Usage

Once deployed, you can access the function at:

```
GET https://your-function-app-name.azurewebsites.net/api/extract?link=https://example.com
```

You can test it using `curl`:

```bash
curl "https://your-function-app-name.azurewebsites.net/api/extract?link=https://example.com"
```

## Custom Domain (Optional)

For a cleaner URL, you can set up a custom domain:

1. In the Azure Portal, go to your Function App
2. Click on "Custom domains"
3. Follow the wizard to add your custom domain
4. Set up the required DNS records with your domain provider

## Production Considerations

For production use, consider:

1. **Authentication**: Add authentication to protect your function
2. **CORS Settings**: Configure CORS in the Azure Portal if needed
3. **Caching**: Add a caching layer with Azure Redis Cache
4. **Monitoring**: Set up Application Insights
5. **Scaling**: Configure scaling limits to control costs
6. **Timeout Settings**: Adjust timeout settings based on your needs

## Cost Optimization

Azure Functions has a consumption-based pricing model:

- Use the minimum memory allocation needed
- Implement caching to reduce function executions
- Consider a Premium plan for predictable workloads
- Monitor execution times and optimize code to reduce billing

## Troubleshooting

- If deployment fails, check the Azure CLI output
- If the function returns errors, check the Application Insights logs
- If you get timeout errors, increase the function timeout in host.json
- For CORS issues, verify the CORS settings in both your code and the Azure Portal