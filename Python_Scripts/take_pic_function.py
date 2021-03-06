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
# def store_pic(pc_counter,frame,key_press):
    
    # global change_flag
    # global break_flag_2  
    
    # if frame is not None:
        
       # os.chdir(r"C:\Users\kpans_000\Desktop\Agile\Codes\Pics")
        
        # if (change_flag==True):
            
            # filename_1=key_press
            # print(change_flag)

            # change_flag = False
            
        # filename_1=key_press    
        # img_name=[str(key_press)+str(pc_counter-1)+'.jpg']
        # print('Output Filename: '+str(img_name))
        # print(np.shape(frame))
        # cv2.imwrite(img_name,frame,[cv2.IMWRITE_JPEG_QUALITY, 90])
        # cv2.imwrite(str(filename_1), a, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        # cv2.SaveImage(img_name,frame)
       # os.chdir(r"C:\Users\kpans_000\Desktop\Agile\Codes")
        
        # return [1,img_name]
        
    # else:
        # break_flag_2=True
        # return [-1,0]
      
# def take_pic(frame,key_press):

    # global pc_counter
    # global break_flag_1 
    # global prev_pc
    # global change_flag
   # while(cap.isOpened()):
       # cv2.imshow('img1',frame) #display the captured image
       # ret, frame = cap.read()
    
    # if (key_press == ord('q')):
        # break_flag_1=True
        # print('Exit due to q pressed')

       # print('Pics/a.png'+str(pic_counter),frame)
       # cv2.imwrite('Pics/a.png'+str(pic_counter),frame)
    
    # elif (key_press == ord('x')):
 
        # change_flag=True
        # pc_counter=1
       # print('Now it will be b')
   
    
    # elif (key_press == ord('y')): #save on pressing 'y' 

        # if ((pc_counter!=-1) & (prev_pc!=pc_counter)):
            # temp,img_name=store_pic(pc_counter,frame)
           # if temp[0]==1:
               # cv2.imwrite(img_name,frame,[cv2.IMWRITE_JPEG_QUALITY, 90])
                
            # pc_counter+=1
        
        
        # if break_flag_2 == True:
            # print('Couldnt Store the image properly') 
            
        # prev_pc=pc_counter   
        # return pc_counter    
    
    # else:
        # return -1

        
# This function takes binary image and returs output after morphological reforms
def thresholding(img):
    ret,thresh1 = cv2.threshold(img,157,255,cv2.THRESH_BINARY)
    kernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(thresh1,kernel,iterations = 1)
    erosion = cv2.erode(dilation,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations = 1)
 #   opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)

    return dilation
# ===============================================================================================================================================
# This function is responsible to detect Red borders perfectly in all lighting conditions
def red_caliberate(frame):
    
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_HSV,np.array([0,50,0]),np.array([10,150,255]) )     # Hard-coded values. Caliberation required!!
    gray = thresholding(mask)    
    return gray
# ===============================================================================================================================================
# This function is responsible to detect Red borders perfectly in all lighting conditions
#def csv_gen([sc,al,ms,exp]):
    
  
#    return 0    
# ===============================================================================================================================================
# This function Detects the ROI and draws Rectangle
# More research needed in this function 
def find_ROI(areas,contours,frame):
    if (np.sum(np.shape(areas))>0):                       # Condition for checking if countours present without messing the rest of the code

        if(max(areas)>4000):
                
            ROI_status=1                                  #  ROI detected  
            max_ind = np.argmax(areas)
            cnt=contours[max_ind]
   
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            return [x,y,w,h]
# ===============================================================================================================================================
# This function calculates the Region of Interest (ROI) and displays live video with boundaries of ROI    
#    r=cv2.selectROI(frame)  -  For manual ROI selection    
def select_ROI(frame):

    temp=1
    a=[]
    ROI_status=0
    
#    while(cap.isOpened()):

#        ret, frame = cap.read()        
    gray=red_caliberate(frame)                          #  Detects red color for all lighting conditions 
        
    contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]
    r=find_ROI(areas,contours,frame)
   
    cap.release()
    cv2.destroyAllWindows()

    imCrop = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    return imCrop
# ===============================================================================================================================================


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
    #if(take_pic(frame)=='None'):
     #   break
    #img=select_ROI(cap)
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
    # if key_pressed is not None:
        
        # filename=[str(key_pressed)+str(pic_cnt-1)+'.jpg']
        # print(frame_cnt)
        # print(key_pressed)
        # print(filename)
        

#        save_image(frame,filename)
#    pc=take_pic(frame,key_pressed)
#    if ((pc!=-1) & (prev_pc!=pc)):
#        store_pic(pc,frame)
#cv2.imshow('frame',frame)
#    print(np.shape(frame))
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
for i in range(len(filenames)):
    
    save_image(frames[i],filenames[i][0])
    # cv2.namedWindow('frame'+str(i))
    # cv2.imshow('frame'+str(i),frame)
    # print(filenames[i])
    # time.sleep(5)
    # i+=1
    
# print(frames)
# print(filenames)

