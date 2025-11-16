from promptflow import tool
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Get the directory of this file and the parent directory (outlander-copilot)
_current_dir = Path(__file__).parent
_flow_dir = _current_dir.parent

# Set up Jinja2 environment to load templates from the flow directory
_jinja_env = Environment(loader=FileSystemLoader(_flow_dir))


@tool
def chat(
    question: str,
    context: str,
    chat_history: list,
    deployment_name: str = "gpt-4o",
    max_tokens: int = 512,
    temperature: float = 0.7
) -> str:
    """
    Generate a chat response using Azure OpenAI with retrieved context.

    Args:
        question: The user's question
        context: Retrieved context from Azure AI Search
        chat_history: List of previous chat interactions
        deployment_name: Azure OpenAI deployment name (default: gpt-4o)
        max_tokens: Maximum tokens in response (default: 512)
        temperature: Sampling temperature (default: 0.7)

    Returns:
        The assistant's response as a string
    """
    # Get Azure OpenAI credentials from environment variables
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    api_type = os.getenv("AZURE_OPENAI_API_TYPE", "azure")
    
    # Optional: Allow deployment name to be overridden by env var
    if not deployment_name:
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")

    if not api_key or not endpoint:
        raise ValueError(
            "Azure OpenAI credentials not found. Please set "
            "AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT in your .env file "
            "or environment variables."
        )

    # Clean endpoint (remove trailing slash)
    endpoint = endpoint.rstrip('/')

    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=endpoint
    )

    # Load and render the Jinja2 template
    try:
        template = _jinja_env.get_template("chat.jinja2")
        # Render the template with the provided variables
        rendered_prompt = template.render(
            context=context,
            chat_history=chat_history,
            question=question
        )
    except Exception as e:
        raise RuntimeError(f"Error loading or rendering chat.jinja2 template: {str(e)}")

    # Parse the rendered prompt to extract messages
    # The template format renders as:
    # system:
    # <system message>
    # 
    # Context:
    # <context>
    # 
    # user:
    # <question from history>
    # assistant:
    # <answer from history>
    # ...
    # user:
    # <current question>
    
    lines = rendered_prompt.split('\n')
    messages = []
    current_role = None
    current_content = []
    
    for line in lines:
        stripped_line = line.rstrip()
        
        # Check for role markers (exact match after stripping)
        if stripped_line == 'system:':
            # Save previous message if exists
            if current_role and current_content:
                content = '\n'.join(current_content).strip()
                if content:  # Only add non-empty messages
                    messages.append({"role": current_role, "content": content})
            current_role = "system"
            current_content = []
        elif stripped_line == 'user:':
            # Save previous message if exists
            if current_role and current_content:
                content = '\n'.join(current_content).strip()
                if content:  # Only add non-empty messages
                    messages.append({"role": current_role, "content": content})
            current_role = "user"
            current_content = []
        elif stripped_line == 'assistant:':
            # Save previous message if exists
            if current_role and current_content:
                content = '\n'.join(current_content).strip()
                if content:  # Only add non-empty messages
                    messages.append({"role": current_role, "content": content})
            current_role = "assistant"
            current_content = []
        elif current_role:
            # Continue building current message (preserve original line, not stripped)
            current_content.append(line)
    
    # Add the last message
    if current_role and current_content:
        content = '\n'.join(current_content).strip()
        if content:  # Only add non-empty messages
            messages.append({"role": current_role, "content": content})
    
    # Ensure we have at least a system message
    if not messages or messages[0].get("role") != "system":
        # Fallback: create system message from template if parsing failed
        system_content = """You are a helpful assistant for Outlander Gear Co., specializing in outdoor equipment and products.
Use the following retrieved context to answer the user's question accurately. If the context doesn't contain relevant information, say so.

Context:
{context}""".format(context=context)
        messages.insert(0, {"role": "system", "content": system_content})

    # Call Azure OpenAI
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Error calling Azure OpenAI: {str(e)}")

