"""Utility modules - Image processing, audio, etc."""
from .image_processor import encode_image, preprocess_image
from .audio import speak_and_save

__all__ = ["encode_image", "preprocess_image", "speak_and_save"]
