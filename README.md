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
- **test.py**: llama.cpp server running on port 8080

---

## Install llama.cpp

### Step 1: Download llama.cpp

```powershell
# Option 1: Download pre-built binary (Windows)
# Visit: https://github.com/ggerganov/llama.cpp/releases
# Download: llama-b8829-bin-win-cpu-x64.zip

# Option 2: Clone and build from source
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
cmake -B build
cmake --build build --config Release
```

### Step 2: Verify Installation

```powershell
# Check if llama-server is available
./llama-server --version
```

---

## Run the Server

### Start VL Model Server

```powershell
# From llama-b8829-bin-win-cpu-x64 folder
./llama-server ^
  -hf LiquidAI/LFM2.5-VL-450M-GGUF:Q4_0 ^
  -c 2048 ^
  --port 8080
```

| Parameter | Description |
|-----------|-------------|
| `-hf` | HuggingFace model ID |
| `-c 2048` | Context length (tokens) |
| `--port 8080` | Server port |

### Expected Output

```
llama server listening on 127.0.0.1:8080
```

---

## Install Python Requirements

### Option 1: Using requirements.txt (Recommended)

```powershell
pip install -r requirements.txt
```

### Option 2: Manual Install

```powershell
pip install requests pyttsx3 opencv-python pyzbar pillow
```

| Package | Purpose |
|---------|---------|
| `requests` | HTTP API calls |
| `pyttsx3` | Text-to-speech |
| `opencv-python` | Image processing |
| `pyzbar` | Barcode detection |
| `PIL` | Image loading |

---

## Running test.py

### Prerequisites

1. ✅ llama.cpp server running on port 8080
2. ✅ Python dependencies installed
3. ✅ Image file exists at specified path

### Step 1: Start the Server (Terminal 1)

```powershell
# In llama-b8829-bin-win-cpu-x64 folder
./llama-server ^
  -hf LiquidAI/LFM2.5-VL-450M-GGUF:Q4_0 ^
  -c 2048 ^
  --port 8080
```

### Step 2: Run the Script (Terminal 2)

```powershell
# In AI_and_ocr folder
python test.py
```

### Configuration

Edit these variables in the script:

```python
img_path = r"D:\oraxiz\smartfram\test11.png"  # Line 17
url = "http://localhost:8080/v1/chat/completions"  # Line 29
```

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

**Step 1: Start the VL model server**

```powershell
# Download llama.cpp → Load GGUF model → Pass image + prompt → Generate output
./llama-cli ^
  -hf LiquidAI/LFM2.5-VL-450M-GGUF:Q4_0 ^
  --image test1.png ^
  -p "What's in this image?"
```

**Step 2: Run the Python script**

```powershell
python test.py
```

### Configuration

Edit these variables in the script:

```python
img_path = r"D:\oraxiz\smartfram\test11.png"  # Line 17
url = "http://localhost:8080/v1/chat/completions"  # Line 29
```

### How It Works

The script communicates with a local VL model server running via llama.cpp:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  test.py       │────▶│  localhost:8080  │────▶│  llama.cpp     │
│  (base64 img)  │     │  (API server)    │     │  (VL model)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  OCR Text       │
                                               └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  pyttsx3 (TTS)  │
                                               └─────────────────┘
```

### Running with llama.cpp

**Step 1: Download and run the VL model**

```powershell
# From llama-b8829-bin-win-cpu-x64 folder
./llama-cli ^
  -hf LiquidAI/LFM2.5-VL-450M-GGUF:Q4_0 ^
  --image ..\test1.png ^
  -p "What's in this image?"
