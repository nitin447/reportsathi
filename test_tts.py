import os

from src.voice import speak

os.makedirs("outputs", exist_ok=True)
audio = speak("नमस्ते, यह ReportSathi का एक परीक्षण है।", "Hindi")
with open("outputs/test_hindi.wav", "wb") as f:
    f.write(audio)
print("Saved outputs/test_hindi.wav")