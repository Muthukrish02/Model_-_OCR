# AI & OCR API

A Python FastAPI server for image processing with **3 core endpoints** — VLM model scanning, Google Gemini OCR, and local barcode detection. Every response includes a **TTS audio file** (MP3) of the result.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      FastAPI Server (:8000)                   │
│                                                              │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────┐  │
│  │ /api/vlm/scan   │  │ /api/gemini/ocr  │  │ /api/      │  │
│  │ image + command  │  │ image            │  │ barcode/   │  │
│  │                  │  │                  │  │ scan       │  │
│  │      ▼           │  │      ▼           │  │ image      │  │
│  │ Llama.cpp Server │  │ Gemini Vision API│  │      ▼     │  │
│  │ (localhost:8080) │  │ (Google Cloud)   │  │ pyzbar     │  │
│  │      ▼           │  │      ▼           │  │ (local)    │  │
│  │  text + audio    │  │  text + audio    │  │      ▼     │  │
│  └─────────────────┘  └──────────────────┘  │ data+audio │  │
│                                              └────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ /audio/{filename}  →  Download generated MP3 files   │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **API Framework** | FastAPI + Uvicorn |
| **VLM Model** | LiquidAI/LFM2.5-VL-450M-GGUF (via Llama.cpp) |
| **Cloud OCR** | Google Gemini Vision API (`gemini-3-flash-preview`) |
| **Barcode Scanner** | pyzbar (local, offline) |
| **Text-to-Speech** | Google TTS (gTTS) |
| **Image Processing** | OpenCV + Pillow |

---

## Quick Start

### 1. Install Dependencies

```powershell
cd D:\oraxiz\smartfram\AI_and_ocr
pip install -r requirements.txt
```

### 2. Configure Environment

```powershell
Copy-Item .env.example .env
notepad .env
```

Edit `.env`:

```ini
# Required for Gemini OCR endpoint
GEMINI_API_KEY=your_gemini_api_key_here

# Required for VLM endpoint (Llama.cpp server URL)
LLAMA_SERVER_URL=http://localhost:8080

# Optional: auto-start Llama server
LLAMA_SERVER_PATH=C:\path\to\llama-server.exe
LLAMA_AUTO_START=false
```

### 3. Start the API Server

```powershell
python api_server.py
```

Output:

```
🚀 Starting AI & OCR FastAPI Server
==================================================
📖 Swagger Docs : http://localhost:8000/docs
📚 ReDoc        : http://localhost:8000/redoc
❤️  Health Check : http://localhost:8000/health
==================================================

📋 Endpoints:
   1. POST /api/vlm/scan      → VLM Model (image + command) + 🔊 TTS
   2. POST /api/gemini/ocr    → Gemini OCR (image) + 🔊 TTS
   3. POST /api/barcode/scan  → Barcode Scanner (image) + 🔊 TTS
   4. GET  /audio/{filename}  → Download MP3 audio
```

### 4. Open Interactive Docs

Go to **http://localhost:8000/docs** in your browser to test all endpoints visually.

---

## API Endpoints

### Endpoint Overview

| Method | Endpoint | Input | Backend | Auth Required |
|--------|----------|-------|---------|---------------|
| `POST` | `/api/vlm/scan` | Image + Command | Llama.cpp (local) | No |
| `POST` | `/api/gemini/ocr` | Image | Google Gemini API | API Key |
| `POST` | `/api/barcode/scan` | Image | pyzbar (local) | No |
| `GET` | `/audio/{filename}` | Filename | Local filesystem | No |
| `GET` | `/health` | — | — | No |

---

### 1️⃣ `POST /api/vlm/scan` — VLM Model Scan

Sends an image + text command to the local Vision-Language Model running on Llama.cpp.

#### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | `file` | ✅ | Image file (PNG, JPG, BMP) |
| `command` | `string` | ✅ | Text prompt for the model |

**Content-Type:** `multipart/form-data`

#### Example Request

```python
import requests

with open("photo.png", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/vlm/scan",
        files={"image": ("photo.png", f, "image/png")},
        data={"command": "What is in this image?"}
    )

print(response.json())
```

