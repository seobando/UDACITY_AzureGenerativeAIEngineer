# How to Find Azure Credentials for .env File

This guide shows you where to find the required Azure credentials in the Azure Portal.

## Required Environment Variables

Create a .env file in outlander-copilot folder with the following credentials:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_CONNECTION_NAME=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=

# Azure AI Search Configuration
AZURE_SEARCH_SERVICE_NAME=
AZURE_SEARCH_API_KEY=
AZURE_SEARCH_ENDPOINT=
```

## Finding Azure OpenAI Credentials

### 1. Azure OpenAI API Key and Endpoint

1. **Go to Azure Portal**: https://portal.azure.com
2. **Navigate to your Azure OpenAI resource**:
   - In the search bar, type "Azure OpenAI" or find it under "AI + Machine Learning"
   - Select your Azure OpenAI service/resource
3. **Get the API Key**:
   - In the left sidebar, go to **"Keys and Endpoint"** (under "Resource Management")
   - You'll see two keys: `KEY 1` and `KEY 2` (either one works)
   - Copy one of the keys → This is your `AZURE_OPENAI_API_KEY`
4. **Get the Endpoint**:
   - On the same "Keys and Endpoint" page, you'll see the **Endpoint** URL
   - It looks like: `https://<your-resource-name>.openai.azure.com/`
   - Copy this URL → This is your `AZURE_OPENAI_ENDPOINT`

**Alternative**: If you're using Azure AI Studio:
- Go to https://ai.azure.com
- Select your project/workspace
- Go to **Connections** → Find your Azure OpenAI connection
- Click on it to view the API key and endpoint

## Finding Azure AI Search Credentials

### 2. Azure AI Search API Key and Endpoint

1. **Go to Azure Portal**: https://portal.azure.com
2. **Navigate to your Azure AI Search resource**:
   - In the search bar, type "Azure AI Search" or "Search services"
   - Select your Azure AI Search service
3. **Get the API Key**:
   - In the left sidebar, go to **"Keys"** (under "Settings")
   - You'll see:
     - **Primary admin key** (recommended)
     - **Secondary admin key**
     - **Query keys** (read-only, for client apps)
   - Copy the **Primary admin key** → This is your `AZURE_SEARCH_API_KEY`
4. **Get the Endpoint**:
   - On the **"Overview"** page of your Azure AI Search service
   - You'll see the **URL** field
   - It looks like: `https://<your-service-name>.search.windows.net`
   - Copy this URL → This is your `AZURE_SEARCH_ENDPOINT`

**Note**: The endpoint can also be constructed as: `https://<service-name>.search.windows.net`

## Example .env File

Create a `.env` file in your project root with:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/

# Azure AI Search Configuration
AZURE_SEARCH_API_KEY=xyz789abc123def456ghi789jkl012mno345pqr678stu
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
```

## Quick Access Links

- **Azure Portal**: https://portal.azure.com
- **Azure AI Studio**: https://ai.azure.com
- **Azure OpenAI Service**: https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/OpenAI
- **Azure AI Search Services**: https://portal.azure.com/#view/HubsExtension/BrowseResource/resourceType/Microsoft.Search%2FsearchServices

## Security Notes

⚠️ **Important**: 
- Never commit your `.env` file to version control
- Keep your API keys secure and rotate them regularly
- Use different keys for development and production environments
- The `.env` file should already be in `.gitignore`

