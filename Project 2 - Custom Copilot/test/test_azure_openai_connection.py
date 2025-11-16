#!/usr/bin/env python3
"""Simple script to test Azure OpenAI connection and deployments."""

import os
import sys
from dotenv import load_dotenv
from openai import AzureOpenAI


# Load .env from outlander-copilot folder
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
env_path = os.path.join(project_root, 'outlander-copilot', '.env')

if not os.path.exists(env_path):
    print(f"❌ Error: .env file not found at {env_path}")
    sys.exit(1)

load_dotenv(env_path)

api_key = os.getenv('AZURE_OPENAI_API_KEY')
endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')

if not api_key or not endpoint:
    print("❌ Error: Missing AZURE_OPENAI_API_KEY or "
          "AZURE_OPENAI_ENDPOINT in .env")
    sys.exit(1)

endpoint = endpoint.rstrip('/')
print(f"✅ Loaded credentials from {env_path}")
print(f"   Endpoint: {endpoint}\n")

# Create client
try:
    client = AzureOpenAI(
        api_key=api_key,
        api_version="2024-02-15-preview",
        azure_endpoint=endpoint
    )
    print("✅ Azure OpenAI client created\n")
except Exception as e:
    print(f"❌ Error creating client: {e}")
    sys.exit(1)

# Test common deployments
deployments = ["gpt-4o", "gpt-4", "gpt-35-turbo", "gpt-4o-mini"]
working = []

for name in deployments:
    try:
        response = client.chat.completions.create(
            model=name,
            messages=[{"role": "user", "content": "Say 'OK'"}],
            max_tokens=10
        )
        result = response.choices[0].message.content
        print(f"✅ {name}: Working ({result})")
        working.append(name)
    except Exception as e:
        error = str(e)
        if "DeploymentNotFound" in error or "404" in error:
            print(f"❌ {name}: Not found")
        else:
            print(f"❌ {name}: {error}")

print(f"\n{'='*50}")
if working:
    print(f"✅ Working deployments: {', '.join(working)}")
else:
    print("❌ No working deployments found")
print(f"{'='*50}")