```bash
curl -X POST http://localhost:8000/api/vlm/scan \
  -F "image=@photo.png" \
  -F "command=What is in this image?"
```

#### Response Schema

```json
{
    "success": true,
    "endpoint": "vlm_scan",
    "command": "What is in this image?",
    "result": "The image shows a document with text...",
    "processing_time_ms": 1523.45,
    "audio_url": "/audio/vlm_a1b2c3d4.mp3"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | `boolean` | Whether the request succeeded |
| `endpoint` | `string` | Always `"vlm_scan"` |
| `command` | `string` | The command that was sent |
| `result` | `string` | Model's text response |
| `processing_time_ms` | `float` | Processing time in milliseconds |
| `audio_url` | `string \| null` | URL path to download TTS audio |

#### Error Responses

| Status | Condition |
|--------|-----------|
| `503` | Llama.cpp server is not running on port 8080 |
| `500` | Internal processing error |

#### Prerequisite

Start the Llama.cpp server before using this endpoint:

```powershell
cd llama-b8829-bin-win-cpu-x64
./llama-server -hf LiquidAI/LFM2.5-VL-450M-GGUF:Q4_0 -c 2048 --port 8080
```

---

### 2️⃣ `POST /api/gemini/ocr` — Google Gemini OCR

Sends an image to Google Gemini Vision API to extract all text.

#### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | `file` | ✅ | Image file (PNG, JPG, BMP) |

**Content-Type:** `multipart/form-data`

#### Example Request

```python
import requests

with open("document.png", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/gemini/ocr",
        files={"image": ("document.png", f, "image/png")}
    )

print(response.json())
```

```bash
curl -X POST http://localhost:8000/api/gemini/ocr \
  -F "image=@document.png"
