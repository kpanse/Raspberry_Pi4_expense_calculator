# Author: Kshitij Panse
# Agile workflow manager
# This project is for Raspberry Pi4 interface with Logitech Webcam using opencv libraries
# Tickets Calculation Android apk to keep track 
#
# Input : Chart Boards and post-it notes video feed
# Output: Expenditure, Income, Balance, TICKETS_INFO & PROGRESS INFO in excel format
#

#
# =============================================================================
# ##Libraries
# =============================================================================
#

import cv2
import numpy as np

#
# =============================================================================
# Initialization
# =============================================================================
#

r=np.zeros([1,4])
cap = cv2.VideoCapture(1)
ROI_status=0

#
# =============================================================================
# Functions
# =============================================================================
#

#
# This function takes binary image and returs output after morphological reforms
#
def thresholding(img):

    ret,thresh1 = cv2.threshold(img,157,255,cv2.THRESH_BINARY)
    kernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(thresh1,kernel,iterations = 1)
    erosion = cv2.erode(dilation,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations = 1)
 #   opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)

    return dilation

#
# This function Detects the ROI and draws Rectangle
# More research needed in this function 
#
def find_ROI(areas,contours,frame):
    if (np.sum(np.shape(areas))>0):                       # Condition for checking if countours present without messing the rest of the code

        if(max(areas)>4000):
                
            ROI_status=1                                  #  ROI detected  
            max_ind = np.argmax(areas)
            cnt=contours[max_ind]
   
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
       
#
# This function calculates the Region of Interest (ROI) and displays live video with boundaries of ROI    
#    r=cv2.selectROI(frame)  -  For manual ROI selection    
#
def select_ROI(cap):

    temp=1
    a=[]
    ROI_status=0
    
    while(cap.isOpened()):

        ret, frame = cap.read()
        
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frame_HSV,np.array([0,50,0]),np.array([10,150,255]) )     # Hard-coded values. Caliberation required!!
        gray = thresholding(mask)    

        contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        areas = [cv2.contourArea(c) for c in contours]
        find_ROI(areas,contours,frame)
   
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    imCrop = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    return imCrop


# =============================================================================
# Main Code
# =============================================================================
img=select_ROI(cap)