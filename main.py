"""
Main entry point for AI & OCR Project
Demonstrates how to use the refactored modules
"""
import time
from src.config import validate_config, LLAMA_SERVER_PATH, LLAMA_AUTO_START, LLAMA_SERVER_URL
from src.server_manager import LlamaServerManager
from src.ocr import scan_barcodes, gemini_ocr
from src.ocr.local_ocr import local_ocr
from src.utils import speak_and_save, preprocess_image
from src.api import GeminiClient, LlamaClient


def initialize_servers():
    """
    Initialize and start Llama.cpp server if configured
    
    Returns:
        LlamaServerManager: Server manager instance or None
    """
    if not LLAMA_AUTO_START:
        print("ℹ️  Auto-start disabled (LLAMA_AUTO_START=false)")
        return None
    
    if not LLAMA_SERVER_PATH:
        print("ℹ️  LLAMA_SERVER_PATH not configured - skipping auto-start")
        print("   To enable auto-start, set LLAMA_SERVER_PATH in .env")
        return None
    
    print("\n" + "=" * 60)
    print("🔧 Initializing Servers")
    print("=" * 60)
    
    manager = LlamaServerManager(LLAMA_SERVER_PATH)
    
    if manager.is_running():
        print(f"✅ Llama.cpp server already running on {LLAMA_SERVER_URL}")
        return manager
    
    print(f"🚀 Starting Llama.cpp server from: {LLAMA_SERVER_PATH}")
    if manager.start():
        print("✅ Llama.cpp server started successfully!")
        return manager
    else:
        print("⚠️  Could not auto-start Llama.cpp server")
        print("   Start it manually or configure LLAMA_SERVER_PATH in .env")
        return None


def process_image_smart(image_path, use_local_model=False):
    """
    Smart image processing pipeline:
    1. Try barcode scanning (fast, local, free)
    2. Fall back to OCR (Gemini or Local VL model)
    
    Args:
        image_path (str): Path to image file
        use_local_model (bool): Use local VL model instead of Gemini
    """
    
    print("=" * 60)
    print(f"📂 Processing: {image_path}")
    print("=" * 60)
    
    overall_start = time.perf_counter()
    
    # ── STEP 1: Try Barcode Scanning ──
    print("\n🔍 Scanning for Barcodes...")
    barcode_start = time.perf_counter()
    barcodes = scan_barcodes(image_path)
    barcode_time = time.perf_counter() - barcode_start
    
    if barcodes:
        print(f"✅ Barcode(s) found in {barcode_time * 1000:.1f}ms!")
        print("\n📊 BARCODE RESULTS:")
        for i, bc in enumerate(barcodes, 1):
            print(f"   [{i}] Type: {bc['type']}")
            print(f"       Data: {bc['data']}")
        
        overall_time = time.perf_counter() - overall_start
        print(f"\n⏱️  Total Time: {overall_time:.3f}s")
        return barcodes
    
    # ── STEP 2: No barcode → Run OCR ──
    print(f"⚠️  No barcode found. Running OCR...")
    
    if use_local_model:
        print("🤖 Using Local VL Model (Llama.cpp)...")
        result = local_ocr(image_path)
    else:
        print("🤖 Using Gemini Vision API...")
        result = gemini_ocr(image_path)
    
    print("\n📄 OCR RESULT:")
    print(result)
    
    overall_time = time.perf_counter() - overall_start
    print(f"\n⏱️  Total Time: {overall_time:.3f}s")
    
    return result


def example_gemini_client():
    """Example: Using GeminiClient directly"""
    print("\n" + "=" * 60)
    print("📌 Example: GeminiClient")
    print("=" * 60)
    
    client = GeminiClient()
    # result = client.extract_text("your_image.png")
    print("✅ GeminiClient is ready to use")


def example_llama_client():
    """Example: Using LlamaClient directly"""
    print("\n" + "=" * 60)
    print("📌 Example: LlamaClient")
    print("=" * 60)
    
    client = LlamaClient()
    is_healthy = client.health_check()
    if is_healthy:
        print("✅ Llama.cpp server is running!")
    else:
        print("⚠️  Llama.cpp server not responding. Make sure it's running.")


if __name__ == "__main__":
    try:
        # Validate configuration
        validate_config()
        
        print("🚀 AI & OCR Project - Main Entry Point\n")
        
        # Initialize and start Llama server if configured
        server_manager = initialize_servers()
        
        # Example 1: Process image with smart routing
        # Uncomment and update image path as needed:
        process_image_smart(r"D:\oraxiz\smartfram\testbar.png")
        
        # Example 2: Use GeminiClient directly
        # example_gemini_client()
        
        # Example 3: Use LlamaClient directly
        # example_llama_client()
        
        print("\n✅ Setup complete! Uncomment examples in main.py to run.")
        
        # Clean up server if started
        if server_manager:
            input("\nPress Enter to stop the server and exit...")
            server_manager.stop()
        
    except ValueError as e:
        print(f"❌ Configuration Error: {str(e)}")
        print("📝 Please create a .env file with GEMINI_API_KEY")
