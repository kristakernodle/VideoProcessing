#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 15:39:38 2019

@author: kkrista
"""

import cv2
import numpy as np

def LED(cap,frameNum):
    
    cap.set(1,frameNum)
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([80,143,220])
    upper_blue = np.array([130,255,255])
    mask = cv2.inRange(hsv,lower_blue,upper_blue)
    value = sum(sum(mask))
    
    return value

def isFirstFrame(frameNum,cap,secs,firstFrame):
    
    testFrame = np.floor(frameNum - (60*secs))
    value = LED(cap,testFrame)
    
    if value > 5000 and secs == 5:
        secs = 5
        frameNum = testFrame
    elif value > 5000 and secs < 5:
        frameNum = testFrame
    elif value <= 5000 and secs > 0.059:
        secs = 0.5*secs
    elif value <= 5000 and secs <= 0.059:
        firstFrame = True
    else:
        print('something odd is happening')
        print('value %d', value)
        print('sec %d', secs)
        print('frameNum %d',frameNum)
        print('testFrame %d',testFrame)
        
    return [firstFrame,frameNum,secs]
    
def LEDDetection(currDayDir,vid):
           
    cap = cv2.VideoCapture(currDayDir+'/'+vid)
    frameCnt=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frameNum=0
    
    vidFrames=[]
    
    while(frameNum < frameCnt):
            
        value = LED(cap,frameNum)

        if value > 5000:
            # If the LED is on:
            # Algorithm to test if we have the first frame
                
            firstFrame = False 
            secs = 5
                
            while firstFrame is False:
                [firstFrame,frameNum,secs] = isFirstFrame(frameNum,cap,secs,firstFrame)

            vidFrames.append(frameNum)
                
            frameNum=frameNum+1400
                
        else:
            frameNum = frameNum+300
            continue

    filename = vid.strip('.MP4') + '.csv'
        
    file=open(currDayDir+'/'+filename,'w+')
    for vf in range(0,len(vidFrames)):
        file.write('%d\n' %vidFrames[vf])   
    file.close()
        
    cap.release()
    cv2.destroyAllWindows()
    
    return filename, vidFrames

