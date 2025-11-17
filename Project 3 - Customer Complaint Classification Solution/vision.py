# vision.py

import os
from utils import (
    create_azure_openai_client,
    describe_local_image
)

# Function to describe the generated image and annotate issues


def describe_image(image_path="output/generated_image.png",
                   deployment_name=None):
    """
    Describes an image and identifies key visual elements related to the
    customer complaint.

    Args:
        image_path (str): Path to the generated image to describe.
        deployment_name (str, optional): Model/deployment name for vision API.
            If not provided, uses GPT_DEPLOYMENT from environment.

    Returns:
        str: A description of the image, including the annotated details.
    """
    # Load the generated image.
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Create Azure OpenAI client
    client = create_azure_openai_client()

    # Use deployment name from environment if not provided
    if not deployment_name:
        deployment_name = os.getenv('GPT_DEPLOYMENT')
        if not deployment_name:
            raise ValueError(
                "GPT_DEPLOYMENT environment variable not set. "
                "Please set it in your .env file or provide deployment_name."
            )

    # Create prompt for image description
    prompt = (
        "Describe this image in detail, focusing on any issues, defects, "
        "or problems visible. Identify key visual elements and annotate "
        "any areas that might be related to a customer complaint. "
        "Be specific about what you see."
    )

    # Use utility function to describe the image
    description = describe_local_image(
        client=client,
        image_path=image_path,
        deployment_name=deployment_name,
        prompt=prompt
    )

    # Save intermediate result
    os.makedirs("output", exist_ok=True)
    with open("output/image_description.txt", "w", encoding="utf-8") as f:
        f.write(description)

    return description

# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     description = describe_image()
#     print(description)
