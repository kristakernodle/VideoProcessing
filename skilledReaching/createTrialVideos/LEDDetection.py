#!/usr/bin/env python3

"""
LEDDetection.py

This file contains a set of functions used for detecting the first frame a blue LED is on 
from a video file. It is a dependency of the SR_vidChop.py script. 

Dependencies:
    cv2 4.0.0
    numpy 1.15.4

"""

__author__ = 'Krista Kernodle'
__copyright__ = 'Copyright 2018, The Leventhal Lab'
__license__ = 'GPL'
__version__ = '0.0.1'
__maintainer__ = 'Krista Kernodle'
__email__ = 'kkrista@umich.edu'
__status__ = 'Development'

import cv2
import numpy as np

def LED(cap,frameNum):
    # This function checks whether a blue LED is on
    # lower_blue and upper_blue provide the hsv upper and lower limits for detection
    
    cap.set(1,frameNum)
    ret, frame = cap.read()
    
    if ret is True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([80,143,220])
        upper_blue = np.array([130,255,255])
        mask = cv2.inRange(hsv,lower_blue,upper_blue)
        value = sum(sum(mask))
    else:
        value = 0
        
    return value

def isFirstFrame(frameNum,cap,secs,firstFrame):
    # This function identifies the first frame in the video where an LED is on
    # Note: Assumtion is made that the frame rate is >= 59 fps
    
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
    # This function reads in the video and performs the LED detection for a blinking LED. 
    #
    # INPUT
    #   currDayDir  : Directory containing video of interest
    #   vid         : Video file of blinking blue LED
    #
    # OUTPUT
    #   filename    : Name of the csv file that was generated containing vidFrames
    #   vidFrames   : List containing all frame numbers that have been identified as the 
    #                 start of the LED on period
    
    cap = cv2.VideoCapture(currDayDir+'/'+vid)
    frameCnt=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frameNum=0
    
    vidFrames=[]
    
    while(frameNum < frameCnt):
            
        value = LED(cap,frameNum)

        if value > 5000:
            # If the LED is on:
            # Algorithm to test if we have the first frame
            
            if frameNum <= 1:
                firstFrame = True
            else:
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
    
    return filename, vidFrames, frameCnt

