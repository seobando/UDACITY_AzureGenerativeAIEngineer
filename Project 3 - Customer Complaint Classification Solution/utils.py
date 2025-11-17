from openai import AzureOpenAI
import json
import base64
import os
from pathlib import Path
from mimetypes import guess_type
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)


def create_openai_client(api_version, api_key, api_endpoint):
    """Create an Azure OpenAI client."""
    client = AzureOpenAI(
        api_version=api_version,
        api_key=api_key,
        azure_endpoint=api_endpoint
    )
    return client


def create_azure_openai_client(api_version=None):
    """
    Create an Azure OpenAI client from environment variables.
    Reads from AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, and GPT_VERSION.

    Args:
        api_version (str, optional): API version to use. If not provided,
            uses GPT_VERSION from environment or default.

    Returns:
        AzureOpenAI: Configured Azure OpenAI client.
    """
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')

    if not api_version:
        api_version = os.getenv('GPT_VERSION', '2024-02-15-preview')

    if not api_key:
        raise ValueError(
            "AZURE_OPENAI_API_KEY environment variable not set. "
            "Please set it in your .env file or environment."
        )
    if not endpoint:
        raise ValueError(
            "AZURE_OPENAI_ENDPOINT environment variable not set. "
            "Please set it in your .env file or environment."
        )

    # Clean up the API key and endpoint (remove quotes if present)
    api_key = api_key.strip().strip('"').strip("'")
    endpoint = endpoint.strip().strip('"').strip("'")

    # Ensure endpoint doesn't have trailing /openai or /deployments paths
    # The SDK will add those automatically
    if '/openai' in endpoint:
        endpoint = endpoint.split('/openai')[0]
    if '/deployments' in endpoint:
        endpoint = endpoint.split('/deployments')[0]
    # Remove trailing slash
    endpoint = endpoint.rstrip('/')

    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=endpoint
    )
    return client


def create_whisper_openai_client(api_version=None):
    """
    Create an Azure OpenAI client specifically for Whisper.
    Uses WHISPER_ENDPOINT and WHISPER_API_KEY if available,
    otherwise falls back to main AZURE_OPENAI_ENDPOINT and
    AZURE_OPENAI_API_KEY.

    Args:
        api_version (str, optional): API version to use. If not provided,
            uses WHISPER_VERSION or GPT_VERSION from environment or default.

    Returns:
        AzureOpenAI: Configured Azure OpenAI client for Whisper.
    """
    # Try Whisper-specific endpoint and API key first
    whisper_api_key = os.getenv('WHISPER_API_KEY')
    whisper_endpoint = os.getenv('WHISPER_ENDPOINT')

    # Fall back to main endpoint/key if Whisper-specific ones aren't set
    api_key = whisper_api_key or os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = whisper_endpoint or os.getenv('AZURE_OPENAI_ENDPOINT')

    if not api_version:
        api_version = (
            os.getenv('WHISPER_VERSION') or
            os.getenv('GPT_VERSION') or
            '2024-06-01'  # Default API version for Whisper
        )

    if not api_key:
        raise ValueError(
            "API key not set. Please set either WHISPER_API_KEY or "
            "AZURE_OPENAI_API_KEY in your .env file."
        )
    if not endpoint:
        raise ValueError(
            "Endpoint not set. Please set either WHISPER_ENDPOINT or "
            "AZURE_OPENAI_ENDPOINT in your .env file."
        )

    # Clean up the API key and endpoint (remove quotes if present)
    api_key = api_key.strip().strip('"').strip("'")
    endpoint = endpoint.strip().strip('"').strip("'")

    # Ensure endpoint doesn't have trailing /openai or /deployments paths
    # The SDK will add those automatically
    if '/openai' in endpoint:
        endpoint = endpoint.split('/openai')[0]
    if '/deployments' in endpoint:
        endpoint = endpoint.split('/deployments')[0]
    # Remove trailing slash
    endpoint = endpoint.rstrip('/')

    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=endpoint
    )
    return client


def local_image_to_data_url(image_path):
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'

    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(
            image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{base64_encoded_data}"


def describe_local_image(client, image_path, deployment_name, prompt):
    data_url = local_image_to_data_url(image_path)

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": data_url}}
                ]
            }
        ],
        max_tokens=1024
    )
    return response.choices[0].message.content


def describe_online_image(client, image_url, deployment_name, prompt):
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        max_tokens=1024
    )
    return response.choices[0].message.content


def generate_image(client, prompt, model, size,
                   quality,
                   style):
    try:
        result = client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            style=style
        )

        json_response = json.loads(result.model_dump_json())
        image_url = json_response["data"][0]["url"]

        return image_url
    except Exception as e:
        error_msg = str(e)
        if ("getaddrinfo failed" in error_msg or
                "Connection error" in error_msg):
            # Get endpoint from environment for better error message
            endpoint = os.getenv('AZURE_OPENAI_ENDPOINT', 'not set')
            api_version = getattr(client, '_api_version', 'unknown')
            raise ConnectionError(
                f"Failed to connect to Azure OpenAI endpoint for DALL-E. "
                f"Please verify:\n"
                f"1. AZURE_OPENAI_ENDPOINT is correct in your .env file\n"
                f"   Current value: {endpoint}\n"
                f"2. The endpoint URL is accessible from your network\n"
                f"3. The endpoint format is correct "
                f"(should be base URL without /openai)\n"
                f"   Example: https://your-resource.openai.azure.com\n"
                f"4. DALLE_VERSION is set correctly "
                f"(if different from GPT_VERSION)\n"
                f"   API Version being used: {api_version}\n"
                f"5. Model deployment name: {model}\n"
                f"Original error: {error_msg}"
            ) from e
        raise


def chat(gpt_client, deployment_name, prompt, system_message=None,
         temperature=None, max_tokens=1000):
    """
    Chat completion using GPT model.

    Args:
        gpt_client: OpenAI client instance.
        deployment_name: Model/deployment name.
        prompt: User prompt.
        system_message: Optional custom system message.
        temperature: Optional temperature setting.
        max_tokens: Maximum tokens in response.

    Returns:
        str: Response content.
    """
    if system_message is None:
        system_message = "You are a helpful assistant."

    messages = [
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    params = {
        "model": deployment_name,
        "messages": messages,
        "max_tokens": max_tokens
    }

    if temperature is not None:
        params["temperature"] = temperature

    response = gpt_client.chat.completions.create(**params)

    result = response.choices[0].message.content
    return result
