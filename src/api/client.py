"""
API Client for consuming the FastAPI server
Useful for testing and integration
"""
import requests
import json
from typing import Dict, Optional
from pathlib import Path


class OCRAPIClient:
    """Client for AI & OCR API"""
    
    def __init__(self, base_url="http://localhost:8000"):
        """
        Initialize API client
        
        Args:
            base_url (str): Base URL of the API server
        """
        self.base_url = base_url
    
    def health_check(self) -> Dict:
        """Check API health status"""
        try:
            response = requests.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def scan_barcode(self, image_path: str) -> Dict:
        """Scan for barcodes"""
        payload = {"image_path": image_path}
        try:
            response = requests.post(
                f"{self.base_url}/api/barcode/scan",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def ocr_gemini(self, image_path: str, prompt: Optional[str] = None) -> Dict:
        """Extract text using Gemini"""
        payload = {"image_path": image_path, "prompt": prompt}
        try:
            response = requests.post(
                f"{self.base_url}/api/ocr/gemini",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def ocr_local(self, image_path: str, prompt: Optional[str] = None) -> Dict:
        """Extract text using local VL model"""
        payload = {"image_path": image_path, "prompt": prompt}
        try:
            response = requests.post(
                f"{self.base_url}/api/ocr/local",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_smart(self, image_path: str, use_local_model: bool = False) -> Dict:
        """Smart processing (barcode + OCR)"""
        payload = {"image_path": image_path, "use_local_model": use_local_model}
        try:
            response = requests.post(
                f"{self.base_url}/api/process/smart",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def upload_file(self, file_path: str) -> Dict:
        """Upload an image file"""
        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                response = requests.post(
                    f"{self.base_url}/api/upload",
                    files=files
                )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def text_to_speech(self, text: str, filename: str = "output.mp3") -> Dict:
        """Convert text to speech"""
        payload = {"text": text, "filename": filename}
        try:
            response = requests.post(
                f"{self.base_url}/api/tts",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def download_audio(self, filename: str, save_path: Optional[str] = None) -> bool:
        """Download audio file"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tts/download/{filename}"
            )
            response.raise_for_status()
            
            save_path = save_path or filename
            with open(save_path, "wb") as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"Download error: {str(e)}")
            return False


# Example usage
if __name__ == "__main__":
    print("🚀 OCR API Client Example\n")
    
    client = OCRAPIClient()
    
    # Check health
    print("📡 Health Check:")
    health = client.health_check()
    print(json.dumps(health, indent=2))
    
    # Example endpoints (uncomment to use)
    # result = client.scan_barcode(r"D:\oraxiz\smartfram\testbar.png")
    # print("\nBarcode Result:", json.dumps(result, indent=2))
    
    # result = client.ocr_gemini(r"D:\oraxiz\smartfram\testbar.png")
    # print("\nGemini OCR:", json.dumps(result, indent=2))
