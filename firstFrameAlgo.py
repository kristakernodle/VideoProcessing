#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 14:10:04 2019

@author: kkrista
"""

# Input: cap,fps, frameNum, timestamps?

def firstFrameAlgo(cap,fps,frameNum,timestamps):
    
    testFrameNum = frameNum-(fps*5)
    cap.set(1,testFrameNum)
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([80,143,220])
    upper_blue = np.array([130,255,255])
    mask = cv2.inRange(hsv,lower_blue,upper_blue)
    value=sum(sum(mask))
    
    if value 