"""Text-to-Speech (TTS) utilities"""
import os
from gtts import gTTS
from src.config import AUDIO_OUTPUT_FILE, AUDIO_LANGUAGE


def speak_and_save(text, filename=AUDIO_OUTPUT_FILE, language=AUDIO_LANGUAGE):
    """
    Convert text to speech and save as MP3 file, then play it
    
    Args:
        text (str): Text to convert to speech
        filename (str): Output filename (default from config)
        language (str): Language code (default: 'en')
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"🔊 Converting text to speech...")
        
        tts = gTTS(text=text, lang=language)
        tts.save(filename)
        print(f"✅ Audio saved as {filename}")
        
        # Play audio (Windows)
        os.system(f"start {filename}")
        print(f"▶️  Playing audio...")
        
        return True
    except Exception as e:
        print(f"❌ TTS error: {str(e)}")
        return False


def save_text_to_speech(text, filename):
    """
    Save text to speech without playing
    
    Args:
        text (str): Text to convert
        filename (str): Output filename
        
    Returns:
        bool: True if successful
    """
    try:
        tts = gTTS(text=text, lang=AUDIO_LANGUAGE)
        tts.save(filename)
        print(f"✅ Audio saved as {filename}")
        return True
    except Exception as e:
        print(f"❌ TTS error: {str(e)}")
        return False
