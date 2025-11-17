# whisper.py

import os
from utils import create_whisper_openai_client

# Function to transcribe customer audio complaints using the Whisper model


def transcribe_audio(audio_file_path="audio/complaint.mp3",
                     deployment_name=None):
    """
    Transcribes an audio file into text using Azure OpenAI's Whisper model.

    Args:
        audio_file_path (str): Path to the audio file to transcribe.
        deployment_name (str, optional): Whisper deployment name.
            If not provided, uses WHISPER_DEPLOYMENT from environment.

    Returns:
        str: The transcribed text of the audio file.
    """
    # Load the audio file.
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    # Use deployment name if provided, otherwise get from environment
    whisper_deployment = deployment_name or os.getenv('WHISPER_DEPLOYMENT')
    if not whisper_deployment:
        raise ValueError(
            "WHISPER_DEPLOYMENT environment variable not set. "
            "Please set it in your .env file or provide deployment_name. "
            "Example: WHISPER_DEPLOYMENT=your-whisper-deployment-name\n"
            "To find your deployment name, check the Azure OpenAI portal "
            "under 'Deployments' section."
        )

    # Clean up deployment name (remove quotes if present)
    whisper_deployment = whisper_deployment.strip().strip('"').strip("'")

    # Use Whisper-specific API version if available, otherwise use default
    # Whisper typically uses API version 2024-06-01 or later
    whisper_api_version = (
        os.getenv('WHISPER_VERSION') or
        os.getenv('GPT_VERSION') or
        '2024-06-01'  # Default API version for Whisper
    )

    # Call the Whisper model to transcribe the audio file.
    # This uses WHISPER_ENDPOINT and WHISPER_API_KEY if available,
    # otherwise falls back to main endpoint/key
    client = create_whisper_openai_client(api_version=whisper_api_version)

    try:
        with open(audio_file_path, "rb") as audio_file:
            result = client.audio.transcriptions.create(
                file=audio_file,
                model=whisper_deployment
            )
    except Exception as e:
        error_msg = str(e)
        if "DeploymentNotFound" in error_msg:
            raise ValueError(
                f"Whisper deployment '{whisper_deployment}' not found. "
                f"Please verify:\n"
                f"1. The deployment name is correct in your .env file\n"
                f"2. The deployment exists in your Azure OpenAI resource\n"
                f"3. The deployment is active and accessible\n"
                f"Original error: {error_msg}"
            ) from e
        raise

    # Extract the transcription and return it.
    transcription_text = result.text

    # Save intermediate result
    os.makedirs("output", exist_ok=True)
    with open("output/transcription.txt", "w", encoding="utf-8") as f:
        f.write(transcription_text)

    return transcription_text


# Example Usage (for testing purposes, remove/comment when deploying):
if __name__ == "__main__":
    transcription = transcribe_audio()
    print(transcription)
