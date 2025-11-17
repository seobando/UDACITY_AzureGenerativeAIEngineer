# dalle.py

import requests
import os
from utils import (
    create_azure_openai_client,
    generate_image as utils_generate_image
)

# Function to generate an image representing the customer complaint


def generate_image(prompt, model=None, size="1024x1024",
                   quality="standard", style="vivid"):
    """
    Generates an image based on a prompt using Azure OpenAI's DALL-E model.

    Args:
        prompt (str): The prompt describing the customer complaint
            to visualize.
        model (str, optional): DALL-E deployment name.
            If not provided, uses DALLE_DEPLOYMENT from environment.
        size (str): Image size (default: "1024x1024").
        quality (str): Image quality (default: "standard").
        style (str): Image style (default: "vivid").

    Returns:
        str: The path to the generated image.
    """
    # Create a detailed, specific prompt to ensure accurate visual representation
    # Extract key defect details from the complaint
    enhanced_prompt = (
        f"Create a clear, detailed, realistic illustration showing the exact "
        f"customer complaint: {prompt}. "
        f"The image must accurately and clearly show: "
        f"1. The specific product or item mentioned in the complaint, "
        f"2. The exact type of damage, defect, or issue described "
        f"(e.g., cracked screen, broken part, wrong size, etc.), "
        f"3. The precise location and appearance of the defect, "
        f"4. The condition of the product as described. "
        f"Make the defect highly visible and prominent in the image. "
        f"Use a clean background to focus attention on the product and defect. "
        f"The image should be photorealistic and clearly show the complaint issue."
    )

    # Use deployment name from environment if not provided
    if not model:
        model = os.getenv('DALLE_DEPLOYMENT')
        if not model:
            raise ValueError(
                "DALLE_DEPLOYMENT environment variable not set. "
                "Please set it in your .env file or provide model parameter."
            )

    # Use DALL-E-specific API version if available
    # Default to 2024-02-01 if not set (based on endpoint URL)
    dalle_api_version = (
        os.getenv('DALLE_VERSION') or
        os.getenv('GPT_VERSION') or
        '2024-02-01'  # Default API version for DALL-E
    )

    # Create Azure OpenAI client with DALL-E API version
    client = create_azure_openai_client(api_version=dalle_api_version)

    # Use utility function to generate the image
    image_url = utils_generate_image(
        client=client,
        prompt=enhanced_prompt,
        model=model,
        size=size,
        quality=quality,
        style=style
    )

    # Download and save the image
    os.makedirs("output", exist_ok=True)
    image_path = "output/generated_image.png"

    img_response = requests.get(image_url, timeout=30)
    if img_response.status_code == 200:
        with open(image_path, "wb") as f:
            f.write(img_response.content)

    # Save the prompt used
    with open("output/image_prompt.txt", "w", encoding="utf-8") as f:
        f.write(enhanced_prompt)

    return image_path


# Example Usage (for testing purposes, remove/comment when deploying):
if __name__ == "__main__":
    test_prompt = (
        "Customer complaint: Hello. I'm calling to complain about a "
        "product I purchased. I ordered a smartphone last week. But when "
        "it arrived, the screen was cracked and the device wouldn't turn "
        "on. This is completely unacceptable. I need a refund immediately."
    )
    test_image_path = generate_image(test_prompt)
    print(f"Generated image saved at: {test_image_path}")
