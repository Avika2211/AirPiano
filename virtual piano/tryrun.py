import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Speak now...")
    recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
    try:
        audio = recognizer.listen(source, timeout=5)
        text = recognizer.recognize_google(audio)
        print(f"✅ You said: {text}")
    except sr.UnknownValueError:
        print("❌ ERROR: Could not understand audio (UnknownValueError)")
    except sr.RequestError:
        print("❌ ERROR: Google Speech API unreachable (RequestError)")
    except OSError as e:
        print(f"❌ ERROR: Microphone issue → {e}")
