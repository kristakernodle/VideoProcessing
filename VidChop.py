#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 13:18:39 2018

@author: kkrista
"""

# Get filenames for all .csv files & all .mp4 files
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# Define animal directory
animalDir = '/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/Animals/'

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
        
        if ('.MP4' in day):
            continue
        
        currDayDir=currAnDir+day
        allFiles=os.listdir(currDayDir)

        
        vidFiles=[file for file in allFiles if file.endswith('.MP4')]
        csvFiles=[file for file in allFiles if file.endswith('.csv')]
        existingReachDir=[file for file in allFiles if 'Reaches' in file]
        
        # If videos have already been processed OR if LED detection hasn't been performed, skip this training day
        if len(existingReachDir) is len(vidFiles):
            continue
        elif len(csvFiles) == 0:
            continue
        
        # Cycle through csvFiles and vidFiles
        for vid in vidFiles:
            
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
                        
                        for reachVid in openCSV:
                            reachVid=reachVid.split(',')
                            if int(reachVid[0]) != 0:
                                startTime=float(reachVid[1])
                                if len(reachVid) == 2:
                                    endTime=startTime+17
                                else:
                                    endTime=float(reachVid[2])
                                
                                if len(reachVid[0]) == 1:
                                    vidNum = '0' + reachVid[0]
                                else:
                                    vidNum = reachVid[0]
                                
                                ffmpeg_extract_subclip(currDayDir + '/' + vid, startTime, endTime, targetname = outDir +'/' + fname + '_R' + vidNum + '.mp4')
                    
                    else:
                        continue
                