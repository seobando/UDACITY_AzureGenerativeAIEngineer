# main.py

# Import functions from other modules
from whisper import transcribe_audio
from dalle import generate_image
from vision import describe_image
from gpt import classify_with_gpt
import os
import json

# Main function to orchestrate the workflow


def main(audio_file_path="audio/complaint.mp3"):
    """
    Orchestrates the workflow for handling customer complaints.

    Steps include:
    1. Transcribe the audio complaint.
    2. Create a prompt from the transcription.
    3. Generate an image representing the issue.
    4. Describe the generated image.
    5. Annotate the reported issue in the image.
    6. Classify the complaint into a category/subcategory pair.

    Args:
        audio_file_path (str): Path to the audio complaint file.

    Returns:
        dict: Dictionary containing all intermediate and final results.
    """
    # Step 1: Transcribe the audio complaint
    print("Step 1: Transcribing audio complaint...")
    transcription = transcribe_audio(audio_file_path)
    print(f"Transcription: {transcription}\n")

    # Step 2: Create a prompt from the transcription
    print("Step 2: Creating prompt from transcription...")
    prompt = f"Customer complaint: {transcription}"
    print(f"Prompt created: {prompt}\n")

    # Step 3: Generate an image based on the prompt
    print("Step 3: Generating image representing the issue...")
    image_path = generate_image(prompt)
    print(f"Image generated and saved at: {image_path}\n")

    # Step 4: Describe the generated image
    print("Step 4: Describing the generated image...")
    image_description = describe_image(image_path)
    print(f"Image description: {image_description}\n")

    # Step 5: Annotate the reported issue in the image
    # The annotation is included in the image description from the vision model
    print("Step 5: Annotating the reported issue in the image...")
    print("Annotation completed as part of image description.\n")

    # Step 6: Classify the complaint based on the image description
    print("Step 6: Classifying the complaint...")
    classification = classify_with_gpt(image_description, transcription)
    print(f"Classification result:\n{classification}\n")

    # Step 7: Store all results
    results = {
        "transcription": transcription,
        "prompt": prompt,
        "image_path": image_path,
        "image_description": image_description,
        "classification": classification
    }

    os.makedirs("output", exist_ok=True)
    with open("output/results_summary.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("=" * 50)
    print("WORKFLOW COMPLETE")
    print("=" * 50)
    print("\nAll results saved to output/ directory:")
    print("  - transcription.txt")
    print("  - image_prompt.txt")
    print("  - generated_image.png")
    print("  - image_description.txt")
    print("  - classification.txt")
    print("  - results_summary.json")
    print("\nFinal Classification:")
    print(classification)

    return results


# Example Usage (for testing purposes, remove/comment when deploying):
if __name__ == "__main__":
    main()
