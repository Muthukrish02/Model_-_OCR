"""Gemini API Client wrapper"""
import requests
import base64
from src.config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_API_URL


class GeminiClient:
    """Client for interacting with Google Gemini Vision API"""
    
    def __init__(self, api_key=GEMINI_API_KEY):
        """
        Initialize Gemini client
        
        Args:
            api_key (str): Google Gemini API key
        """
        self.api_key = api_key
        self.model = GEMINI_MODEL
        self.base_url = GEMINI_API_URL
    
    def extract_text(self, image_path, prompt="Extract all text from this image clearly."):
        """
        Extract text from image
        
        Args:
            image_path (str): Path to image
            prompt (str): Custom prompt
            
        Returns:
            str: Extracted text
        """
        try:
            with open(image_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": img_b64
                            }
                        }
                    ]
                }]
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
            
        except Exception as e:
            print(f"❌ Gemini error: {str(e)}")
            return "Error: Could not extract text"
    
    def analyze_image(self, image_path, custom_prompt):
        """
        Analyze image with custom prompt
        
        Args:
            image_path (str): Path to image
            custom_prompt (str): Custom analysis prompt
            
        Returns:
            str: Analysis result
        """
        return self.extract_text(image_path, custom_prompt)
