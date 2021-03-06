#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 15:39:38 2019

@author: kkrista
"""

import cv2
import numpy as np

filename='740_20181212_CC2_01'

cap = cv2.VideoCapture('/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/et740/Training/et740_20181212_CC2_T13/'+filename+'.MP4')
frameCnt=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps=int(cap.get(cv2.CAP_PROP_FPS))


frameNum=0
currTime=frameNum/fps
dur=frameCnt/fps

timestamps=[]

binOn=0
while(currTime<=dur):
    cap.set(1,frameNum);
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([80,143,220])
    upper_blue = np.array([130,255,255])
    mask = cv2.inRange(hsv,lower_blue,upper_blue)
    value=sum(sum(mask))
    
    if value > 5000:
        timestamps.append(int(currTime))
        frameNum=frameNum+(fps*20)
        binOn=1
    elif binOn==0:
        frameNum=frameNum+10
    else:
        frameNum=frameNum+fps*8
    currTime=frameNum/fps
    
file=open('/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/et740/Training/et740_20181212_CC2_T13/'+filename+'.txt','w+')
for ts in range(0,len(timestamps)):
    file.write('%d\n' %timestamps[ts])   
file.close()

