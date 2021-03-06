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
import pygame
import subprocess as sp


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
global pic_cnt_d

r=[70,40,120,80]

filename_1='a'
key='a'

pc_counter=1
prev_pc=0
pc=1

frames=[]
filenames=[]
filename='a0.jpg'

frame_cnt=0
pic_cnt_a=0
pic_cnt_b=0
pic_cnt_c=0
pic_cnt_d=0

cv2.namedWindow('test')
cv2.namedWindow('frame')
cv2.resizeWindow('test', 640,480)
cv2.resizeWindow('frame', 640,480)


# ===============================================================================================================================================
# Functions
# ===============================================================================================================================================


# Function generates file names

def fname_gen(key,frame): 
    
    global pic_cnt_a
    global pic_cnt_b
    global pic_cnt_c
    global pic_cnt_d
    if (key=='a'):

        pic_cnt_a+=1
        filename=[key+'_'+str(pic_cnt_a-1)+'.png']
 #       print(filename)
#        save_image(frame,filename)
        return filename
    
    elif (key=='b'):

        pic_cnt_b+=1    
        print(str(pic_cnt_b-1))
        filename=[key+'_'+str(pic_cnt_b-1)+'.png']
#            
#        save_image(frame,filename)
        return filename

            
    elif (key=='c'):

        pic_cnt_c+=1    
        filename=[key+'_'+str(pic_cnt_c-1)+'.png']
#            print(filename)          # will change to save_image(frame,filename) in all 3
#        save_image(frame,filename)
        return filename

    elif (key=='d'):

        pic_cnt_d+=1    
        filename=[key+'_'+str(pic_cnt_d-1)+'.png']
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

    lower_red1 = np.array([0,200,100], dtype = "uint8")
    upper_red1 = np.array([5,255,255], dtype = "uint8")
    lower_red2 = np.array([170,200,100], dtype = "uint8")
    upper_red2 = np.array([179,255,255], dtype = "uint8")    
    
    ret,thresh1 = cv2.threshold(img,157,255,cv2.THRESH_BINARY)
    kernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(thresh1,kernel,iterations = 1)
    erosion = cv2.erode(dilation,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations = 1)
    
    mask_red1 = cv2.inRange(dilation, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(dilation, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    thresh_img = cv2.bitwise_and(img, img, mask = mask_red) 

#   opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)

    return thresh_img, dilation

#
# This function Detects the ROI and draws Rectangle
# More research needed in this function 
#

    
#

# ===============================================================================================================================================
# Main Code
# ===============================================================================================================================================

# Next task: Improve selectROI
# Next task: csv_gen function implementation for creating the .csv file everyday at 23.00
# Implementation of caliberate function after fixing the position of the box. 30 second footage is recorded in three scenarios and the hue values  


# press y three times to start recording pictures
# press q to quit


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
ROI_status=0

stdoutdata = sp.getoutput("hcitool con")
if "1C:A0:B8:5C:BF:96" in stdoutdata.split():
    print("Bluetooth device is connected")
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()


while(cap.isOpened()):
        
     frame_cnt+=1
     ret, frame = cap.read()
     frame1=frame
        
     if "1C:A0:B8:5C:BF:96" in stdoutdata.split():
         print("Bluetooth device is connected")
        
         events = pygame.event.get()
            
         for event in events:
        
            if event.type == pygame.JOYBUTTONDOWN:
 #               print("Button Pressed")
                
                if j.get_button(3):
                    print("Square Pressed")
                    key='d'
                elif j.get_button(0):
                    print("X Pressed")
                    key='a'    
                elif j.get_button(1):
                    print("Circle Pressed")
                    key='b'
                elif j.get_button(2):
                    print("Triangle Pressed")
                    key='c'
                elif j.get_button(4):
                    print("L1 Pressed")
                elif j.get_button(5):
                    print("R1 Pressed")
                elif j.get_button(6):
                     print("L2 Pressed")
                elif j.get_button(7):
                     print("R2 Pressed")
                elif j.get_button(8):
                     print("Share Pressed")
                elif j.get_button(9):
                    print("Options Pressed")
                elif j.get_button(11):
                    print("Left Analog Pressed")
                elif j.get_button(12):
                    print("Right Analog Pressed")
                elif j.get_button(10):
                    print("PS Button Pressed")
                    #key='q'
                elif j.get_button(13):
                    print("Touchpad Pressed")                    
     

                filename=fname_gen(key,frame)
                print(filename)
        
                if filename is not None:
                    filenames.append(filename)
                    frames.append(frame1)         #        Later for save_image(frame,filename)
        
     else:
        print("Controller Disconnected")
            # Try to connect the controller here
        
     img_thresh1, img_thresh2 = thresholding(frame)
     cv2.imshow('frame',img_thresh1)
     cv2.imshow('test',img_thresh2)

     key_pressed=cv2.waitKey(1) & 0xFF
    
     if key_pressed != 255:
        if (chr(key_pressed)=='q'):
            print('Mission Abort! Run')
            break


     prev_pc=pc
   

#    print(frames)            # Raspberry will send it to the server for processing. JSON format
print(filenames)         # Raspberry will send it to the server for processing.  Json 


for i in range(len(filenames)):
    img_thresh=thresholding(frames[i])
    save_image(img_thresh,filenames[i][0])
