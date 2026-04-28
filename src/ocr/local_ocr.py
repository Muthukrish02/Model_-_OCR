"""Local Vision-Language Model OCR module using Llama.cpp"""
import requests
import time
from src.config import LLAMA_SERVER_URL, LLAMA_MODEL_NAME, LLAMA_MAX_TOKENS, LLAMA_TEMPERATURE
from src.utils.image_processor import encode_image


def local_ocr(image_path, prompt="What is this?"):
    """
    Extract text/information using local Llama.cpp Vision-Language Model
    
    Args:
        image_path (str): Path to the image file
        prompt (str): Question or prompt for the VL model (default: "What is this?")
        
    Returns:
        str: Model response
    """
    try:
        # ── ENCODE IMAGE ───
        img_b64 = encode_image(image_path)
        
        # ── BUILD REQUEST ───
        url = f"{LLAMA_SERVER_URL}/v1/chat/completions"
        
        payload = {
            "model": LLAMA_MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_b64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": LLAMA_MAX_TOKENS,
            "temperature": LLAMA_TEMPERATURE
        }
        
        # ── SEND REQUEST ───
        start_time = time.perf_counter()
        response = requests.post(url, json=payload)
        elapsed = time.perf_counter() - start_time
        
        print(f"📡 Llama.cpp Status: {response.status_code}")
        print(f"⏱️  Response Time: {elapsed:.3f}s ({elapsed * 1000:.1f}ms)")
        
        # ── PARSE RESPONSE ───
        if response.status_code != 200:
            print(f"❌ Server Error: {response.text}")
            return "No response"
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
        
    except KeyError:
        print("❌ Invalid server response format")
        return "No response"
    except Exception as e:
        print(f"❌ Local OCR error: {str(e)}")
        return "No response"
