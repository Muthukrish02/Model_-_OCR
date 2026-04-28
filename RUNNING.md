## 🚀 How to Run the AI & OCR Project

### Prerequisites
- Python 3.8 or higher
- Windows PowerShell or Command Prompt
- For Gemini: Google API key
- For Local VL Model: Llama.cpp (optional - can be auto-started)

---

## ✅ Quick Start (2 Options)

### Option A: Auto-Start Llama Server (Recommended)

**Step 1: Run Setup Helper**
```powershell
cd D:\oraxiz\smartfram\AI_and_ocr
python setup_llama.py
```
This will:
- ✅ Find your llama-server installation
- ✅ Update .env automatically
- ✅ Test the configuration

**Step 2: Install Dependencies**
```powershell
pip install -r requirements.txt
```

**Step 3: Run Project**
```powershell
python main.py
```
The Llama server starts automatically! 🎉

---

### Option B: Manual Setup

**Step 1: Install Dependencies**
```powershell
pip install -r requirements.txt
```

**Step 2: Create `.env` File**
```powershell
Copy-Item .env.example .env
notepad .env
```

**Step 3: Configure (Edit `.env`):**
```
GEMINI_API_KEY=your_actual_key

# Path to llama-server executable
LLAMA_SERVER_PATH=C:\llama-b8829-bin-win-cpu-x64\llama-server.exe

# Or disable auto-start
LLAMA_AUTO_START=false
```

**Step 4: Run**
```powershell
python main.py
```

---

## ✅ Quick Start (5 Steps)

### Step 1: Install Dependencies
```powershell
cd D:\oraxiz\smartfram\AI_and_ocr
pip install -r requirements.txt
```

### Step 2: Create `.env` File
```powershell
# Copy the template
Copy-Item .env.example .env

# Open and edit .env with your API key
notepad .env
```

**Edit `.env` and update:**
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
LLAMA_SERVER_URL=http://localhost:8080
```

### Step 3: Verify Installation
```powershell
python -m pip list
```
Check that these are installed:
- `requests` ✅
- `opencv-python` ✅
- `Pillow` ✅
- `pyzbar` ✅
- `gtts` ✅
- `python-dotenv` ✅

### Step 4: Run Main Program
```powershell
python main.py
```

Expected output:
```
🚀 AI & OCR Project - Main Entry Point

✅ Setup complete! Uncomment examples in main.py to run.
```

### Step 5: Process an Image
Edit `main.py` and uncomment the example:

```python
if __name__ == "__main__":
    try:
        validate_config()
        print("🚀 AI & OCR Project - Main Entry Point\n")
        
        # Uncomment this line:
        process_image_smart(r"D:\oraxiz\smartfram\testbar.png")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {str(e)}")
```

Then run:
```powershell
python main.py
```

---

## 🎯 Usage Examples

### Example 1: Barcode Scanning Only
```python
from src.ocr import scan_barcodes

barcodes = scan_barcodes("your_image.png")
for barcode in barcodes:
    print(f"Type: {barcode['type']}")
    print(f"Data: {barcode['data']}")
```

### Example 2: OCR with Gemini
```python
from src.api import GeminiClient

client = GeminiClient()
text = client.extract_text("your_image.png")
print(text)
```

### Example 3: OCR with Local VL Model
```python
from src.api import LlamaClient

client = LlamaClient()
# Make sure Llama.cpp server is running!
result = client.query("your_image.png", "What is in this image?")
print(result)
```

### Example 4: Smart Pipeline (Recommended)
```python
from main import process_image_smart

# Try barcode first, fallback to Gemini
process_image_smart("your_image.png", use_local_model=False)

# Try barcode first, fallback to Local VL Model
process_image_smart("your_image.png", use_local_model=True)
```

### Example 5: Text-to-Speech
```python
from src.utils import speak_and_save

text = "Hello, this is a test message"
speak_and_save(text)  # Saves as output.mp3 and plays
```

---

## 🔧 For Llama.cpp (Local VL Model)

### Automatic Start (Recommended)

The server will start automatically when you run `python main.py` if configured:

```powershell
# Run setup helper (one-time)
python setup_llama.py

# Run project - server starts automatically
python main.py
```

### Manual Start (If Auto-Start Not Working)

Start the server in a separate terminal:
```powershell
cd "C:\path\to\llama-b8829-bin-win-cpu-x64"

