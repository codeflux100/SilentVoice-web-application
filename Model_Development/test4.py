import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import os
import pygame
import time
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# IBM Watson setup
api_key = 'nJmgJFVpWEKxdb8KJaW0AxrdFRmHLpRLL2IzX1SPY9oR'
url = 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/c709be35-e718-4cc8-8d64-0650b9a6c34e'

authenticator = IAMAuthenticator(api_key)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(url)

# Pygame init
pygame.mixer.init()
clock = pygame.time.Clock()

def speak(text, filename='output.mp3'):
    # Retry deletion if locked
    for _ in range(3):
        if os.path.exists(filename):
            try:
                os.remove(filename)
                break
            except PermissionError:
                print(f"Retrying delete: {filename} still in use...")
                time.sleep(0.5)

    # Write new TTS audio
    with open(filename, 'wb') as audio_file:
        response = tts.synthesize(
            text,
            voice='en-US_AllisonV3Voice',
            accept='audio/mp3'
        ).get_result()
        audio_file.write(response.content)

    # Play sound
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(10)
    except Exception as e:
        print("Playback error:", e)

    # Force unload to release file
    pygame.mixer.music.unload()

# Camera & classifier
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("C:/Users/acer/Desktop/converted_keras1/keras_model.h5" , "C:/Users/acer/Desktop/converted_keras1/labels.txt")
offset = 20
imgSize = 300
labels = ["Hello","I Love You","No","Okay","Please","Thank You","Yes"]
last_spoken = None
cooldown = 2
last_spoken_time = 0

while True:
    success, img = cap.read()
    if not success:
        break

    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        aspectRatio = h / w
        try:
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap: wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap: hCal + hGap, :] = imgResize
        except:
            continue

        prediction, index = classifier.getPrediction(imgWhite, draw=False)
        label = labels[index]

        # Cooldown check
        current_time = time.time()
        if label != last_spoken or current_time - last_spoken_time > cooldown:
            speak(label)
            last_spoken = label
            last_spoken_time = current_time

        # Display
        cv2.rectangle(imgOutput, (x - offset, y - offset - 70),
                      (x - offset + 400, y - offset + 60 - 50), (0, 255, 0), cv2.FILLED)
        cv2.putText(imgOutput, label, (x, y - 30),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
        cv2.rectangle(imgOutput, (x - offset, y - offset),
                      (x + w + offset, y + h + offset), (0, 255, 0), 4)

        cv2.imshow('ImageCrop', imgCrop)
        cv2.imshow('ImageWhite', imgWhite)

    cv2.imshow('Image', imgOutput)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
