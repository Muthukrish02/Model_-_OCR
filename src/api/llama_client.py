"""Llama.cpp API Client wrapper"""
import requests
import base64
from src.config import LLAMA_SERVER_URL, LLAMA_MODEL_NAME, LLAMA_MAX_TOKENS, LLAMA_TEMPERATURE


class LlamaClient:
    """Client for interacting with Llama.cpp Vision-Language Model server"""
    
    def __init__(self, server_url=LLAMA_SERVER_URL):
        """
        Initialize Llama.cpp client
        
        Args:
            server_url (str): URL of Llama.cpp server
        """
        self.server_url = server_url
        self.model = LLAMA_MODEL_NAME
        self.endpoint = f"{server_url}/v1/chat/completions"
    
    def encode_image(self, image_path):
        """
        Encode image to base64
        
        Args:
            image_path (str): Path to image
            
        Returns:
            str: Base64 encoded image
        """
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    
    def query(self, image_path, prompt="What is this?"):
        """
        Query VL model with image
        
        Args:
            image_path (str): Path to image
            prompt (str): Question/prompt for model
            
        Returns:
            str: Model response
        """
        try:
            img_b64 = self.encode_image(image_path)
            
            payload = {
                "model": self.model,
                "messages": [{
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
                }],
                "max_tokens": LLAMA_MAX_TOKENS,
                "temperature": LLAMA_TEMPERATURE
            }
            
            response = requests.post(self.endpoint, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to Llama.cpp server at {self.server_url}")
            return "Error: Server connection failed"
        except Exception as e:
            print(f"❌ Llama.cpp error: {str(e)}")
            return "Error: Query failed"
    
    def health_check(self):
        """
        Check if server is running
        
        Returns:
            bool: True if server is accessible
        """
        try:
            response = requests.get(f"{self.server_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
