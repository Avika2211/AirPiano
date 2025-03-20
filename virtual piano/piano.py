import cv2
import numpy as np
import mediapipe as mp
import pygame
import os

# Pygame Initialize
pygame.init()
pygame.mixer.init()

# Correct Path for Sound Files
BASE_PATH = r"C:\Users\AVIKA\Desktop\virtual piano" 
WHITE_KEYS = ["A.wav", "B.wav","C.wav", "D.wav", "E.wav", "F.wav", "G.mp3","A#.wav"]
BLACK_KEYS = ["C#.wav", "D#.mp3", "F#.wav", "G#.wav", "A#.wav"]

# 🎵 Load Sounds with Error Handling
sounds = []
for file in WHITE_KEYS + BLACK_KEYS:
    path = os.path.join(BASE_PATH, file)
    if not os.path.exists(path):
        print(f"Error: {file} NOT FOUND in {BASE_PATH}!")
        exit()
    try:
        sounds.append(pygame.mixer.Sound(path))
    except Exception as e:
        print(f"Error loading {file}: {e}")
        exit()

# Piano Keys (x1, y1, x2, y2)
white_keys = [(50 + i * 80, 100, 130 + i * 80, 400) for i in range(8)]  # 7 White Keys
black_keys = [(110 + i * 80, 100, 150 + i * 80, 300) for i in range(5) if i not in [2, 5]]  # 5 Black Keys

# Mediapipe Hand Tracking Setup
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Webcam Start
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print(" Failed to read from camera!")
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Draw White Keys
    for x1, y1, x2, y2 in white_keys:
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), -1)  # White keys
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 2)  # Border

    # Draw Black Keys
    for x1, y1, x2, y2 in black_keys:
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), -1)  # Black keys

    # Reset Key States
    pressed_keys = [False] * len(sounds)

    #  Hand Tracking Logic
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            #  Detect Multiple Fingers
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id in [8, 12, 16, 20]:  #  Index, Middle, Ring, Pinky
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

                    # Check White Keys
                    for i, (x1, y1, x2, y2) in enumerate(white_keys):
                        if x1 < cx < x2 and y1 < cy < y2 and not pressed_keys[i]:
                            print(f" Playing White Note {i+1}")
                            sounds[i].play()
                            pressed_keys[i] = True
                            cv2.rectangle(img, (x1, y1), (x2, y2), (200, 200, 200), -1)  # Highlight key

                    # Check Black Keys
                    for i, (x1, y1, x2, y2) in enumerate(black_keys):
                        if x1 < cx < x2 and y1 < cy < y2 and not pressed_keys[i + 7]:
                            print(f" Playing Black Note {i+1}")
                            sounds[i + 7].play()
                            pressed_keys[i + 7] = True
                            cv2.rectangle(img, (x1, y1), (x2, y2), (50, 50, 50), -1)  # Highlight key

    cv2.imshow("Virtual Piano", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  #  Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
