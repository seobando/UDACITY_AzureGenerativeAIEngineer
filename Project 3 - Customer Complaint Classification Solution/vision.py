# vision.py

import os
from PIL import Image, ImageDraw, ImageFont
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

    # Create prompt for image description with location details
    prompt = (
        "Analyze this image in detail and describe any defects, issues, "
        "or problems visible. For each defect, describe:\n"
        "1. What the defect is (crack, damage, wrong item, etc.)\n"
        "2. Where it is located in the image (center, top-left, bottom-right, "
        "foreground, background, etc.)\n"
        "3. The size and appearance of the defect\n"
        "4. Any other notable visual elements\n"
        "Be very specific about defect locations and appearances. "
        "Focus on issues that would be part of a customer complaint."
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


def get_defect_locations(image_path, deployment_name=None):
    """
    Uses vision API to get specific defect location information.

    Args:
        image_path (str): Path to the image.
        deployment_name (str, optional): Model/deployment name.

    Returns:
        str: Description with location information.
    """
    if not deployment_name:
        deployment_name = os.getenv('GPT_DEPLOYMENT')
        if not deployment_name:
            raise ValueError(
                "GPT_DEPLOYMENT environment variable not set."
            )

    client = create_azure_openai_client()

    location_prompt = (
        "Analyze this image and identify ALL defects, damages, or issues. "
        "For each defect, describe:\n"
        "1. The type of defect (crack, break, damage, wrong item, etc.)\n"
        "2. Its EXACT location using these terms: "
        "'center', 'top', 'bottom', 'left', 'right', 'top-left', "
        "'top-right', 'bottom-left', 'bottom-right', 'foreground', "
        "'background'\n"
        "3. Approximate size (small, medium, large)\n"
        "4. What part of the product is affected\n"
        "Be very specific about locations. List each defect separately."
    )

    location_info = describe_local_image(
        client=client,
        image_path=image_path,
        deployment_name=deployment_name,
        prompt=location_prompt
    )

    return location_info


def annotate_image(image_path="output/generated_image.png",
                   deployment_name=None):
    """
    Annotates the image with bounding boxes highlighting defect areas.

    Args:
        image_path (str): Path to the generated image.
        deployment_name (str, optional): Model/deployment name for vision API.

    Returns:
        str: Path to the annotated image.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Get detailed location information from vision API
    location_info = get_defect_locations(image_path, deployment_name)

    # Load the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Analyze location info to identify defect areas
    defect_areas = []
    location_info_lower = location_info.lower()

    # Define location mappings to coordinates
    location_coords = {
        'center': (width * 0.25, height * 0.25, width * 0.75, height * 0.75),
        'top': (width * 0.2, height * 0.05, width * 0.8, height * 0.35),
        'bottom': (width * 0.2, height * 0.65, width * 0.8, height * 0.95),
        'left': (width * 0.05, height * 0.2, width * 0.45, height * 0.8),
        'right': (width * 0.55, height * 0.2, width * 0.95, height * 0.8),
        'top-left': (width * 0.05, height * 0.05,
                     width * 0.45, height * 0.35),
        'top-right': (width * 0.55, height * 0.05,
                      width * 0.95, height * 0.35),
        'bottom-left': (width * 0.05, height * 0.65,
                        width * 0.45, height * 0.95),
        'bottom-right': (width * 0.55, height * 0.65,
                         width * 0.95, height * 0.95),
        'foreground': (width * 0.15, height * 0.3, width * 0.85, height * 0.7),
    }

    # Find all mentioned locations
    found_locations = []
    for loc_name, coords in location_coords.items():
        # Check for location mentions (with word boundaries)
        if (f' {loc_name} ' in location_info_lower or
                location_info_lower.startswith(f'{loc_name} ') or
                location_info_lower.endswith(f' {loc_name}')):
            found_locations.append((loc_name, coords))

    # If specific locations found, use them
    if found_locations:
        defect_areas = [coords for _, coords in found_locations]
    else:
        # Fallback: check for defect keywords and use center
        defect_keywords = [
            'crack', 'damage', 'broken', 'defect', 'issue', 'problem',
            'screen', 'surface', 'foreground'
        ]
        has_defect = any(keyword in location_info_lower
                         for keyword in defect_keywords)
        if has_defect:
            defect_areas.append(location_coords['center'])
        else:
            # Default to center for main subject
            defect_areas.append(location_coords['center'])

    # Draw bounding boxes for each defect area
    box_color = (255, 0, 0)  # Red color for bounding boxes
    box_width = 5  # Thickness of the bounding box lines

    for i, (x1, y1, x2, y2) in enumerate(defect_areas):
        # Draw rectangle
        draw.rectangle(
            [x1, y1, x2, y2],
            outline=box_color,
            width=box_width
        )

        # Add label if possible
        try:
            # Try to use default font, fallback to basic if not available
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except (OSError, IOError):
                try:
                    font = ImageFont.truetype(
                        "C:/Windows/Fonts/arial.ttf", 20)
                except (OSError, IOError):
                    font = ImageFont.load_default()

            label = f"Defect Area {i+1}"
            # Get text bounding box
            bbox = draw.textbbox((0, 0), label, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Draw background for text
            draw.rectangle(
                [x1, y1 - text_height - 5, x1 + text_width + 10,
                 y1],
                fill=box_color
            )

            # Draw text
            draw.text(
                (x1 + 5, y1 - text_height - 2),
                label,
                fill=(255, 255, 255),  # White text
                font=font
            )
        except (OSError, IOError, AttributeError):
            # If font loading fails, just draw the box
            pass

    # Save annotated image
    os.makedirs("output", exist_ok=True)
    annotated_path = "output/annotated_image.png"
    img.save(annotated_path)

    return annotated_path

# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     description = describe_image()
#     print(description)
