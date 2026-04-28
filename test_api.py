"""
Test Script for AI & OCR API
Tests all 3 endpoints by uploading actual image files

Usage:
  1. Start the server:  python api_server.py
  2. Run this script:   python test_api.py
"""
import sys
import requests
import json
from pathlib import Path

# Fix Windows console encoding for emoji/unicode
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


BASE_URL = "http://localhost:8000"

# ── Colors for terminal output ──
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(text):
    print(f"\n{'=' * 60}")
    print(f"{BOLD}{CYAN}{text}{RESET}")
    print(f"{'=' * 60}")


def print_result(response):
    """Pretty-print API response"""
    if response.status_code == 200:
        print(f"  {GREEN}✅ Status: {response.status_code}{RESET}")
        data = response.json()
        print(f"  {json.dumps(data, indent=4, ensure_ascii=False)}")
    else:
        print(f"  {RED}❌ Status: {response.status_code}{RESET}")
        try:
            print(f"  {json.dumps(response.json(), indent=4)}")
        except Exception:
            print(f"  {response.text}")


# ══════════════════════════════════════════════════════════════
#  TEST 0: Health Check
# ══════════════════════════════════════════════════════════════

def test_health():
    print_header("🏥 Health Check — GET /health")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_result(response)
        return True
    except requests.exceptions.ConnectionError:
        print(f"  {RED}❌ Cannot connect to server at {BASE_URL}{RESET}")
        print(f"  {YELLOW}   Make sure to run: python api_server.py{RESET}")
        return False


# ══════════════════════════════════════════════════════════════
#  TEST 1: VLM Model Scan (Llama.cpp)
# ══════════════════════════════════════════════════════════════

def test_vlm_scan(image_path):
    print_header("1️⃣  VLM Scan — POST /api/vlm/scan")
    print(f"  📂 Image: {image_path}")
    print(f"  💬 Command: What is in this image?")

    with open(image_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/api/vlm/scan",
            files={"image": (Path(image_path).name, f, "image/png")},
            data={"command": "What is in this image?"}
        )

    print_result(response)
    return response


# ══════════════════════════════════════════════════════════════
#  TEST 2: Gemini OCR
# ══════════════════════════════════════════════════════════════

def test_gemini_ocr(image_path):
    print_header("2️⃣  Gemini OCR — POST /api/gemini/ocr")
    print(f"  📂 Image: {image_path}")

    with open(image_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/api/gemini/ocr",
            files={"image": (Path(image_path).name, f, "image/png")}
        )

    print_result(response)
    return response


# ══════════════════════════════════════════════════════════════
#  TEST 3: Barcode Scanner
# ══════════════════════════════════════════════════════════════

def test_barcode_scan(image_path):
    print_header("3️⃣  Barcode Scan — POST /api/barcode/scan")
    print(f"  📂 Image: {image_path}")

    with open(image_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/api/barcode/scan",
            files={"image": (Path(image_path).name, f, "image/png")}
        )

    print_result(response)
    return response


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════

def main():
    print(f"\n{BOLD}🧪 AI & OCR API — Test Script{RESET}")
    print(f"   Server: {BASE_URL}")

    # Step 0: Health check
    if not test_health():
        sys.exit(1)

    # ── Pick test images ──
    project_dir = Path(__file__).parent

    # Image with text (for VLM + Gemini)
    text_image = project_dir / "test11.png"
    if not text_image.exists():
        # Try any available test image
        for name in ["test5.png", "test4.png", "test3.png", "test2.png", "temp.png"]:
            alt = project_dir / name
            if alt.exists():
                text_image = alt
                break

    # Image with barcode
    barcode_image = project_dir / "testbar.png"

    # ── Run tests ──
    print(f"\n{'─' * 60}")
    print(f"  📁 Text image  : {text_image}")
    print(f"  📁 Barcode image: {barcode_image}")
    print(f"{'─' * 60}")

    results = {}

    # Test 1: VLM Scan
    if text_image.exists():
        try:
            r = test_vlm_scan(str(text_image))
            results["vlm_scan"] = "✅ PASS" if r.status_code == 200 else f"❌ FAIL ({r.status_code})"
        except Exception as e:
            results["vlm_scan"] = f"❌ ERROR: {e}"
    else:
        results["vlm_scan"] = f"⚠️  SKIP (no image: {text_image})"

    # Test 2: Gemini OCR
    if text_image.exists():
        try:
            r = test_gemini_ocr(str(text_image))
            results["gemini_ocr"] = "✅ PASS" if r.status_code == 200 else f"❌ FAIL ({r.status_code})"
        except Exception as e:
            results["gemini_ocr"] = f"❌ ERROR: {e}"
    else:
        results["gemini_ocr"] = f"⚠️  SKIP (no image: {text_image})"

    # Test 3: Barcode Scan
    if barcode_image.exists():
        try:
            r = test_barcode_scan(str(barcode_image))
            results["barcode_scan"] = "✅ PASS" if r.status_code == 200 else f"❌ FAIL ({r.status_code})"
        except Exception as e:
            results["barcode_scan"] = f"❌ ERROR: {e}"
    else:
        results["barcode_scan"] = f"⚠️  SKIP (no image: {barcode_image})"

    # ── Summary ──
    print_header("📊 Test Results Summary")
    for name, status in results.items():
        print(f"  {name:20s} → {status}")

    print()


if __name__ == "__main__":
    main()
