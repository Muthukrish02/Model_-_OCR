# 🚀 FastAPI Integration - API Endpoints

## Quick Start

### 1. Install FastAPI Dependencies
```powershell
pip install fastapi uvicorn[standard]
```

### 2. Start the API Server
```powershell
python api_server.py
```

### 3. Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000

---

## 📋 Available Endpoints

### 1. Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "gemini_configured": true,
  "llama_server_running": false,
  "services": {
    "gemini": "✅ Configured",
    "llama": "❌ Not running"
  }
}
```

---

### 2. Barcode Scanning
```
POST /api/barcode/scan
```

**Request:**
```json
{
  "image_path": "D:\\oraxiz\\smartfram\\testbar.png"
}
```

**Response:**
```json
{
  "success": true,
  "source": "barcode",
  "barcodes": [
    {
      "type": "CODE128",
      "data": "123456789",
      "rect": {"x": 10, "y": 20, "width": 100, "height": 50}
    }
  ],
  "count": 1,
  "processing_time_ms": 45.32
}
```

---

### 3. OCR with Gemini
```
POST /api/ocr/gemini
```

**Request:**
```json
{
  "image_path": "D:\\oraxiz\\smartfram\\test.png",
  "prompt": "Extract all text from this image"
}
```

**Response:**
```json
{
  "success": true,
  "source": "gemini_ocr",
  "text": "Extracted text from image...",
  "processing_time_ms": 1234.56
}
```

---

### 4. OCR with Local VL Model
```
POST /api/ocr/local
```

**Request:**
```json
{
  "image_path": "D:\\oraxiz\\smartfram\\test.png",
  "prompt": "What is in this image?"
}
```

**Response:**
```json
{
  "success": true,
  "source": "local_ocr",
  "text": "Model response...",
  "processing_time_ms": 2345.67
}
```

**Note:** Llama.cpp server must be running!

---

### 5. Smart Processing (Recommended)
```
POST /api/process/smart
```

**Workflow:**
1. Tries barcode scanning first (fast, local)
2. If no barcode found, runs OCR (Gemini or Local)

**Request:**
```json
{
  "image_path": "D:\\oraxiz\\smartfram\\test.png",
  "use_local_model": false,
  "prompt": "Extract text"
}
```

**Response (with barcode):**
```json
{
  "success": true,
  "source": "barcode",
  "barcodes": [...],
  "processing_time_ms": 123.45
}
```

**Response (with OCR):**
```json
{
  "success": true,
  "source": "gemini_ocr",
  "text": "Extracted text...",
  "processing_time_ms": 1234.56
}
```

---

### 6. File Upload
```
POST /api/upload
```

**Request (multipart/form-data):**
- Form field: `file` (binary image)

**Response:**
```json
{
  "success": true,
  "filename": "image.png",
  "path": "uploads/image.png",
  "size_bytes": 51234
}
```

---

### 7. Text-to-Speech
```
POST /api/tts
```

**Request:**
```json
{
  "text": "Hello, this is a test message",
  "filename": "greeting.mp3"
}
```

**Response:**
```json
{
  "success": true,
  "filename": "greeting.mp3",
  "message": "Audio saved as greeting.mp3"
}
```

---

### 8. Download TTS Audio
```
GET /api/tts/download/{filename}
```

**Example:**
```
GET /api/tts/download/output.mp3
```

Returns the MP3 file for download.

---

## 🧪 Testing Endpoints

### Using cURL

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Barcode Scan:**
```bash
curl -X POST http://localhost:8000/api/barcode/scan \
  -H "Content-Type: application/json" \
  -d "{\"image_path\": \"D:\\\\oraxiz\\\\smartfram\\\\testbar.png\"}"
```

**Smart Processing:**
```bash
curl -X POST http://localhost:8000/api/process/smart \
  -H "Content-Type: application/json" \
  -d "{\"image_path\": \"D:\\\\oraxiz\\\\smartfram\\\\test.png\", \"use_local_model\": false}"
```

### Using Python Requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Scan barcode
response = requests.post(
    "http://localhost:8000/api/barcode/scan",
    json={"image_path": "D:\\oraxiz\\smartfram\\testbar.png"}
)
print(response.json())

# Smart processing
response = requests.post(
    "http://localhost:8000/api/process/smart",
    json={
        "image_path": "D:\\oraxiz\\smartfram\\test.png",
        "use_local_model": False
    }
)
print(response.json())
```

### Using Python API Client

```python
from src.api.client import OCRAPIClient

# Initialize client
client = OCRAPIClient("http://localhost:8000")

# Health check
print(client.health_check())

# Scan barcode
result = client.scan_barcode("D:\\oraxiz\\smartfram\\testbar.png")
print(result)

# Gemini OCR
result = client.ocr_gemini("D:\\oraxiz\\smartfram\\test.png")
print(result)

# Smart processing
result = client.process_smart("D:\\oraxiz\\smartfram\\test.png")
print(result)

# Text-to-speech
result = client.text_to_speech("Hello, World!")
print(result)
```

---

## 🔒 Production Deployment

### Using Gunicorn + Nginx

```bash
# Install gunicorn
pip install gunicorn

# Run with Gunicorn (multiple workers)
gunicorn -w 4 -b 0.0.0.0:8000 api_server:app
```

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "api_server.py"]
```

Build and run:
```bash
docker build -t ocr-api .
docker run -p 8000:8000 ocr-api
```

---

## ⚙️ Configuration

### Update Port
Edit `api_server.py`:
```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=9000,  # Change port
    log_level="info"
)
```

### Enable HTTPS
```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,
    ssl_keyfile="/path/to/key.pem",
    ssl_certfile="/path/to/cert.pem"
)
```

---

## 📊 API Response Format

All successful responses include:
```json
{
  "success": true,
  "data": {...},
  "processing_time_ms": 123.45
}
```

All error responses include:
```json
{
  "success": false,
  "error": "Error message",
  "details": "Additional details"
}
```

---

## 🔗 API Routes Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/api/barcode/scan` | Scan barcodes |
| POST | `/api/ocr/gemini` | OCR with Gemini |
| POST | `/api/ocr/local` | OCR with local VL model |
| POST | `/api/process/smart` | Smart processing |
| POST | `/api/upload` | Upload image file |
| POST | `/api/tts` | Convert text to speech |
| GET | `/api/tts/download/{filename}` | Download audio |

---

## 💡 Tips

1. **Always check health first**: Call `/health` to verify service status
2. **Use smart processing**: `/api/process/smart` is the most efficient
3. **Upload files**: Use `/api/upload` for files on client machine
4. **Batch processing**: Send multiple requests with different images
5. **Error handling**: Check `success` field before using data

---

## 🐛 Troubleshooting

### API Won't Start
```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID [PID] /F
```

### 503 Service Unavailable
- Gemini: Check `GEMINI_API_KEY` in `.env`
- Llama: Ensure server is running (`python setup_llama.py`)

### Timeout Issues
- Increase uvicorn timeout:
```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,
    timeout_keep_alive=75
)
```

---

## 📚 Additional Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [Uvicorn](https://www.uvicorn.org/)
