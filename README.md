# AI & OCR Project

Two Python scripts for image text extraction and OCR processing.

## Files Overview

| File | Purpose |
|------|---------|
| `googleorc.py` | Barcode scanning + Gemini Vision OCR |
| `test.py` | Local VL model OCR with text-to-speech |

---

## Prerequisites

### Install Dependencies

```powershell
pip install requests pyttsx3 opencv-python pyzbar pillow
```

### Additional Requirements

- **googleorc.py**: Valid Google Gemini API key
- **test.py**: Local server running at `http://localhost:8080`

---

## googleorc.py

### What It Does

1. **Barcode Scanner** — Uses `pyzbar` to detect barcodes/QR codes (fast, local, free)
2. **Gemini OCR** — Falls back to Google Gemini Vision if no barcodes found

### How to Run

```powershell
python googleorc.py
```

### Configuration

Edit these variables in the script:

```python
API_KEY = "YOUR_GEMINI_API_KEY"          # Line 7
image_path = r"D:\path\to\your\image.png" # Line 97
```

### Sample Output

```
📂 Processing: D:\path\to\image.png
🔍 Scanning for Barcodes...
✅ Barcode(s) found in 45.2ms — Skipping Gemini ⚡
   [1] Type : QRCODE
       Data : https://example.com
```

---

## test.py

### What It Does

1. Reads and resizes an image to 256×256
2. Encodes image to base64
3. Sends to local VL model API (`http://localhost:8080`)
4. Speaks the OCR result using Windows TTS

### How to Run

```powershell
python test.py
```

### Configuration

Edit these variables in the script:

```python
img_path = r"D:\oraxiz\smartfram\test11.png"  # Line 17
url = "http://localhost:8080/v1/chat/completions"  # Line 29
```

### Sample Output

```
🧠 AI Response: Hello World

🔊 [TTS speaks the result]

⏱ Total Time: 2.345 sec

✅ Program exited cleanly
```

---

## How It Works

### googleorc.py Flowchart

```
┌─────────────────┐
│  Load Image     │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Scan Barcodes  │ ──► pyzbar.decode()
└────────┬────────┘
         ▼
    ┌────┴────┐
    │ Barcode  │
    │ Found?   │
    └────┬────┘
   Yes   │   No
    ▼    ▼    ▼
 STOP   │  Gemini Vision
        │   OCR
        ▼
┌─────────────────┐
│  Return Result  │
└─────────────────┘
```

### test.py Flowchart

```
┌─────────────────┐
│  Load & Resize  │ ──► cv2.resize(256,256)
└────────┬────────┘
         ▼
┌─────────────────┐
│  Base64 Encode  │
└────────┬────────┘
         ▼
┌─────────────────┐
│  POST to API    │ ──► localhost:8080
└────────┬────────┘
         ▼
┌─────────────────┐
│  Extract Text   │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Speak (TTS)    │ ──► pyttsx3
└─────────────────┘
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install` for missing package |
| `API key invalid` | Replace `API_KEY` in googleorc.py |
| `Connection refused` | Start local VL server on port 8080 |
| `No text detected` | Check image path and API response |

---

## License

MIT License