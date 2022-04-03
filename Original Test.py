# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
import numpy as np

path="C:\eye.flv" #create a path to locate the file
cap = cv2.VideoCapture(path) #Call cv2.VideoCapture to display the video

while True:
    #ret is a boolean variable that returns true if the frame is available
    #frame is an image array vector captured based on the default frames per second defined explicitly or implicitly
    ret, frame = cap.read() 
    
    if ret is False:
        break
    
    #cv2.cvtColor() is used to convert an image from one color space to another.
    gray= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #cv2.COLOR_BGR2GRAY is used to convert it in gray

    gray = cv2.GaussianBlur(gray, (7,7), 0)   #cv2.gaussianblur() is used to apply Gaussian Smoothing on the input source image
    rows, cols,_= frame.shape   #we save the shape of the frame 
    _, threshold = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)   #cv2.threshold is used to apply the binarization of the video
    
    contours ,_ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #cv2.findContours is used to create a curve joining all the continuous points along the boundary
    contours= sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)   #sorted function sorts the elements of the contours in a specific order and returns it as a list.
    #cv2.contourArea(x) is the lenght of the contours area
    #finding contours is like finding white object from black background, that's why we use the threshold.
    print(contours)
    
    for cnt in contours:
        (x, y ,w, h) = cv2.boundingRect(cnt) #cv2 boundingrect() is used to save the x and y cordinates, the w=width and h=high of the rectangle
        #x and y are taken from the down-left corner of the rectangle. 
        cv2.drawContours(frame, [cnt], -1, (0, 0,255), 3) #draw contours at the frame
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 1) #draw a rectangle arround the contours
        
        #create a 2-axis system with a center in the midle of the previous rectangle
        cv2.line(frame, (x+int(w/2), 0), (x+int(w/2), rows), (255,0,0), 1) 
        cv2.line(frame, (0, y+int(h/2)), (cols , y+int(h/2)), (255,0,0), 1)
        break

    #display the frame, the threshold and the gray 
    cv2.imshow("threshold", threshold)
    cv2.imshow("gray", gray)
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(30)
    if key == 27 :    # if the 27 key is pressed, break from the loop
        break
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows() #cv2.destroyAllWindows() destroys all the created windows 