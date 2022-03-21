import cv2
import numpy as np

path="D:\Downloads\IMG_0216.MOV"
cap = cv2.VideoCapture(path)
eye_cascade = cv2.CascadeClassifier("D:\Downloads\haarcascade_eye.xml")

while True:
    ret, frame = cap.read()
    
    if ret is False:
        break
    
    gray= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 5)
    rows, cols,_= frame.shape 
    _, threshold = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
    contours ,_ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours= sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)    
    
    
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 3)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(frame, (ex, ey),(ex+ew, ey+eh), (0,150,255))
        while(eyes.all()==True):
            for cnt in contours:
                (x, y ,w, h) = cv2.boundingRect(cnt)
                if((ex<=x) and (ey<=y) and (ex+ew<=x+w) and (ey+eh<=y+h)):
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 1)
                    cv2.line(frame, (x+int(w/2), 0), (x+int(w/2), rows), (255,0,0), 1)
                    cv2.line(frame, (0, y+int(h/2)), (cols , y+int(h/2)), (255,0,0), 1)
            break
    
    
    cv2.imshow("threshold", threshold)
    cv2.imshow("gray", gray)
    cv2.imshow("frame", frame)
    
    key = cv2.waitKey(30)
    if key == 27 :
        break
    
cap.release()
cv2.destroyAllWindows()