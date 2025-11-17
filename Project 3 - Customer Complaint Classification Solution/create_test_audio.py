"""
Helper script to create test audio complaint files using text-to-speech.
This script uses gTTS (Google Text-to-Speech) to generate MP3 files.
"""

import os
from gtts import gTTS

# Sample customer complaints for testing
SAMPLE_COMPLAINTS = {
    "complaint.mp3": (
        "Hello, I'm calling to complain about a product I purchased. "
        "I ordered a smartphone last week, but when it arrived, the screen "
        "was cracked and the device wouldn't turn on. This is completely "
        "unacceptable. I need a refund immediately."
    ),
    "complaint_electronics.mp3": (
        "I bought a laptop computer from your store, and it's been nothing "
        "but problems. The keyboard doesn't work properly, and the battery "
        "drains in less than an hour. I want to return this defective product."
    ),
    "complaint_clothing.mp3": (
        "I ordered a pair of shoes online, but they arrived in the wrong size. "
        "Also, the quality is terrible - the sole is already coming apart. "
        "I'm very disappointed with this purchase."
    ),
    "complaint_home.mp3": (
        "The furniture I ordered arrived damaged. There are scratches all over "
        "the surface and one of the legs is broken. This is not what I paid for. "
        "I need a replacement or a full refund."
    ),
}


def create_audio_file(filename, text, lang="en", slow=False):
    """
    Create an MP3 audio file from text using Google Text-to-Speech.

    Args:
        filename: Output filename (e.g., "complaint.mp3")
        text: Text to convert to speech
        lang: Language code (default: "en" for English)
        slow: Whether to speak slowly (default: False)
    """
    # Ensure audio directory exists
    audio_dir = "audio"
    os.makedirs(audio_dir, exist_ok=True)
    
    filepath = os.path.join(audio_dir, filename)
    
    try:
        # Create TTS object
        tts = gTTS(text=text, lang=lang, slow=slow)
        
        # Save to file
        tts.save(filepath)
        print(f"✓ Created: {filepath}")
        print(f"  Text: {text[:100]}...")
        return filepath
    except Exception as e:
        print(f"✗ Error creating {filepath}: {e}")
        return None


def main():
    """Create all sample complaint audio files."""
    print("Creating test audio complaint files...")
    print("=" * 60)
    
    created_files = []
    for filename, text in SAMPLE_COMPLAINTS.items():
        filepath = create_audio_file(filename, text)
        if filepath:
            created_files.append(filepath)
    
    print("=" * 60)
    print(f"\nCreated {len(created_files)} audio file(s):")
    for filepath in created_files:
        print(f"  - {filepath}")
    
    if created_files:
        print("\nYou can now run main.py to test the application!")
    else:
        print("\nNo files were created. Please check your internet connection.")


if __name__ == "__main__":
    main()

