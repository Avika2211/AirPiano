import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Speak something...")
    recognizer.adjust_for_ambient_noise(source)  # Reduce noise
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print(f"✅ You said: {text}")
except sr.UnknownValueError:
    print("❌ Could not understand audio")
except sr.RequestError:
    print("❌ Could not request results, check internet")
