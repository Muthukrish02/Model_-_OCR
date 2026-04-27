import requests
import base64
import time
import threading
import cv2
from gtts import gTTS
import os

# =========================
# 🔊 TTS SAVE + PLAY
# =========================
def speak_and_save(text, filename="output.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)   # 🔥 save file

    # Play audio (Windows)
    os.system(f"start {filename}")

# =========================
# 🖼️ IMAGE PREPROCESS
# =========================
img_path = r"D:\oraxiz\smartfram\test11.png"

img = cv2.imread(img_path)
img = cv2.resize(img, (256, 256))
cv2.imwrite("temp.png", img)

# =========================
# 🔐 ENCODE IMAGE
# =========================
def encode(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_b64 = encode("temp.png")

# =========================
# 🌐 API CONFIG
# =========================
url = "http://localhost:8080/v1/chat/completions"

data = {
    "model": "LFM2.5-VL",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is this?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{img_b64}"
                    }
                }
            ]
        }
    ],
    "max_tokens": 21,
    "temperature": 0.0
}

# =========================
# ⏱️ START TIMER
# =========================
start = time.perf_counter()

# =========================
# 🚀 REQUEST
# =========================
res = requests.post(url, json=data)

if res.status_code != 200:
    print("❌ ERROR:", res.status_code)
    print(res.text)
    exit()

result = res.json()["choices"][0]["message"]["content"]

# =========================
# ⏱️ END TIMER
# =========================
end = time.perf_counter()

# =========================
# 🧠 OUTPUT
# =========================
print("\n🧠 AI Response:\n", result)

# =========================
# 🔊 SAVE + PLAY AUDIO
# =========================
speak_and_save(result)

# =========================
# ⏱️ TIME
# =========================
print("\n⏱ Total Time:", round(end - start, 3), "sec")

print("\n✅ Audio saved as output.mp3")