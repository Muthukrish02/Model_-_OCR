"""
FastAPI server for AI & OCR Project
3 Endpoints (each with TTS audio response):
  1. POST /api/vlm/scan     → VLM Model (Llama.cpp) — image + command
  2. POST /api/gemini/ocr   → Google Gemini OCR     — image
  3. POST /api/barcode/scan → Local Barcode Scanner  — image
"""
import sys
import time
import os
import uuid
import tempfile
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# Fix Windows console encoding for emoji/unicode
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Import project modules
from src.config import GEMINI_API_KEY, LLAMA_SERVER_PATH, LLAMA_AUTO_START
from src.server_manager import LlamaServerManager
from src.ocr import scan_barcodes, gemini_ocr
from src.ocr.local_ocr import local_ocr
from src.api import LlamaClient
from src.utils.audio import save_text_to_speech


# ── Global state ──
llama_manager = None

# ── Audio output directory ──
AUDIO_DIR = Path("audio_output")
AUDIO_DIR.mkdir(exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global llama_manager

    print("\n" + "=" * 60)
    print("🚀 AI & OCR API Server Starting")
    print("=" * 60)

    # Auto-start Llama server if configured
    if LLAMA_AUTO_START and LLAMA_SERVER_PATH:
        llama_manager = LlamaServerManager(LLAMA_SERVER_PATH)
        if not llama_manager.is_running():
            print("📌 Attempting to start Llama.cpp server...")
            llama_manager.start()

    yield

    # Shutdown
    print("\n🛑 Shutting down AI & OCR API Server")
    if llama_manager:
        llama_manager.stop()


# ── Initialize FastAPI ──
app = FastAPI(
    title="AI & OCR API",
    description="""
## 3 Endpoints for Image Processing (with TTS Audio)

Each endpoint returns a text result **+ audio MP3** of the response.

| # | Endpoint | Input | Backend |
|---|----------|-------|---------|
| 1 | `POST /api/vlm/scan` | Image + Command | Llama.cpp VLM Server |
| 2 | `POST /api/gemini/ocr` | Image | Google Gemini Vision API |
| 3 | `POST /api/barcode/scan` | Image | Local pyzbar Scanner |

### Audio Download
Every response includes an `audio_url` field. Use it to download the MP3:
```
GET /audio/{filename}
```
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Helper: Save uploaded file temporarily ──
def save_temp_file(file: UploadFile) -> str:
    """Save UploadFile to a temp file, return the path"""
    suffix = Path(file.filename).suffix or ".png"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, prefix="ocr_")
    content = file.file.read()
    tmp.write(content)
    tmp.flush()
    tmp.close()
    return tmp.name


# ── Helper: Generate TTS audio from text ──
def generate_tts(text: str, prefix: str = "response") -> str:
    """
    Generate TTS audio file from text.

    Args:
        text: Text to convert to speech
        prefix: Filename prefix (e.g. 'vlm', 'gemini', 'barcode')

    Returns:
        str: Filename of the generated audio (inside AUDIO_DIR)
    """
    filename = f"{prefix}_{uuid.uuid4().hex[:8]}.mp3"
    filepath = AUDIO_DIR / filename

    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='en')
        tts.save(str(filepath))
        print(f"🔊 TTS audio saved: {filename}")
        return filename
    except Exception as e:
        print(f"⚠️  TTS generation failed: {e}")
        return None


# ══════════════════════════════════════════════════════════════
#  AUDIO DOWNLOAD ENDPOINT
# ══════════════════════════════════════════════════════════════

@app.get("/audio/{filename}")
async def download_audio(filename: str):
    """
    ## 🔊 Download TTS Audio

    Download the generated MP3 audio file from any endpoint response.

    ### Usage:
    Use the `audio_url` from any endpoint response.
    """
    # Security: only allow files from AUDIO_DIR, no path traversal
    safe_name = Path(filename).name
    filepath = AUDIO_DIR / safe_name

    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(
        path=str(filepath),
        media_type="audio/mpeg",
        filename=safe_name
    )


# ══════════════════════════════════════════════════════════════
#  ENDPOINT 1 — VLM Model Scan (Llama.cpp Server)
# ══════════════════════════════════════════════════════════════

@app.post("/api/vlm/scan")
async def vlm_scan(
    image: UploadFile = File(..., description="Image file to process"),
    command: str = Form(..., description="Command/prompt for the VLM model (e.g. 'What is in this image?')")
):
    """
    ## 1️⃣ VLM Model Scan (Llama.cpp Server)

    Sends an image + text command to the local Vision-Language Model
    running on Llama.cpp server (port 8080).

    ### Input:
    - **image**: Image file (PNG, JPG, BMP)
    - **command**: Text prompt (e.g. "What is in this image?", "Extract text", "Describe this")

    ### Output:
    - Model's text response + TTS audio

    ### Requires:
    - Llama.cpp server running on `http://localhost:8080`
    """
    tmp_path = None
    try:
        # Check if Llama server is running
        llama_client = LlamaClient()
        if not llama_client.health_check():
            raise HTTPException(
                status_code=503,
                detail="Llama.cpp server is not running. Start it first on port 8080."
            )

        # Save uploaded file
        tmp_path = save_temp_file(image)

        # Process with VLM
        start_time = time.perf_counter()
        result = llama_client.query(tmp_path, command)
        elapsed = (time.perf_counter() - start_time) * 1000

        # Generate TTS audio
        audio_file = generate_tts(result, prefix="vlm")

        return {
            "success": True,
            "endpoint": "vlm_scan",
            "command": command,
            "result": result,
            "processing_time_ms": round(elapsed, 2),
            "audio_url": f"/audio/{audio_file}" if audio_file else None
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"VLM processing error: {str(e)}")
    finally:
        # Clean up temp file
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


# ══════════════════════════════════════════════════════════════
#  ENDPOINT 2 — Google Gemini OCR
# ══════════════════════════════════════════════════════════════

@app.post("/api/gemini/ocr")
async def gemini_ocr_endpoint(
    image: UploadFile = File(..., description="Image file for OCR text extraction")
):
    """
    ## 2️⃣ Google Gemini OCR

    Sends an image to Google Gemini Vision API to extract all text.

    ### Input:
    - **image**: Image file (PNG, JPG, BMP)

    ### Output:
    - Extracted text from the image + TTS audio

    ### Requires:
    - Valid `GEMINI_API_KEY` in `.env` file
    """
    tmp_path = None
    try:
        # Check if Gemini is configured
        if not GEMINI_API_KEY:
            raise HTTPException(
                status_code=400,
                detail="GEMINI_API_KEY not configured in .env file"
            )

        # Save uploaded file
        tmp_path = save_temp_file(image)

        # Process with Gemini
        start_time = time.perf_counter()
        text = gemini_ocr(tmp_path)
        elapsed = (time.perf_counter() - start_time) * 1000

        # Generate TTS audio
        audio_file = generate_tts(text, prefix="gemini")

        return {
            "success": True,
            "endpoint": "gemini_ocr",
            "text": text,
            "processing_time_ms": round(elapsed, 2),
            "audio_url": f"/audio/{audio_file}" if audio_file else None
        }

    except HTTPException:
        raise
    except ValueError as e:
        # API key invalid / expired / leaked
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini OCR error: {str(e)}")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


# ══════════════════════════════════════════════════════════════
#  ENDPOINT 3 — Local Barcode Scanner
# ══════════════════════════════════════════════════════════════

@app.post("/api/barcode/scan")
async def barcode_scan(
    image: UploadFile = File(..., description="Image file to scan for barcodes/QR codes")
):
    """
    ## 3️⃣ Local Barcode / QR Code Scanner

    Scans an image locally using pyzbar to detect barcodes and QR codes.
    No internet required — runs entirely offline.

    ### Input:
    - **image**: Image file (PNG, JPG, BMP)

    ### Output:
    - List of detected barcodes with type and data + TTS audio

    ### No external dependencies:
    - Runs locally using pyzbar
    - Very fast (~50ms)
    """
    tmp_path = None
    try:
        # Save uploaded file
        tmp_path = save_temp_file(image)

        # Scan for barcodes
        start_time = time.perf_counter()
        barcodes = scan_barcodes(tmp_path)
        elapsed = (time.perf_counter() - start_time) * 1000

        # Format barcode results (convert Rect namedtuple to dict)
        barcode_results = []
        for bc in barcodes:
            barcode_results.append({
                "type": bc["type"],
                "data": bc["data"],
                "position": {
                    "left": bc["rect"].left,
                    "top": bc["rect"].top,
                    "width": bc["rect"].width,
                    "height": bc["rect"].height
                }
            })

        # Build TTS text from barcode results
        if barcode_results:
            tts_parts = []
            for i, bc in enumerate(barcode_results, 1):
                tts_parts.append(f"Barcode {i}: type {bc['type']}, data: {bc['data']}")
            tts_text = f"Found {len(barcode_results)} barcode. " + ". ".join(tts_parts)
        else:
            tts_text = "No barcodes found in the image."

        # Generate TTS audio
        audio_file = generate_tts(tts_text, prefix="barcode")

        return {
            "success": True,
            "endpoint": "barcode_scan",
            "barcodes_found": len(barcode_results),
            "barcodes": barcode_results,
            "processing_time_ms": round(elapsed, 2),
            "audio_url": f"/audio/{audio_file}" if audio_file else None
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Barcode scanning error: {str(e)}")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


# ══════════════════════════════════════════════════════════════
#  HEALTH CHECK
# ══════════════════════════════════════════════════════════════

@app.get("/health")
async def health_check():
    """Check which services are available"""
    gemini_ok = bool(GEMINI_API_KEY)

    llama_client = LlamaClient()
    llama_ok = llama_client.health_check()

    return {
        "status": "ok",
        "services": {
            "vlm_model": "✅ Running" if llama_ok else "❌ Not running",
            "gemini_api": "✅ Configured" if gemini_ok else "❌ Not configured",
            "barcode_scanner": "✅ Ready (local)"
        }
    }


# ══════════════════════════════════════════════════════════════
#  ROOT — API Info
# ══════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """API info and endpoint list"""
    return {
        "name": "AI & OCR API",
        "version": "1.0.0",
        "endpoints": {
            "1. VLM Scan":     "POST /api/vlm/scan      → image + command → text + audio",
            "2. Gemini OCR":   "POST /api/gemini/ocr    → image → text + audio",
            "3. Barcode Scan": "POST /api/barcode/scan  → image → barcode data + audio",
            "4. Audio":        "GET  /audio/{filename}  → download MP3",
        },
        "docs": "/docs",
        "health": "/health"
    }


# ══════════════════════════════════════════════════════════════
#  ERROR HANDLERS
# ══════════════════════════════════════════════════════════════

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "details": str(exc)
        }
    )


# ══════════════════════════════════════════════════════════════
#  RUN SERVER
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🚀 Starting AI & OCR FastAPI Server")
    print("=" * 50)
    print("📖 Swagger Docs : http://localhost:8000/docs")
    print("📚 ReDoc        : http://localhost:8000/redoc")
    print("❤️  Health Check : http://localhost:8000/health")
    print("=" * 50)
    print("\n📋 Endpoints:")
    print("   1. POST /api/vlm/scan      → VLM Model (image + command) + 🔊 TTS")
    print("   2. POST /api/gemini/ocr    → Gemini OCR (image) + 🔊 TTS")
    print("   3. POST /api/barcode/scan  → Barcode Scanner (image) + 🔊 TTS")
    print("   4. GET  /audio/{filename}  → Download MP3 audio")
    print()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
