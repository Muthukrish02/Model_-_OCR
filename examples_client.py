#!/usr/bin/env python3
"""
Example: Using the API Client
Demonstrates how to use the OCRAPIClient to call the FastAPI endpoints
"""
import json
import time
from src.api.client import OCRAPIClient


def example_health_check():
    """Example: Check API health"""
    print("\n" + "=" * 60)
    print("📡 Example: Health Check")
    print("=" * 60)
    
    client = OCRAPIClient()
    result = client.health_check()
    print(json.dumps(result, indent=2))


def example_scan_barcode():
    """Example: Scan for barcodes"""
    print("\n" + "=" * 60)
    print("🔍 Example: Barcode Scanning")
    print("=" * 60)
    
    client = OCRAPIClient()
    
    # Update path to your test image
    image_path = r"D:\oraxiz\smartfram\testbar.png"
    
    print(f"\n📂 Scanning: {image_path}")
    result = client.scan_barcode(image_path)
    
    if result.get("success"):
        print(f"✅ Found {result['count']} barcode(s)")
        for i, barcode in enumerate(result.get("barcodes", []), 1):
            print(f"   [{i}] Type: {barcode['type']}")
            print(f"       Data: {barcode['data']}")
        print(f"⏱️  Time: {result['processing_time_ms']:.2f}ms")
    else:
        print(f"❌ Error: {result.get('error')}")


def example_ocr_gemini():
    """Example: OCR with Gemini"""
    print("\n" + "=" * 60)
    print("🤖 Example: OCR with Gemini")
    print("=" * 60)
    
    client = OCRAPIClient()
    
    image_path = r"D:\oraxiz\smartfram\test.png"
    custom_prompt = "Extract all text from this image clearly"
    
    print(f"\n📂 Processing: {image_path}")
    result = client.ocr_gemini(image_path, custom_prompt)
    
    if result.get("success"):
        print("\n📄 Extracted Text:")
        print(result["text"])
        print(f"\n⏱️  Time: {result['processing_time_ms']:.2f}ms")
    else:
        print(f"❌ Error: {result.get('error')}")


def example_ocr_local():
    """Example: OCR with Local VL Model"""
    print("\n" + "=" * 60)
    print("🤖 Example: OCR with Local VL Model")
    print("=" * 60)
    
    client = OCRAPIClient()
    
    image_path = r"D:\oraxiz\smartfram\test.png"
    prompt = "What is in this image?"
    
    print(f"\n📂 Processing: {image_path}")
    result = client.ocr_local(image_path, prompt)
    
    if result.get("success"):
        print("\n📄 Model Response:")
        print(result["text"])
        print(f"\n⏱️  Time: {result['processing_time_ms']:.2f}ms")
    else:
        print(f"❌ Error: {result.get('error')}")


def example_smart_processing():
    """Example: Smart Processing (Recommended)"""
    print("\n" + "=" * 60)
    print("⚡ Example: Smart Processing (Barcode + OCR)")
    print("=" * 60)
    
    client = OCRAPIClient()
    
    image_path = r"D:\oraxiz\smartfram\test.png"
    
    print(f"\n📂 Processing: {image_path}")
    print("🔄 Trying barcode first, then OCR fallback...")
    
    result = client.process_smart(image_path, use_local_model=False)
    
    if result.get("success"):
        source = result["source"]
        
        if source == "barcode":
            print(f"\n✅ Barcodes found:")
            for i, barcode in enumerate(result.get("barcodes", []), 1):
                print(f"   [{i}] {barcode['type']}: {barcode['data']}")
        else:
            print(f"\n📄 OCR Result ({source}):")
            print(result["text"])
        
        print(f"\n⏱️  Time: {result['processing_time_ms']:.2f}ms")
    else:
        print(f"❌ Error: {result.get('error')}")


def example_file_upload():
    """Example: Upload file"""
    print("\n" + "=" * 60)
    print("📤 Example: File Upload")
    print("=" * 60)
    
    client = OCRAPIClient()
    
    # Update path to your test image
    file_path = r"D:\oraxiz\smartfram\test.png"
    
    print(f"\n📂 Uploading: {file_path}")
    result = client.upload_file(file_path)
    
    if result.get("success"):
        print(f"✅ File uploaded successfully")
        print(f"   Path: {result['path']}")
        print(f"   Size: {result['size_bytes']} bytes")
    else:
        print(f"❌ Error: {result.get('error')}")


def example_tts():
    """Example: Text-to-Speech"""
    print("\n" + "=" * 60)
    print("🔊 Example: Text-to-Speech")
    print("=" * 60)
    
    client = OCRAPIClient()
    
    text = "Hello, this is a test message from the OCR API"
    filename = "example_output.mp3"
    
    print(f"\n🗣️  Converting text to speech...")
    result = client.text_to_speech(text, filename)
    
    if result.get("success"):
        print(f"✅ Audio generated: {result['filename']}")
        
        # Optionally download
        print(f"📥 Downloading audio...")
        if client.download_audio(filename, f"downloads/{filename}"):
            print(f"✅ Audio downloaded to: downloads/{filename}")
    else:
        print(f"❌ Error: {result.get('error')}")


def run_all_examples():
    """Run all examples"""
    print("\n🚀 AI & OCR API - Client Examples")
    print("=" * 60)
    print("Make sure the API server is running: python api_server.py\n")
    
    try:
        # Check health first
        example_health_check()
        
        # Uncomment examples to run them
        # example_scan_barcode()
        # example_ocr_gemini()
        # example_ocr_local()
        # example_smart_processing()
        # example_file_upload()
        # example_tts()
        
        print("\n\n✅ Examples completed!")
        print("\nUncomment additional examples in this file to test them.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure the API server is running!")


if __name__ == "__main__":
    run_all_examples()
