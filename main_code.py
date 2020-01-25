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
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
ROI_status=0

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

filename_1='a'
pc_counter=1
prev_pc=0
pc=1
key='a'

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

    
#

# ===============================================================================================================================================
# Main Code
# ===============================================================================================================================================

# Next task: Improve selectROI
# Next task: csv_gen function implementation for creating the .csv file everyday at 23.00
# Implementation of caliberate function after fixing the position of the box. 30 second footage is recorded in three scenarios and the hue values  


# press y three times to start recording pictures
# press q to quit

frame_cnt=0
try:
    while(cap.isOpened()):
    
        frame_cnt+=1
        ret, frame = cap.read()


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
                    key='q'
                elif j.get_button(13):
                    print("Touchpad Pressed")                    
         

#    key_pressed=cv2.waitKey(100) & 0xFF
    
#    if key_pressed != 255:
        
#        print(chr(key_pressed)) 
#		print(np.shape(frame))
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

        img_thresh=thresholding(frame)
        cv2.imshow('frame',frame)
        cv2.imshow('test',img_thresh)
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

    for i in range(len(filenames)):
        img_thresh=thresholding(frames[i])
        save_image(img_thresh,filenames[i][0])


            
            
#            elif event.type == pygame.JOYBUTTONUP:
#                print("Button Released")
                

# This is it for server
#img_thresh=np.zeros(np.shape(frame))

except KeyboardInterrupt:
    print("EXITING NOW")    
    for i in range(len(filenames)):
        img_thresh=thresholding(frames[i])
        save_image(img_thresh,filenames[i][0])
    j.quit()
# print(frames)
# print(filenames)


