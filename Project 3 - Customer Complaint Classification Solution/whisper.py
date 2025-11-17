# whisper.py

import os
from utils import create_azure_openai_client

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

    # Call the Whisper model to transcribe the audio file.
    client = create_azure_openai_client()

    # Use deployment name if provided, otherwise get from environment
    whisper_deployment = deployment_name or os.getenv('WHISPER_DEPLOYMENT')
    if not whisper_deployment:
        raise ValueError(
            "WHISPER_DEPLOYMENT environment variable not set. "
            "Please set it in your .env file or provide deployment_name."
        )

    with open(audio_file_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            file=audio_file,
            model=whisper_deployment
        )

    # Extract the transcription and return it.
    transcription_text = result.text

    # Save intermediate result
    os.makedirs("output", exist_ok=True)
    with open("output/transcription.txt", "w", encoding="utf-8") as f:
        f.write(transcription_text)

    return transcription_text

# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     transcription = transcribe_audio()
#     print(transcription)