```

**Step 2: Run the Python script**

```powershell
python test.py
```

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

---

# Additional Details

## Models Used

### 1. LFM2.5-VL (Vision Language Model)

| Property | Value |
|----------|-------|
| **Model** | LiquidAI/LFM2.5-VL-450M-GGUF:Q4_0 |
| **Size** | ~450M parameters |
| **Format** | GGUF (Quantized Q4_0) |
| **Type** | Vision Language Model |
| **Task** | Image OCR + Text extraction |

**Why Q4_0 quantization?**
- Reduces model size by ~50%
- Runs on CPU without GPU
- Minimal accuracy loss

### 2. Gemini Vision (Google Cloud)

| Property | Value |
|----------|-------|
| **Model** | gemini-3-flash-preview |
| **Provider** | Google AI Studio |
| **API** | Generative Language API |
| **Type** | Cloud-based Vision |

---

## What is llama.cpp?

### Overview

**llama.cpp** is a C++ implementation of LLaMA (Large Language Model Architecture) by Georgi Gerganov. It enables running LLM models locally on consumer hardware.

### Key Features

- **Pure C++** — No Python dependencies
- **CPU-only** — Runs on any CPU (no GPU required)
- **GGUF format** — Optimized quantized model files
- **Fast inference** — BLAS acceleration support
- **Cross-platform** — Windows, Linux, macOS

### Why Use llama.cpp?

| Benefit | Description |
|---------|-------------|
| **Privacy** | Data stays local — no cloud uploads |
| **Cost** | Free — no API fees |
| **Offline** | Works without internet |
| **Control** | Full parameter control |
| **Speed** | BLAS-optimized inference |

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                                │
│                     (Image + Prompt)                             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      test.py                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ cv2.imread  │→│ base64      │→│ requests    │             │
│  │ (256x256)   │  │ encode      │  │ .post()    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP POST (base64)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  localhost:8080                                 │
│                  (API Server)                                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              llama.cpp (LFM2.5-VL Model)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ Load GGUF   │→│ Vision      │→│ Generate    │             │
│  │ Model       │  │ Encoder     │  │ Response    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└──────────────────────────┬──────────────────────────────────────┘
                           │ JSON Response
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      test.py                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ Parse JSON  │→│ pyttsx3     │→│ Audio Output│             │
│  │ (OCR Text)  │  │ (TTS Engine)│  │ (Speech)    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

### googleorc.py Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                                │
│                     (Image File)                                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    googleorc.py                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              STEP 1: Barcode Scanner                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │   │
│  │  │ PIL.Image   │→│ pyzbar      │→│ Decode      │       │   │
│  │  │ .open()    │  │ .decode()   │  │ Barcodes    │       │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                    ┌──────┴──────┐                              │
│                    │ Barcode     │                              │
│                    │ Found?       │                              │
│                    └──────┬──────┘                              │
│                 Yes       │       No                            │
│                  ┌────────┘    ┌────────┘                       │
│                  ▼             ▼                                 │
│           ┌──────────┐   ┌────────────────────────────────┐      │
│           │ RETURN   │   │ STEP 2: Gemini Vision OCR     │      │
│           │ Result   │   │  ┌─────────────┐  ┌─────────┐ │      │
│           └──────────┘   │  │ base64     │→│ POST    │ │      │
│                           │  │ encode     │  │ to API │ │      │
│                           │  └─────────────┘  └─────────┘ │      │
│                           │        │            │        │      │
│                           │        ▼            ▼        │      │
│                           │  ┌─────────────┐  ┌─────────┐ │      │
│                           │  │ Gemini     │←│ Parse   │ │      │
│                           │  │ Response   │  │ JSON    │ │      │
│                           │  └─────────────┘  └─────────┘ │      │
│                           │        │                        │      │
│                           │        ▼                        │      │
│                           │   ┌──────────┐                  │      │
│                           │   │ RETURN   │                  │      │
│                           │   │ Result   │                  │      │
│                           │   └──────────┘                  │      │
│                           └────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Comparison

| Script | Input | Processing | Output |
|--------|-------|-------------|--------|
| `test.py` | Image file | VL model (llama.cpp) | Text + TTS |
| `googleorc.py` | Image file | Barcode → Gemini fallback | Text / Barcode data |

---

## API Endpoints

### test.py API Call

```python
url = "http://localhost:8080/v1/chat/completions"

payload = {
    "model": "LFM2.5-VL",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is text in this image?"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
            ]
        }
    ],
    "max_tokens": 16,
    "temperature": 0.0
}
```

### googleorc.py API Call

```python
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={API_KEY}"

payload = {
    "contents": [
        {
            "parts": [
                {"text": "Extract all text from this image clearly."},
                {"inline_data": {"mime_type": "image/png", "data": img_b64}}
            ]
        }
    ]
}
```

---

## Performance Comparison

| Metric | googleorc.py (Barcode) | googleorc.py (Gemini) | test.py (LFM2.5-VL) |
|--------|------------------------|------------------------|---------------------|
| **Speed** | ~50ms | ~2-5s | ~1-3s |
| **Cost** | Free | API credits | Free |
| **Accuracy** | 100% (barcodes) | High | Medium |
| **Internet** | Not required | Required | Not required |
| **Hardware** | CPU only | Cloud | CPU (local)