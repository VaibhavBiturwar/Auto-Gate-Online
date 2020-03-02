import cv2
import numpy as np

cap = cv2.VideoCapture(0)

frame = []

while True:
    ret , frame = cap.read()
    cv2.imshow('frame'  ,  frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cap.release()
cv2.imwrite("frame.jpg" , frame)


