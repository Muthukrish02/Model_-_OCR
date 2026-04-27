import requests
import base64
import pyttsx3
import time
import threading
import cv2

# =========================
# 🔊 TTS FUNCTION (SAFE)
# =========================
def speak(text):
    engine = pyttsx3.init('sapi5')  # Windows driver
    engine.setProperty('rate', 180)

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()
    engine.stop()  # 🔥 ensures clean shutdown

# =========================
# 🖼️ IMAGE PREPROCESS
# =========================
img_path = r"D:\oraxiz\smartfram\test11.png"

img = cv2.imread(img_path)
img = cv2.resize(img, (256, 256))  # faster inference
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
                {"type": "text", "text": "What is text in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{img_b64}"
                    }
                }
            ]
        }
    ],
    "max_tokens": 16,
    "temperature": 0.0
}

# =========================
# ⏱️ START TIMER
# =========================
start = time.perf_counter()

# =========================
# 🚀 SEND REQUEST
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
# 🔊 PLAY VOICE (WAIT FULLY)
# =========================
t = threading.Thread(target=speak, args=(result,))
t.start()
t.join()   # 🔥 waits until voice finishes

# =========================
# ⏱️ TIME RESULT
# =========================
print("\n⏱ Total Time:", round(end - start, 3), "sec")

print("\n✅ Program exited cleanly")