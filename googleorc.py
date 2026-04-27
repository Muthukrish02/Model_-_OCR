import requests
import base64
import time
from pyzbar.pyzbar import decode
from PIL import Image

API_KEY = "AIzaSyB01GEpA92222lRyMMvzQE1sUXrx99efMA"

def scan_barcodes(image_path):
    """Dedicated barcode scanner using pyzbar"""
    img = Image.open(image_path)
    barcodes = decode(img)
    
    if not barcodes:
        return []
    
    results = []
    for barcode in barcodes:
        results.append({
            "type": barcode.type,
            "data": barcode.data.decode("utf-8"),
            "rect": barcode.rect
        })
    return results


def gemini_ocr(image_path):
    """Gemini Vision for text OCR"""
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Extract all text from this image clearly."},
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

    start_time = time.perf_counter()
    res = requests.post(url, json=payload)
    end_time = time.perf_counter()
    elapsed = end_time - start_time

    print("📡 Gemini Status:", res.status_code)
    print(f"⏱️  Gemini Response Time: {elapsed:.3f}s ({elapsed * 1000:.1f}ms)")

    try:
        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        print("RAW:", res.text)
        return "No text detected"


def process_image(image_path):
    """Smart router — barcode first, Gemini only if no barcode found"""

    overall_start = time.perf_counter()

    print("=" * 50)
    print(f"📂 Processing: {image_path}")
    print("=" * 50)

    # ── STEP 1: Try Barcode First (fast, local, free) ───
    print("\n🔍 Scanning for Barcodes...")
    barcode_start = time.perf_counter()
    barcodes = scan_barcodes(image_path)
    barcode_elapsed = time.perf_counter() - barcode_start

    # ── STEP 2: If barcode found → STOP, skip Gemini ───
    if barcodes:
        overall_elapsed = time.perf_counter() - overall_start
        print(f"✅ Barcode(s) found in {barcode_elapsed * 1000:.1f}ms — Skipping Gemini ⚡")
        print("\n📊 BARCODE RESULTS:")
        for i, bc in enumerate(barcodes, 1):
            print(f"   [{i}] Type : {bc['type']}")
            print(f"       Data : {bc['data']}")
            print(f"       Position: {bc['rect']}")

        print("\n" + "=" * 50)
        print(f"✅ Total Time: {overall_elapsed:.3f}s ({overall_elapsed * 1000:.1f}ms)")
        print("=" * 50)

        return {
            "source": "barcode",
            "barcodes": barcodes,
            "ocr_text": None,
            "total_time_ms": round(overall_elapsed * 1000, 1)
        }

    # ── STEP 3: No barcode → Send to Gemini OCR ────────
    print(f"⚠️  No barcode found ({barcode_elapsed * 1000:.1f}ms) — Sending to Gemini...")
    print("\n🧠 Running Gemini OCR...")
    ocr_result = gemini_ocr(image_path)

    print("\n📄 OCR RESULT:")
    print(ocr_result)

    overall_elapsed = time.perf_counter() - overall_start
    print("\n" + "=" * 50)
    print(f"✅ Total Time: {overall_elapsed:.3f}s ({overall_elapsed * 1000:.1f}ms)")
    print("=" * 50)

    return {
        "source": "gemini_ocr",
        "barcodes": [],
        "ocr_text": ocr_result,
        "total_time_ms": round(overall_elapsed * 1000, 1)
    }


# 🔥 RUN
result = process_image(r"D:\oraxiz\smartfram\testbar.png")

# Access results
print("\n🔁 Source Used:", result["source"])