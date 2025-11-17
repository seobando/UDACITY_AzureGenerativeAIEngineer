# gpt.py

import json
import os
from utils import (
    create_azure_openai_client,
    chat
)

# Function to classify the customer complaint based on the image description


def classify_with_gpt(image_description, transcription=None,
                      deployment_name=None):
    """
    Classifies the customer complaint into a category/subcategory based on
    the image description.

    Args:
        image_description (str): Description of the generated image.
        transcription (str, optional): The original transcription text.
        deployment_name (str, optional): Model/deployment name for GPT API.
            If not provided, uses GPT_DEPLOYMENT from environment.

    Returns:
        str: The category and subcategory of the complaint.
    """
    # Create a prompt that includes the image description and other details.
    # Load categories
    with open("categories.json", "r", encoding="utf-8") as f:
        categories = json.load(f)

    # Format categories for the prompt
    categories_text = json.dumps(categories, indent=2)

    prompt = (
        "You are a customer service classification system. Based on the "
        "following image description and complaint details, classify the "
        "customer complaint into the most appropriate category and "
        "subcategory from the provided catalog.\n\n"
        f"Image Description: {image_description}\n"
    )

    if transcription:
        prompt += f"\nOriginal Complaint Transcription: {transcription}\n"

    prompt += (
        f"\nAvailable Categories and Subcategories:\n{categories_text}\n\n"
        "Please respond with ONLY the category and subcategory in the "
        "following format:\n"
        "Category: [category name]\n"
        "Subcategory: [subcategory name]\n\n"
        "Be precise and choose the most appropriate classification based "
        "on the complaint details."
    )

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

    # Create system message for classification
    system_message = (
        "You are a helpful assistant that classifies customer complaints "
        "into appropriate categories."
    )

    # Use utility function for chat with custom system message
    classification = chat(
        gpt_client=client,
        deployment_name=deployment_name,
        prompt=prompt,
        system_message=system_message,
        temperature=0.3,
        max_tokens=200
    )

    # Save intermediate result
    os.makedirs("output", exist_ok=True)
    with open("output/classification.txt", "w", encoding="utf-8") as f:
        f.write(classification)

    return classification

# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     classification = classify_with_gpt()
#     print(classification)
