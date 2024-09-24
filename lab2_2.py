import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, (140,50,120), (179,255,255))
    onlyRed_frame = cv2.bitwise_and(frame, frame, mask = mask)

    cv2.imshow('RED OBJ', onlyRed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
