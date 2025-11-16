from promptflow.core import tool
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@tool
def retrieve(query: str, index_name: str, top_k: int = 3) -> str:
    """
    Retrieve relevant documents from Azure AI Search index.

    Args:
        query: The search query
        index_name: The name of the Azure AI Search index
        top_k: Number of documents to retrieve

    Returns:
        A formatted string containing the retrieved documents
    """
    # Get Azure AI Search credentials from environment variables
    search_service_name = os.getenv("AZURE_SEARCH_SERVICE_NAME")
    search_api_key = os.getenv("AZURE_SEARCH_API_KEY")
    search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")

    # If endpoint is not set, construct it from service name
    if not search_endpoint and search_service_name:
        search_endpoint = (
            f"https://{search_service_name}.search.windows.net"
        )

    if not search_endpoint or not search_api_key:
        raise ValueError(
            "Azure AI Search credentials not found. Please set "
            "AZURE_SEARCH_ENDPOINT (or AZURE_SEARCH_SERVICE_NAME) and "
            "AZURE_SEARCH_API_KEY in your .env file or environment variables."
        )

    # Initialize the search client
    credential = AzureKeyCredential(search_api_key)
    search_client = SearchClient(
        endpoint=search_endpoint,
        index_name=index_name,
        credential=credential
    )

    # Perform hybrid search (vector + keyword)
    # The search_type parameter can be set to "semantic", "vector",
    # or defaults to hybrid
    results = search_client.search(
        search_text=query,
        top=top_k,
        include_total_count=True
    )

    # Extract and format the retrieved documents
    documents = []
    for result in results:
        # Try to get content field, or concatenate all text fields
        content = result.get("content") or result.get("text") or ""
        if not content:
            # If no content field, concatenate all string fields
            content = " ".join([
                str(v) for k, v in result.items()
                if isinstance(v, str) and k != "id"
            ])

        # Add metadata if available
        metadata = {}
        if "id" in result:
            metadata["id"] = result["id"]
        if "@search.score" in result:
            metadata["score"] = result["@search.score"]

        doc_text = content
        if metadata:
            score = metadata.get('score', 'N/A')
            doc_text = f"[Score: {score}] {content}"

        documents.append(doc_text)

    # Return formatted context
    if documents:
        return "\n\n---\n\n".join(documents)
    else:
        return "No relevant documents found."
