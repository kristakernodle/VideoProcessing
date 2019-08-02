#!/usr/bin/env python3

"""
Created on Thu Sep 27 13:18:39 2018

@author: kkrista
"""

import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import LEDDetection

# Define animal directory
animalDir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/'

# Initialize Variables
allAnimals=[]
allFolders = os.listdir(animalDir)

# Get all animal folders
index=0
for file in allFolders:
    if 'et' in file[:2]:
        allAnimals.append(file)
        index += 1

# Loop through animals
for animal in allAnimals:
    currAnDir=animalDir+animal+'/Training/'
    
    if not os.path.isdir(currAnDir):
        continue
    
    allTrainDays=os.listdir(currAnDir)
    
    # Loop through training days
    for day in allTrainDays:
        
        # Skip .MP4 files in allTrainDays
        if ('.MP4' in day):
            continue
        
        currDayDir=currAnDir+day
        allFiles=os.listdir(currDayDir)

        
        vidFiles=[file for file in allFiles if file.endswith('.MP4')]
        csvFiles=[file for file in allFiles if file.endswith('.csv')]
        existingReachDir=[file for file in allFiles if 'Reaches' in file]
        
        # If LED detection hasn't been performed, perform the LED Detection
        if len(csvFiles) == 0:
            csvFiles = LEDDetection.LEDDetection(currDayDir,vidFiles)
        
        # Cycle through csvFiles and vidFiles
        for vid in vidFiles:
            
            # If vid is an open file (._) or not a video, skip
            if ('._' in vid) or ('.MP4' not in vid):
                continue
            
            
            fname = vid.strip('.MP4')
            
            for csv in csvFiles:
                if (fname in csv) and (len(fname) is len(csv.strip('.csv'))):
                    
                    outDir=currDayDir + '/Reaches' + fname[-2:]
                    # Make output directory
                    if ('Reaches'+ fname[-2:] not in existingReachDir):
                        os.makedirs(outDir)
                    
                    if not (os.listdir(currDayDir + '/' +'Reaches'+ fname[-2:])):
                        # Load csv file
                        with open(currDayDir + '/' + csv) as f:
                            openCSV = f.read().splitlines()
                    
                        vidCnt=0
                        for reachVid in openCSV:
                            startTime=int(reachVid)
                            endTime=startTime+17
                            vidCnt += 1
                            
                            if len(str(vidCnt))<2:
                                vidNum = '0' + str(vidCnt)
                            else:
                                vidNum=str(vidCnt)
                            
                            ffmpeg_extract_subclip(currDayDir + '/' + vid, startTime, endTime, targetname = outDir +'/' + fname + '_R' + vidNum + '.mp4')
                    
                    else:
                        continue
                
