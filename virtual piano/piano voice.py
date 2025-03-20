import cv2
import numpy as np
import mediapipe as mp
import pygame
import os
import random
import time
import speech_recognition as sr  # 🎤 Voice Recognition
import threading

# 🎵 Initialize Pygame
pygame.init()
pygame.mixer.init()

# 📂 Path for Sound Files
BASE_PATH = r"C:\Users\AVIKA\Desktop\virtual piano"  # 🔥 Change this if needed
WHITE_KEYS = ["C.wav", "D.wav", "E.wav", "F.wav", "G.mp3", "A.wav", "B.wav"]
BLACK_KEYS = ["C#.wav", "D#.mp3", "F#.wav", "G#.wav", "A#.wav"]
ALL_KEYS = WHITE_KEYS + BLACK_KEYS

# 🎵 Load Sounds
sounds = {}
for file in ALL_KEYS:
    path = os.path.join(BASE_PATH, file)
    if not os.path.exists(path):
        print(f"❌ Error: {file} NOT FOUND in {BASE_PATH}!")
        exit()
    try:
        sounds[file] = pygame.mixer.Sound(path)
    except Exception as e:
        print(f"❌ Error loading {file}: {e}")
        exit()

# 🖐️ Mediapipe Hand Tracking
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# 🎥 Webcam Start
cap = cv2.VideoCapture(0)

# 🎤 Speech Recognition Setup
recognizer = sr.Recognizer()

# 🎼 Auto-Play Mode (Sample Tune)
auto_play_notes = ["C.wav", "E.wav", "G.wav", "C.wav", "E.wav", "G.wav"]
auto_play_index = 0
auto_playing = False

# 🎵 Function to Play Sound
def play_sound(note):
    if note in sounds:
        sounds[note].play()
        print(f"🎶 Playing {note}")

# 🎙️ Function to Recognize Speech Commands
def listen_for_commands():
    global auto_playing
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("🎙️ Say a note (C, D, E, etc.) or 'auto play'")
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                
                if command in ["c", "d", "e", "f", "g", "a", "b"]:
                    play_sound(command.upper() + ".wav")
                elif command == "auto play":
                    auto_playing = not auto_playing  # Toggle auto-play mode
                    print("🎼 Auto-Play Mode:", "ON" if auto_playing else "OFF")
        except Exception as e:
            print("🤖 Voice Error:", e)

# 🎶 Start Listening for Commands in a Separate Thread
threading.Thread(target=listen_for_commands, daemon=True).start()

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("❌ Failed to read from camera!")
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # 🖥️ Display Piano Keys
    for i, note in enumerate(ALL_KEYS):
        x1, y1, x2, y2 = (50 + i * 80, 100, 130 + i * 80, 400)  
        color = (255, 255, 255) if i < 7 else (0, 0, 0)  # White or Black Keys
        cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 2)

    # ✋ Hand Tracking Logic
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 8:  # ✅ Index Finger
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

                    # 🎵 Check for Key Press
                    for i, note in enumerate(ALL_KEYS):
                        x1, y1, x2, y2 = (50 + i * 80, 100, 130 + i * 80, 400)
                        if x1 < cx < x2 and y1 < cy < y2:
                            play_sound(note)

    # 🎼 Auto-Play Mode
    if auto_playing:
        if auto_play_index < len(auto_play_notes):
            play_sound(auto_play_notes[auto_play_index])
            auto_play_index += 1
            time.sleep(0.5)  # Delay Between Notes
        else:
            auto_play_index = 0

    cv2.imshow("🎹 Virtual Piano", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # ⏹️ Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
