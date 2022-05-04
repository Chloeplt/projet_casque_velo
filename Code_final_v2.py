# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 17:41:54 2022

@author: chloe
"""

import cv2
import numpy as np
from statistics import multimode

path=r"C:\Users\chloe\Desktop\Casque_velo\test_12.mp4"#create a path to locate the file
cap = cv2.VideoCapture(path) #Call cv2.VideoCapture to display the video
path1=r"C:\Users\chloe\Desktop\Casque_velo\test_13.mp4" #create a path for the measuring the center of eyes
test_cent = cv2.VideoCapture(path1) #display the video

#function to calculate the distance from the eye_center
def dist_from_center(x, y, eye_center):
    dist = np.array([eye_center[0] - x, eye_center[1]-y])
    return dist

#function to calculate if the distance between the pupil and the eye_center is lagre enough (we define N) 
#to say that the kid looks elsewhere 
def looking_elsewhere(dist, N):
    if abs(dist[0])<N : # we use all() to test every cordinate
        a=False
    elif abs(dist[1])<N:
        a=False
    else:
        a=True
    return a

#function to return the most frequent value of an array
def MostFreqValue(array):
    mfv = multimode(array)
    return mfv

#function to display a video to capture the cordinates of the eye_center->pupil_center
def center_eye():
    eye_cord = np.array([])
    while True:
        ret1, frame1 = test_cent.read()
        
        if ret1 is False:
            break
        gray1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY) #cv2.COLOR_BGR2GRAY is used to convert it in gray

        gray1 = cv2.GaussianBlur(gray1, (7,7), 0)   #cv2.gaussianblur() is used to apply Gaussian Smoothing on the input source image
        row, col,_= frame1.shape   #we save the shape of the frame 
        _, threshold1 = cv2.threshold(gray1, 15, 255, cv2.THRESH_BINARY_INV)   #cv2.threshold is used to apply the binarization of the video
        
        contours1 ,_ = cv2.findContours(threshold1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #cv2.findContours is used to create a curve joining all the continuous points along the boundary
        contours1= sorted(contours1, key=lambda x: cv2.contourArea(x), reverse=True)   #sorted function sorts the elements of the contours in a specific order and returns it as a list.
        #cv2.contourArea(x) is the lenght of the contours area
        #finding contours is like finding white object from black background, that's why we use the threshold.
        #print(contours)
        
        for cnt in contours1:
            (xc, yc ,wc, hc) = cv2.boundingRect(cnt) #cv2 boundingrect() is used to save the x and y cordinates, the w=width and h=high of the rectangle
            #x and y are taken from the down-left corner of the rectangle. 
            
            a = np.array([]) #array to calculate save the cordinates of the eye_center
            eye_cord=np.append(a, [xc+int(wc/2), yc+int(hc/2)])
            print(eye_cord)
            break
    return eye_cord

#call the function center_eye and save the array with the values of the center of the eye
eye_cords=np.array(center_eye())
#call MostFreqValue and get the most fruent value of the previous array, which is the center 
eye_center = MostFreqValue(eye_cords);
print("\nThe cordinates of the eye when it is looking straight are:", eye_center) #print the cordinates of the center

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
    _, threshold = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY_INV)   #cv2.threshold is used to apply the binarization of the video
    
    contours ,_ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #cv2.findContours is used to create a curve joining all the continuous points along the boundary
    contours= sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)   #sorted function sorts the elements of the contours in a specific order and returns it as a list.
    #cv2.contourArea(x) is the lenght of the contours area
    #finding contours is like finding white object from black background, that's why we use the threshold.
    #print(contours)
    
    for cnt in contours:
        (x, y ,w, h) = cv2.boundingRect(cnt) #cv2 boundingrect() is used to save the x and y cordinates, the w=width and h=high of the rectangle
        #x and y are taken from the down-left corner of the rectangle. 
        cv2.drawContours(frame, [cnt], -1, (0, 0,255), 3) #draw contours at the frame
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 1) #draw a rectangle arround the contours
        
        #create a 2-axis system with a center in the midle of the previous rectangle
        x1 = cv2.line(frame, (x+int(w/2), 0), (x+int(w/2), rows), (255,0,0), 1) 
        y1 = cv2.line(frame, (0, y+int(h/2)), (cols , y+int(h/2)), (255,3,0), 1)
        print(x+int(w/2), y+int(h/2))
        
        distance = dist_from_center(x+int(w/2), y+int(h/2), eye_center)
        print(distance)
        
        if looking_elsewhere(distance, 20)==True:
            print("looking elsewhere")
        else:
            print("looking str")
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