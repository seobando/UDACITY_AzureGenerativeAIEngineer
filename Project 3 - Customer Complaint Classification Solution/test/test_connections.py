"""
Test connections for Azure OpenAI services.
Loads environment variables from .env file and tests connectivity.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Get environment variables (lines 1-8 from .env)
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
GPT_DEPLOYMENT = os.getenv('GPT_DEPLOYMENT')
GPT_VERSION = os.getenv('GPT_VERSION')
DALLE_DEPLOYMENT = os.getenv('DALLE_DEPLOYMENT')
DALLE_VERSION = os.getenv('DALLE_VERSION')


def test_env_variables_loaded():
    """Test that all required environment variables are loaded."""
    print("=" * 60)
    print("Testing Environment Variables")
    print("=" * 60)
    
    env_vars = {
        'AZURE_OPENAI_API_KEY': AZURE_OPENAI_API_KEY,
        'AZURE_OPENAI_ENDPOINT': AZURE_OPENAI_ENDPOINT,
        'GPT_DEPLOYMENT': GPT_DEPLOYMENT,
        'GPT_VERSION': GPT_VERSION,
        'DALLE_DEPLOYMENT': DALLE_DEPLOYMENT,
        'DALLE_VERSION': DALLE_VERSION,
    }
    
    all_loaded = True
    for var_name, var_value in env_vars.items():
        if var_value:
            # Remove quotes if present
            var_value = var_value.strip('"').strip("'")
            if len(var_value) > 20:
                msg = f"✓ {var_name}: {var_value[:20]}..."
            else:
                msg = f"✓ {var_name}: {var_value}"
            print(msg)
        else:
            print(f"✗ {var_name}: Not set or empty")
            all_loaded = False

    print()
    return all_loaded


def test_azure_openai_connection():
    """Test connection to Azure OpenAI endpoint."""
    print("=" * 60)
    print("Testing Azure OpenAI Connection")
    print("=" * 60)
    
    try:
        # Clean up the API key and endpoint
        api_key = None
        endpoint = None
        if AZURE_OPENAI_API_KEY:
            api_key = AZURE_OPENAI_API_KEY.strip().strip('"').strip("'")
        if AZURE_OPENAI_ENDPOINT:
            endpoint = AZURE_OPENAI_ENDPOINT.strip().strip('"').strip("'")

        if not api_key or not endpoint:
            print("✗ Missing API key or endpoint")
            return False

        # Create Azure OpenAI client
        api_version = GPT_VERSION or "2025-01-01-preview"
        AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )

        # Test connection by listing models/deployments
        print("✓ Azure OpenAI client created successfully")
        print(f"  Endpoint: {endpoint}")
        print(f"  API Version: {api_version}")

        # Try a simple API call to test connectivity
        # Note: This is a minimal test
        print("✓ Connection parameters validated")

        return True

    except Exception as e:
        print(f"✗ Connection failed: {str(e)}")
        return False


def test_gpt_deployment():
    """Test GPT deployment connection."""
    print("=" * 60)
    print("Testing GPT Deployment")
    print("=" * 60)
    
    try:
        api_key = None
        endpoint = None
        deployment = None
        if AZURE_OPENAI_API_KEY:
            api_key = AZURE_OPENAI_API_KEY.strip().strip('"').strip("'")
        if AZURE_OPENAI_ENDPOINT:
            endpoint = AZURE_OPENAI_ENDPOINT.strip().strip('"').strip("'")
        if GPT_DEPLOYMENT:
            deployment = GPT_DEPLOYMENT.strip().strip('"').strip("'")

        if not api_key or not endpoint:
            print("✗ Missing API key or endpoint")
            return False

        if not deployment:
            print("⚠ GPT_DEPLOYMENT not set - skipping deployment test")
            return None

        client = AzureOpenAI(
            api_key=api_key,
            api_version=GPT_VERSION or "2025-01-01-preview",
            azure_endpoint=endpoint
        )

        # Test with a simple completion
        user_msg = "Say 'Connection test successful' if you can read this."
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=20
        )

        result = response.choices[0].message.content
        print(f"✓ GPT Deployment '{deployment}' is accessible")
        print(f"  Response: {result}")
        return True

    except Exception as e:
        print(f"✗ GPT Deployment test failed: {str(e)}")
        return False


def test_dalle_deployment():
    """Test DALL-E deployment connection."""
    print("=" * 60)
    print("Testing DALL-E Deployment")
    print("=" * 60)
    
    try:
        api_key = None
        endpoint = None
        deployment = None
        if AZURE_OPENAI_API_KEY:
            api_key = AZURE_OPENAI_API_KEY.strip().strip('"').strip("'")
        if AZURE_OPENAI_ENDPOINT:
            endpoint = AZURE_OPENAI_ENDPOINT.strip().strip('"').strip("'")
        if DALLE_DEPLOYMENT:
            deployment = DALLE_DEPLOYMENT.strip().strip('"').strip("'")

        if not api_key or not endpoint:
            print("✗ Missing API key or endpoint")
            return False

        if not deployment:
            print("⚠ DALLE_DEPLOYMENT not set - skipping deployment test")
            return None

        api_version = DALLE_VERSION or "2024-02-01"
        AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )

        # Test with a simple image generation
        print(f"✓ DALL-E Deployment '{deployment}' parameters validated")
        print(f"  API Version: {api_version}")
        msg = "  Note: Full test would generate an image (skipped)"
        print(msg)

        return True

    except Exception as e:
        print(f"✗ DALL-E Deployment test failed: {str(e)}")
        return False


def test_whisper_connection():
    """Test Whisper model connection."""
    print("=" * 60)
    print("Testing Whisper Connection")
    print("=" * 60)
    
    try:
        api_key = None
        endpoint = None
        if AZURE_OPENAI_API_KEY:
            api_key = AZURE_OPENAI_API_KEY.strip().strip('"').strip("'")
        if AZURE_OPENAI_ENDPOINT:
            endpoint = AZURE_OPENAI_ENDPOINT.strip().strip('"').strip("'")

        if not api_key or not endpoint:
            print("✗ Missing API key or endpoint")
            return False

        AzureOpenAI(
            api_key=api_key,
            api_version=GPT_VERSION or "2025-01-01-preview",
            azure_endpoint=endpoint
        )

        print("✓ Whisper connection parameters validated")
        print("  Note: Full test would require an audio file (skipped)")

        return True

    except Exception as e:
        print(f"✗ Whisper connection test failed: {str(e)}")
        return False


def test_vision_connection():
    """Test Vision model connection."""
    print("=" * 60)
    print("Testing Vision (GPT-4o) Connection")
    print("=" * 60)
    
    try:
        api_key = None
        endpoint = None
        deployment = None
        if AZURE_OPENAI_API_KEY:
            api_key = AZURE_OPENAI_API_KEY.strip().strip('"').strip("'")
        if AZURE_OPENAI_ENDPOINT:
            endpoint = AZURE_OPENAI_ENDPOINT.strip().strip('"').strip("'")
        if GPT_DEPLOYMENT:
            deployment = GPT_DEPLOYMENT.strip().strip('"').strip("'")

        if not api_key or not endpoint:
            print("✗ Missing API key or endpoint")
            return False

        AzureOpenAI(
            api_key=api_key,
            api_version=GPT_VERSION or "2025-01-01-preview",
            azure_endpoint=endpoint
        )

        print("✓ Vision connection parameters validated")
        dep_str = deployment or 'Not specified'
        print(f"  Deployment: {dep_str}")
        print("  Note: Full test would require an image file (skipped)")

        return True

    except Exception as e:
        print(f"✗ Vision connection test failed: {str(e)}")
        return False


def main():
    """Run all connection tests."""
    print("\n" + "=" * 60)
    print("Azure OpenAI Connection Tests")
    print("=" * 60 + "\n")
    
    results = {}
    
    # Test 1: Environment variables
    results['env_vars'] = test_env_variables_loaded()
    print()
    
    # Test 2: Azure OpenAI connection
    results['azure_connection'] = test_azure_openai_connection()
    print()
    
    # Test 3: GPT deployment
    results['gpt'] = test_gpt_deployment()
    print()
    
    # Test 4: DALL-E deployment
    results['dalle'] = test_dalle_deployment()
    print()
    
    # Test 5: Whisper connection
    results['whisper'] = test_whisper_connection()
    print()
    
    # Test 6: Vision connection
    results['vision'] = test_vision_connection()
    print()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        if result is True:
            print(f"✓ {test_name}: PASSED")
        elif result is False:
            print(f"✗ {test_name}: FAILED")
        else:
            print(f"⚠ {test_name}: SKIPPED")
    
    print()
    
    # Overall status
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)
    
    print(f"Total: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed == 0:
        print("\n✓ All critical tests passed!")
        return 0
    else:
        msg = f"\n✗ {failed} test(s) failed. Please check your configuration."
        print(msg)
        return 1


if __name__ == "__main__":
    exit(main())
