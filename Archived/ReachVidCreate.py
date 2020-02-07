#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 13:18:39 2018

@author: kkrista
"""
# Get filenames for all .csv files & all .mp4 files
import glob, os, cv2
import numpy as np
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

os.chdir('/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/FindLED')
vids = glob.glob('./*_*_*_*.MP4')

# Begin loop for each video
for item in range(len(vids)):
    
    # Get video information into useable variables
    filename = vids[item].strip('.MP4')
    splitName = filename.split("_")
    eT = splitName[0]
    date = splitName[1]
    CC = splitName[2]
    vidNum = splitName[3]
    
    # Define the output directory
    
    outDir = '/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/Cut/' + eT + '/' + eT + '_' + date + '_' + CC + '/Reaches' + vidNum
    os.makedirs(outDir)
    
    cap = cv2.VideoCapture('/media/kkrista/KRISTAEHD/Python_LEDDetection/'+filename+'.MP4')
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
    file=open('/media/kkrista/KRISTAEHD/Python_LEDDetection/'+filename+'.csv','w+')
    for ts in range(0,len(timestamps)):
        file.write('%d\n' %timestamps[ts])   
    file.close()

    cnt = 1
    # Iterate over number of reaches
    for reach in timestamps:
        if reach[0] != 0:                    
            ffmpeg_extract_subclip('/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/FindLED/' + eT + '_' + date + '_' + CC + '_' + vidNum + '.MP4', reach[1]+1, reach[1]+17, targetname = outDir + '/' + eT + '_' + date + '_' + vidNum + '_R' + str(cnt) + '.MP4')
            cnt = cnt + 1
            
    # Move completed files (csv & MP4) to the "Cut" directory
    os.rename('/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/FindLED/' + eT + '_' + date + '_' + CC + '_' + vidNum + '.MP4','/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/Cut/' + eT + '/' + eT + '_' + date + '_' + CC + '/' + eT + '_' + date + '_' + CC + '_' + vidNum + '.MP4')
    os.rename('/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/FindLED/' + eT + '_' + date + '_' + CC + '_' + vidNum + '.csv','/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/Cut/' + eT + '/' + eT + '_' + date + '_' + CC + '/' + eT + '_' + date + '_' + CC + '_' + vidNum + '.csv')
