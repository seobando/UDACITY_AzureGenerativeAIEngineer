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
        "customer complaint into the MOST APPROPRIATE category and "
        "subcategory from the EXACT catalog provided below.\n\n"
        f"Image Description: {image_description}\n"
    )

    if transcription:
        prompt += f"\nOriginal Complaint Transcription: {transcription}\n"

    prompt += (
        f"\nAvailable Categories and Subcategories:\n{categories_text}\n\n"
        "CRITICAL REQUIREMENTS:\n"
        "1. You MUST use EXACTLY one of the category names from the list "
        "above (case-sensitive)\n"
        "2. You MUST use EXACTLY one of the subcategory names from within "
        "that category (case-sensitive)\n"
        "3. Do NOT use generic terms like 'Product issue' or 'General'\n"
        "4. Do NOT create new categories or subcategories\n"
        "5. Choose the most specific and accurate match\n\n"
        "Respond with ONLY the category and subcategory in this EXACT format:\n"
        "Category: [exact category name from the catalog]\n"
        "Subcategory: [exact subcategory name from that category]\n\n"
        "Example:\n"
        "Category: Electronics\n"
        "Subcategory: Mobile Phones & Accessories\n\n"
        "Now classify the complaint:"
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
        temperature=0.1,  # Lower temperature for more consistent results
        max_tokens=200
    )

    # Validate and parse classification
    classification = validate_classification(classification, categories)

    # Save intermediate result
    os.makedirs("output", exist_ok=True)
    with open("output/classification.txt", "w", encoding="utf-8") as f:
        f.write(classification)

    return classification


def validate_classification(classification_text, categories):
    """
    Validates that the classification uses exact category/subcategory
    from the catalog.

    Args:
        classification_text (str): Raw classification text from GPT.
        categories (dict): Dictionary of categories and subcategories.

    Returns:
        str: Validated classification text.
    """
    lines = classification_text.strip().split('\n')
    category = None
    subcategory = None

    # Extract category and subcategory
    for line in lines:
        line_lower = line.lower().strip()
        if line_lower.startswith('category:'):
            category = line.split(':', 1)[1].strip()
        elif line_lower.startswith('subcategory:'):
            subcategory = line.split(':', 1)[1].strip()

    # Validate against catalog
    if category and category in categories:
        valid_subcategories = categories[category]
        if subcategory and subcategory in valid_subcategories:
            # Return formatted classification
            return f"Category: {category}\nSubcategory: {subcategory}"
        else:
            # If subcategory is invalid, use first one from category
            if valid_subcategories:
                return (f"Category: {category}\n"
                        f"Subcategory: {valid_subcategories[0]}")
    elif category:
        # Category not found, try to find closest match
        category_lower = category.lower()
        for cat in categories.keys():
            if cat.lower() == category_lower:
                valid_subcategories = categories[cat]
                if valid_subcategories:
                    return (f"Category: {cat}\n"
                            f"Subcategory: {valid_subcategories[0]}")
                break

    # If validation fails, return original but log warning
    return classification_text

# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     classification = classify_with_gpt()
#     print(classification)
