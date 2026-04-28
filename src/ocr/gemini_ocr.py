"""Gemini Vision API OCR module"""
import requests
import base64
import time
from src.config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_API_URL


def gemini_ocr(image_path, prompt="Extract all text from this image clearly."):
    """
    Extract text from image using Google Gemini Vision API
    
    Args:
        image_path (str): Path to the image file
        prompt (str): Custom prompt for Gemini (default: extract text)
        
    Returns:
        str: Extracted text from image
        
    Raises:
        ValueError: If API key is invalid or expired
        ConnectionError: If cannot reach Gemini API
        RuntimeError: If API returns an unexpected error
    """
    # ── ENCODE IMAGE TO BASE64 ───
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    
    # ── BUILD REQUEST ───
    url = f"{GEMINI_API_URL}/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": img_b64
                        }
                    }
                ]
            }
        ]
    }
    
    # ── SEND REQUEST ───
    start_time = time.perf_counter()
    response = requests.post(url, json=payload, timeout=30)
    elapsed = time.perf_counter() - start_time
    
    print(f"📡 Gemini Status: {response.status_code}")
    print(f"⏱️  Response Time: {elapsed:.3f}s ({elapsed * 1000:.1f}ms)")
    
    # ── HANDLE ERRORS ───
    if response.status_code != 200:
        try:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "Unknown error")
        except Exception:
            error_msg = response.text
        
        print(f"❌ API Error: {response.text}")
        
        # Raise specific errors so the API endpoint can return proper status codes
        if response.status_code in (401, 403):
            raise ValueError(f"Gemini API key error: {error_msg}")
        elif response.status_code == 400:
            raise ValueError(f"Gemini API error: {error_msg}")
        elif response.status_code == 429:
            raise RuntimeError(f"Gemini rate limit exceeded: {error_msg}")
        else:
            raise RuntimeError(f"Gemini API error ({response.status_code}): {error_msg}")
    
    # ── PARSE RESPONSE ───
    try:
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError("Invalid Gemini API response format — no text found in response")
