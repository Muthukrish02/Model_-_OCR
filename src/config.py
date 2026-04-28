"""
Configuration module for AI & OCR Project
Loads settings from environment variables
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==================== GEMINI API ====================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-3-flash-preview"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"

# ==================== LLAMA.CPP SERVER ====================
LLAMA_SERVER_PATH = os.getenv("LLAMA_SERVER_PATH", None)  # e.g., "C:\\llama-b8829-bin\\llama-server.exe"
LLAMA_SERVER_URL = os.getenv("LLAMA_SERVER_URL", "http://localhost:8080")
LLAMA_MODEL_NAME = "LFM2.5-VL"
LLAMA_CONTEXT_LENGTH = 2048
LLAMA_MAX_TOKENS = 21
LLAMA_TEMPERATURE = 0.0
LLAMA_AUTO_START = os.getenv("LLAMA_AUTO_START", "true").lower() == "true"

# ==================== IMAGE PROCESSING ====================
IMAGE_SIZE = int(os.getenv("IMAGE_SIZE", "256"))
SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg", ".bmp", ".gif"]

# ==================== AUDIO ====================
AUDIO_OUTPUT_FILE = "output.mp3"
AUDIO_LANGUAGE = "en"

# ==================== LOGGING ====================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ==================== VALIDATION ====================
def validate_config():
    """Validate critical configuration before running"""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set in .env file")
    return True