```

#### Response Schema

```json
{
    "success": true,
    "endpoint": "gemini_ocr",
    "text": "Invoice #12345\nDate: 2026-04-28\nTotal: $150.00",
    "processing_time_ms": 2105.32,
    "audio_url": "/audio/gemini_e5f6g7h8.mp3"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | `boolean` | Whether the request succeeded |
| `endpoint` | `string` | Always `"gemini_ocr"` |
| `text` | `string` | Extracted text from the image |
| `processing_time_ms` | `float` | Processing time in milliseconds |
| `audio_url` | `string \| null` | URL path to download TTS audio |

#### Error Responses

| Status | Condition |
|--------|-----------|
| `400` | `GEMINI_API_KEY` not configured in `.env` |
| `401` | API key invalid, expired, or leaked |
| `500` | Internal processing error |

#### Prerequisite

Set `GEMINI_API_KEY` in your `.env` file. Get a key from [Google AI Studio](https://aistudio.google.com/apikey).

---

### 3️⃣ `POST /api/barcode/scan` — Barcode / QR Code Scanner

Scans an image locally for barcodes and QR codes using pyzbar. Runs entirely **offline** — no internet required.

#### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | `file` | ✅ | Image file (PNG, JPG, BMP) |

**Content-Type:** `multipart/form-data`

#### Example Request

```python
import requests

with open("barcode.png", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/barcode/scan",
        files={"image": ("barcode.png", f, "image/png")}
    )

print(response.json())
```

```bash
curl -X POST http://localhost:8000/api/barcode/scan \
  -F "image=@barcode.png"
```

#### Response Schema

```json
{
    "success": true,
    "endpoint": "barcode_scan",
    "barcodes_found": 1,
    "barcodes": [
        {
            "type": "CODE128",
            "data": "oraxiz",
            "position": {
                "left": 18,
                "top": 17,
                "width": 236,
                "height": 75
            }
        }
    ],
    "processing_time_ms": 105.64,
    "audio_url": "/audio/barcode_9d3c8afa.mp3"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | `boolean` | Whether the request succeeded |
| `endpoint` | `string` | Always `"barcode_scan"` |
| `barcodes_found` | `integer` | Number of barcodes detected |
| `barcodes` | `array` | List of detected barcodes |
| `barcodes[].type` | `string` | Barcode type (CODE128, QR_CODE, EAN13, etc.) |
| `barcodes[].data` | `string` | Decoded barcode content |
| `barcodes[].position` | `object` | Barcode location in image (left, top, width, height) |
| `processing_time_ms` | `float` | Processing time in milliseconds |
| `audio_url` | `string \| null` | URL path to download TTS audio |

#### Supported Barcode Types

| Type | Example |
|------|---------|
| `CODE128` | Standard barcodes |
| `CODE39` | Industrial barcodes |
| `EAN13` | Product barcodes |
| `EAN8` | Short product barcodes |
| `QRCODE` | QR codes |
| `PDF417` | 2D barcodes |
| `I25` | Interleaved 2 of 5 |

#### Error Responses

| Status | Condition |
|--------|-----------|
| `500` | Internal scanning error |

---

### 🔊 `GET /audio/{filename}` — Download TTS Audio

Download the MP3 audio file generated by any endpoint.

#### Example

```python
import requests

# 1. Call any endpoint
r = requests.post(
    "http://localhost:8000/api/barcode/scan",
    files={"image": ("barcode.png", open("barcode.png", "rb"), "image/png")}
)
audio_url = r.json()["audio_url"]

# 2. Download the audio
audio = requests.get(f"http://localhost:8000{audio_url}")
with open("result.mp3", "wb") as f:
    f.write(audio.content)
```

```bash
# Direct browser/curl download
curl -o result.mp3 http://localhost:8000/audio/barcode_9d3c8afa.mp3
```

#### Response

| Status | Content-Type | Description |
|--------|-------------|-------------|
| `200` | `audio/mpeg` | MP3 audio file |
| `404` | `application/json` | Audio file not found |

---

### ❤️ `GET /health` — Health Check

Check which backend services are available.

#### Response Schema

```json
{
    "status": "ok",
    "services": {
        "vlm_model": "✅ Running",
        "gemini_api": "✅ Configured",
        "barcode_scanner": "✅ Ready (local)"
    }
}
```

---

## Error Response Format

All error responses follow this schema:

```json
{
    "success": false,
    "error": "Description of what went wrong"
}
```

| Status Code | Meaning |
|-------------|---------|
| `400` | Bad request (missing config, invalid input) |
| `401` | Authentication error (invalid API key) |
| `404` | Resource not found |
| `500` | Internal server error |
| `503` | Service unavailable (Llama server not running) |

---

## Project Structure

```
AI_and_ocr/
├── api_server.py               # FastAPI server (main entry point)
├── main.py                     # CLI entry point
├── test_api.py                 # API test script
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (secrets)
├── .env.example                # Environment template
│
├── src/
│   ├── __init__.py
│   ├── config.py               # Centralized configuration
│   ├── server_manager.py       # Llama.cpp server lifecycle
│   │
│   ├── ocr/
│   │   ├── __init__.py
│   │   ├── barcode_scanner.py  # pyzbar barcode detection
│   │   ├── gemini_ocr.py       # Gemini Vision API client
│   │   └── local_ocr.py        # Llama.cpp VLM client
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── gemini_client.py    # Gemini API wrapper class
│   │   ├── llama_client.py     # Llama.cpp API wrapper class
│   │   ├── client.py           # API consumer client
│   │   └── models.py           # Pydantic models
│   │
│   └── utils/
│       ├── __init__.py
│       ├── image_processor.py  # Image resize & base64 encoding
│       └── audio.py            # TTS (Google Text-to-Speech)
│
├── audio_output/               # Generated TTS audio files
├── llama-b8829-bin-win-cpu-x64/# Llama.cpp binaries
└── tests/
    └── __init__.py
```

---

## Configuration

All settings are loaded from `.env` via `src/config.py`:

| Variable | Default | Required For | Description |
|----------|---------|-------------|-------------|
| `GEMINI_API_KEY` | — | Gemini OCR | Google Gemini API key |
| `LLAMA_SERVER_URL` | `http://localhost:8080` | VLM Scan | Llama.cpp server URL |
| `LLAMA_SERVER_PATH` | — | Auto-start | Path to llama-server executable |
| `LLAMA_AUTO_START` | `true` | Auto-start | Auto-start Llama on server boot |
| `IMAGE_SIZE` | `256` | Image processing | Resize dimension |
| `LOG_LEVEL` | `INFO` | Logging | Log verbosity |

---

## Testing

### Option 1: Swagger UI (Interactive)

Open **http://localhost:8000/docs** — click any endpoint → "Try it out" → upload image → "Execute"

### Option 2: Test Script

```powershell
# Terminal 1: Start the server
python api_server.py

# Terminal 2: Run tests
python test_api.py
```

### Option 3: Python Code

```python
import requests

# ── 1. VLM Scan ──
with open("test11.png", "rb") as f:
    r = requests.post(
        "http://localhost:8000/api/vlm/scan",
        files={"image": ("test11.png", f, "image/png")},
        data={"command": "What is in this image?"}
    )
print("VLM:", r.json())

# ── 2. Gemini OCR ──
with open("test11.png", "rb") as f:
    r = requests.post(
        "http://localhost:8000/api/gemini/ocr",
        files={"image": ("test11.png", f, "image/png")}
    )
print("Gemini:", r.json())

# ── 3. Barcode Scan ──
with open("testbar.png", "rb") as f:
    r = requests.post(
        "http://localhost:8000/api/barcode/scan",
        files={"image": ("testbar.png", f, "image/png")}
    )
print("Barcode:", r.json())

# ── 4. Download Audio ──
audio_url = r.json()["audio_url"]
audio = requests.get(f"http://localhost:8000{audio_url}")
with open("result.mp3", "wb") as f:
    f.write(audio.content)
print(f"Audio saved: {len(audio.content)} bytes")
```

### Option 4: cURL

```bash
# VLM Scan
curl -X POST http://localhost:8000/api/vlm/scan \
  -F "image=@test11.png" \
  -F "command=What is in this image?"

# Gemini OCR
curl -X POST http://localhost:8000/api/gemini/ocr \
  -F "image=@test11.png"

# Barcode Scan
curl -X POST http://localhost:8000/api/barcode/scan \
  -F "image=@testbar.png"

# Health Check
curl http://localhost:8000/health

# Download Audio
curl -o result.mp3 http://localhost:8000/audio/barcode_9d3c8afa.mp3
```

---

## Models Used

### LFM2.5-VL (Vision-Language Model)

| Property | Value |
|----------|-------|
| **Model** | LiquidAI/LFM2.5-VL-450M-GGUF:Q4_0 |
| **Parameters** | ~450M |
| **Format** | GGUF (Q4_0 quantized) |
| **Runtime** | Llama.cpp (CPU, no GPU required) |
| **Task** | Image understanding, text extraction |

### Gemini Vision (Google Cloud)

| Property | Value |
|----------|-------|
| **Model** | gemini-3-flash-preview |
| **Provider** | Google AI Studio |
| **API** | Generative Language API |
| **Task** | OCR text extraction |

---

## Performance

| Endpoint | Speed | Cost | Internet |
|----------|-------|------|----------|
| Barcode Scan | ~50–100ms | Free | ❌ Offline |
| VLM Scan | ~1–3s | Free | ❌ Offline |
| Gemini OCR | ~1–5s | API credits | ✅ Required |

---

## Llama.cpp Setup

### Download

```powershell
# Download pre-built binary (Windows)
# https://github.com/ggerganov/llama.cpp/releases
# File: llama-b8829-bin-win-cpu-x64.zip
```

### Start Server

```powershell
cd llama-b8829-bin-win-cpu-x64
./llama-server -hf LiquidAI/LFM2.5-VL-450M-GGUF:Q4_0 -c 2048 --port 8080
```

### Auto-Setup

```powershell
python setup_llama.py
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `503: Llama.cpp server is not running` | Start llama-server on port 8080 |
| `401: Gemini API key error` | Update `GEMINI_API_KEY` in `.env` with a valid key |
| `400: GEMINI_API_KEY not configured` | Create `.env` file with your API key |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `UnicodeEncodeError` on Windows | Already handled — stdout is reconfigured to UTF-8 |
| `pyzbar` not working | Install ZBar: `choco install zbar` or download from GitHub |

---

## License

MIT License