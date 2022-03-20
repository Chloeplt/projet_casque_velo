# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
import numpy as np
path="C:\eye.mp4"
cap = cv2.VideoCapture(path)

while True:
    ret, frame = cap.read()
    
    if ret is False:
        break
    
    gray= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7,7), 0)
    rows, cols,_= frame.shape 
    _, threshold = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
    contours ,_ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours= sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)    
    
    for cnt in contours:
        (x, y ,w, h) = cv2.boundingRect(cnt)
        #cv2.drawContours(frame, [cnt], -1, (0, 0,255), 3)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 1)
        cv2.line(frame, (x+int(w/2), 0), (x+int(w/2), rows), (255,0,0), 1)
        
        cv2.line(frame, (0, y+int(h/2)), (cols , y+int(h/2)), (255,0,0), 1)
        break

    
    cv2.imshow("threshold", threshold)
    cv2.imshow("gray", gray)
    cv2.imshow("gray", frame)
    
    key = cv2.waitKey(30)
    if key == 27 :
        break
    
cap.release()
cv2.destroyAllWindows()