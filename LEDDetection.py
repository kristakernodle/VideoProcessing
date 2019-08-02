#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 15:39:38 2019

@author: kkrista
"""

import cv2
import numpy as np

def LEDDetection(currDayDir,vidFiles):
    
    csvFiles=[]
    
    for vid in vidFiles:

        print(currDayDir+'/'+vid)    
        cap = cv2.VideoCapture(currDayDir+'/'+vid)
        frameCnt=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps=int(cap.get(cv2.CAP_PROP_FPS))
    
        frameNum=0
        currTime=frameNum/fps
        dur=frameCnt/fps
    
        timestamps=[]
    
        binOn=0
        while(currTime<=dur-10):
            cap.set(1,frameNum)
            ret, frame = cap.read()
            
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([80,143,220])
            upper_blue = np.array([130,255,255])
            mask = cv2.inRange(hsv,lower_blue,upper_blue)
            value=sum(sum(mask))

            if value > 5000 and binOn == 0:
		        # If the LED was previously off but is now on
                
                # Algorithm to test if we have the first frame
                

                timestamps.append(int(currTime))
                frameNum=frameNum+(fps*10)
                binOn=1
                print(currTime)
            else:
                continue
            
            currTime=frameNum/fps
            
        filename=vid.strip('.MP4')
        file=open(currDayDir+'/'+filename+'.csv','w+')
        for ts in range(0,len(timestamps)):
            file.write('%d\n' %timestamps[ts])   
        file.close()
        csvFiles.append(filename+'.csv')
        
    cap.release()
    cv2.destroyAllWindows()
    return csvFiles