# Start server
.\llama-server `
  -hf LiquidAI/LFM2.5-VL-450M-GGUF:Q4_0 `
  -c 2048 `
  --port 8080
```

Expected output:
```
llama server listening on 127.0.0.1:8080
```

Keep this terminal open, then run the project in another terminal:
```powershell
python main.py
```

---

## 🐛 Troubleshooting

### Error: "LLAMA_SERVER_PATH not found"
**Solution:** Run the setup helper:
```powershell
python setup_llama.py
```
This will automatically detect your llama-server installation.

### Error: "Could not auto-start Llama.cpp server"
**Solution:** 
1. Check if LLAMA_SERVER_PATH is correct in .env
2. Verify the file exists:
```powershell
Test-Path "C:\path\to\llama-server.exe"
```
3. Try running manually to see detailed errors

### Error: "ModuleNotFoundError: No module named 'src'"
**Solution:** Make sure you're running from the project root:
```powershell
cd D:\oraxiz\smartfram\AI_and_ocr
python main.py
```

### Error: "GEMINI_API_KEY not set"
**Solution:** Create and edit `.env` file:
```powershell
Copy-Item .env.example .env
notepad .env
# Add: GEMINI_API_KEY=your_key
```

### Error: "Connection refused" for Llama.cpp
**Solution:** Start the Llama.cpp server first:
```powershell
# In a separate terminal
.\llama-server -hf LiquidAI/LFM2.5-VL-450M-GGUF:Q4_0 -c 2048 --port 8080
```

### Error: "pyzbar not working on Windows"
**Solution:** Install system dependency (Zbar):
```powershell
# Option 1: Using Chocolatey
choco install zbar

# Option 2: Manual - Download from:
# https://github.com/ZBar/ZBar/releases
```

---

## 📁 Project Structure Reference

```
AI_and_ocr/
├── main.py                  # Entry point - START HERE
├── .env                     # Your secret keys (create this)
├── requirements.txt         # Dependencies
├── src/
│   ├── config.py           # Settings & environment vars
│   ├── ocr/
│   │   ├── barcode_scanner.py
│   │   ├── gemini_ocr.py
│   │   └── local_ocr.py
│   ├── utils/
│   │   ├── image_processor.py
│   │   └── audio.py
│   └── api/
│       ├── gemini_client.py
│       └── llama_client.py
└── tests/
```

---

## ⚙️ Configuration Reference

Edit `src/config.py` to modify defaults, or set in `.env`:

| Setting | Default | Purpose |
|---------|---------|---------|
| `GEMINI_API_KEY` | From `.env` | Google API key |
| `LLAMA_SERVER_PATH` | `None` | Path to llama-server executable (for auto-start) |
| `LLAMA_SERVER_URL` | `http://localhost:8080` | Local VL model server URL |
| `LLAMA_AUTO_START` | `true` | Whether to auto-start server |
| `IMAGE_SIZE` | `256` | Image resize dimension |
| `LLAMA_MAX_TOKENS` | `21` | Max response length |
| `AUDIO_OUTPUT_FILE` | `output.mp3` | TTS output file |

---

## 🎓 Complete Working Example

Save as `test_example.py`:

```python
#!/usr/bin/env python3
"""Complete working example of the AI & OCR project"""

from main import process_image_smart
from src.api import GeminiClient
from src.utils import speak_and_save

# Update this path to your test image
IMAGE_PATH = r"D:\oraxiz\smartfram\testbar.png"

if __name__ == "__main__":
    print("🚀 Starting AI & OCR Example\n")
    
    # Example 1: Smart processing (barcode + OCR)
    print("=" * 60)
    print("Example 1: Smart Processing")
    print("=" * 60)
    result = process_image_smart(IMAGE_PATH)
    
    # Example 2: Extract text and speak it
    print("\n" + "=" * 60)
    print("Example 2: Extract & Speak")
    print("=" * 60)
    client = GeminiClient()
    text = client.extract_text(IMAGE_PATH, "Extract all text")
    if "Error" not in text:
        speak_and_save(text)
    
    print("\n✅ Examples completed!")
```

Run it:
```powershell
python test_example.py
```

---

## 📱 Next Steps

1. ✅ Install dependencies
2. ✅ Create `.env` file
3. ✅ Update image paths in code
4. ✅ Run `python main.py`
5. ✅ Try the examples

For questions, check the docstrings in each module:
```python
from src.api import GeminiClient
help(GeminiClient.extract_text)  # View documentation
```
