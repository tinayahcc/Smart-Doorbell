import RPi.GPIO as GPIO
import time
import requests, urllib.parse
import numpy as np
import io
from PIL import Image
import cv2

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    if GPIO.input(10) == GPIO.LOW:
        print('no one here')
        time.sleep(0.5)
    if GPIO.input(10) == GPIO.HIGH:
        print('someone here')
        time.sleep(0.5)
        
        cap = cv2.VideoCapture(0)
        token = " " # Line Notify Token
        url = 'https://notify-api.line.me/api/notify'
        HEADERS = {'Authorization': 'Bearer ' + token}
        ret, frame = cap.read()
        cv2.imshow('frame',frame)
        ret, frame = cap.read()
        cv2.imwrite('capture.png',frame)
        msg = "someone pushed the doorbell !"
        stickerPackageId = 446
        stickerId = 1990
        img = Image.open('capture.png')
        img.load()
        myimg = np.array(img)
        f = io.BytesIO()
        f = io.BytesIO()
        Image.fromarray(myimg).save(f, 'png')
        data = f.getvalue()
        response = requests.post(url,headers=HEADERS,params={"message": msg,
                                                             "stickerPackageId" : stickerPackageId,
                                                             "stickerId" : stickerId},
                                 files={"imageFile" : data})
        print(response)
