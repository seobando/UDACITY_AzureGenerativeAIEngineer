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
        prompt (str): The prompt describing the customer complaint to visualize.
        model (str, optional): DALL-E deployment name.
            If not provided, uses DALLE_DEPLOYMENT from environment.
        size (str): Image size (default: "1024x1024").
        quality (str): Image quality (default: "standard").
        style (str): Image style (default: "vivid").

    Returns:
        str: The path to the generated image.
    """
    # Create a prompt to represent the customer complaint.
    # The prompt is passed as a parameter, but we can enhance it
    enhanced_prompt = (
        f"A clear, detailed illustration showing: {prompt}. "
        "The image should clearly depict the customer complaint issue."
    )

    # Create Azure OpenAI client
    client = create_azure_openai_client()

    # Use deployment name from environment if not provided
    if not model:
        model = os.getenv('DALLE_DEPLOYMENT')
        if not model:
            raise ValueError(
                "DALLE_DEPLOYMENT environment variable not set. "
                "Please set it in your .env file or provide model parameter."
            )

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

    img_response = requests.get(image_url)
    if img_response.status_code == 200:
        with open(image_path, "wb") as f:
            f.write(img_response.content)

    # Save the prompt used
    with open("output/image_prompt.txt", "w", encoding="utf-8") as f:
        f.write(enhanced_prompt)

    return image_path

# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     image_path = generate_image()
#     print(f"Generated image saved at: {image_path}")
