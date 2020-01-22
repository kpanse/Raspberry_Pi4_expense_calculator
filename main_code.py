# Author: Kshitij Panse
# Agile workflow manager
# This project is for Raspberry Pi4 interface with Logitech Webcam using opencv libraries
# Tickets Calculation Android apk to keep track 
#
# Input : Chart Boards and post-it notes video feed
# Output: Expenditure, Income, Balance, TICKETS_INFO & PROGRESS INFO in excel format
# =======================================================================================================

# ===============================================================================================================================================
# Libraries^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
# ===============================================================================================================================================

import cv2
import numpy as np
import os
import time 

# ===============================================================================================================================================
# Initialization
# ===============================================================================================================================================

global pc_counter
global break_flag_1
global prev_pc
global filename_1
global change_flag
global pic_cnt_a
global pic_cnt_b
global pic_cnt_c
r=[70,40,120,80]
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
ROI_status=0

filename_1='a'
pc_counter=1
prev_pc=0
pc=1

frames=[]
filenames=[]
break_flag_1=False
break_flag_2=False
change_flag=False

frame_cnt=0
filename='a0.jpg'
pic_cnt_a=0
pic_cnt_b=0
pic_cnt_c=0

cv2.namedWindow('test')


# ===============================================================================================================================================
# Functions
# ===============================================================================================================================================


# Function generates file names

def fname_gen(key,frame): 
    
    global pic_cnt_a
    global pic_cnt_b
    global pic_cnt_c
    
    if (key=='a'):

        pic_cnt_a+=1
        filename=[chr(key_pressed)+'_'+str(pic_cnt_a-1)+'.png']
 #       print(filename)
#        save_image(frame,filename)
        return filename
    
    elif (key=='b'):

        pic_cnt_b+=1    
        print(str(pic_cnt_b-1))
        filename=[chr(key_pressed)+'_'+str(pic_cnt_b-1)+'.png']
#            
#        save_image(frame,filename)
        return filename

            
    elif (key=='c'):

        pic_cnt_c+=1    
        filename=[chr(key_pressed)+'_'+str(pic_cnt_c-1)+'.png']
#            print(filename)          # will change to save_image(frame,filename) in all 3
#        save_image(frame,filename)
        return filename
         
    else:
        print("Wrong input")
        

def save_image(frame,filename):
    
    path = os.getcwd()
    path1=path+"/Pics"
    os.chdir(path1)
   
    cv2.imwrite(str(filename),frame)
   
    os.chdir(path)
    
#
def path_image(filename):
    
    path = os.getcwd()
    path1=str(path)+"\Inputs"+str(filename)
    return path1
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



def fname_gen2(key): 
    
    global pic_cnt_a
    global pic_cnt_b
    global pic_cnt_c
    
    if (key=='a'):

        pic_cnt_a+=1
        t='\ '
        filename=[t+chr(key_pressed)+'_'+str(pic_cnt_a-1)+  '.png']
 #       print(filename)
#        save_image(frame,filename)
        return filename
    
    elif (key=='b'):

        pic_cnt_b+=1    
        print(str(pic_cnt_b-1))
        filename=[chr(key_pressed)+'_'+str(pic_cnt_b-1)+'.png']
#            
#        save_image(frame,filename)
        return filename

            
    elif (key=='c'):

        pic_cnt_c+=1    
        filename=[chr(key_pressed)+'_'+str(pic_cnt_c-1)+'.png']
#            print(filename)          # will change to save_image(frame,filename) in all 3
#        save_image(frame,filename)
        return filename
         
    else:
        print("Wrong input")
        


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

# ===============================================================================================================================================
# Main Code
# ===============================================================================================================================================

# Next task: Improve selectROI
# Next task: csv_gen function implementation for creating the .csv file everyday at 23.00
# Implementation of caliberate function after fixing the position of the box. 30 second footage is recorded in three scenarios and the hue values  


# press y three times to start recording pictures
# press q to quit

while(cap.isOpened()):
    
    frame_cnt+=1
    ret, frame = cap.read()
    key_pressed=cv2.waitKey(1) & 0xFF
    
    if key_pressed != 255:
        
#        print(chr(key_pressed)) 
        key=chr(key_pressed)
        filename=fname_gen(key,frame)
        print(filename)
        
        if filename is not None:
            filenames.append(filename)
            frames.append(frame)
#        save_image(frame,filename)
    
        if (key=='q'):
            print('Mission Abort! Run')
            break

#    cv2.imshow('frame',frame)
    cv2.imshow('test',frame)
    prev_pc=pc
   
    if (break_flag_1==True):    
        break

# print(len(filenames))
# print(np.shape(filenames))
# print(len(frames))
# print(np.shape(frames))

print(frames)            # Raspberry will send it to the server for processing. JSON format
print(filenames)         # Raspberry will send it to the server for processing.  Json 
 
# Write a code to read these values in JSON format and do some basic processing like displaying the image 
 

# This is it for server
img_thresh=np.zeros(np.shape(frame))
for i in range(len(filenames)):
    img_thresh=thresholding(frames[i])    
    save_image(img_thresh,filenames[i][0])

# print(frames)
# print(filenames)


