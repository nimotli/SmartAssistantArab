# -*- coding: utf-8 -*-
import numpy as np
import cv2
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def cleanText(text):
    finaltext=""
    for char in text:
        if char.isalpha() or char == " " or char == "\n":
            finaltext=finaltext+char
    return finaltext
def readText():
    readText=False
    waitTime=5
    minChars=100

    oldTime=time.time()+waitTime
    willPredict=False
    resultText=""
    cap = cv2.VideoCapture(0)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3)
        if (time.time() >= oldTime+waitTime and willPredict==False):
            oldTime=time.time() 
            willPredict=True
        if willPredict:
            result = pytesseract.image_to_string(gray,lang="ara")
            charLen=len(result)
            if charLen==0:
                print("looking for text to read ..")
            else:
                print("the lenght of the predicted text is :",charLen,"it needs to be at least 200")
            if(len(result) >= minChars):
                result =cleanText(result)
                willPredict=False
                oldTime=time.time()+waitTime
                resultText=result
                readText=True
        # Display the resulting frame
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            willPredict=False
            break
    cap.release()
    cv2.destroyAllWindows()
    if readText:
        return resultText
    else:
        return 0