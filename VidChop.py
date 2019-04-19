#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 13:18:39 2018

@author: kkrista
"""
# Get filenames for all .csv files & all .mp4 files
import glob, os
import numpy as np
#from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

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
        elif len(csvFiles) is 0:
            continue
        
        # Cycle through csvFiles and vidFiles
        for vid in vidFiles:
            
            if ('._' in vid) or ('.MP4' not in vid):
                continue
            
            fname = vid.strip('.MP4')
            
            for csv in csvFiles:
                if (fname in csv) and (len(fname) is len(csv.strip('.csv'))) and ('Reaches'+ fname[-2:] not in existingReachDir):
                    # Load csv file
                    
                    
                    # Make output directory
                    outDir=currDayDir + '/Reaches' + fname[-2]
                    os.makedirs(outDir)
                    
                    # Load csv file
                    
                else:
                    continue
                
        
        
        
#
                    
                
## Begin loop for each video
#for item in range(len(csvs)):
#    
#    # Get video information into useable variables
#    filename = csvs[item].strip(('./' '.csv'))
#    splitName = filename.split("_")
#    eT = splitName[0]
#    date = splitName[1]
#    CC = splitName[2]
#    vidNum = splitName[3]
#    
#    # Define the output directory
#    
#    outDir = '/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/Cut/' + eT + '/' + eT + '_' + date + '_' + CC + '/Reaches' + vidNum
#    os.makedirs(outDir)
#    
#    # Import .csv files
#    allReaches = np.genfromtxt(csvs[item], delimiter=',')
#    
#    cnt = 1
#    
#    # Iterate over number of reaches
#    for reach in allReaches:
#        if reach[0] != 0:                    
#            ffmpeg_extract_subclip('/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/ToBeCut/' + eT + '_' + date + '_' + CC + '_' + vidNum + '.MP4', reach[1]+1, reach[1]+17, targetname = outDir + '/' + eT + '_' + date + '_' + vidNum + '_R' + str(cnt) + '.MP4')
#            cnt = cnt + 1
#            
#    # Move completed files (csv & MP4) to the "Cut" directory
#    os.rename('/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/ToBeCut/' + eT + '_' + date + '_' + CC + '_' + vidNum + '.MP4','/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/Cut/' + eT + '/' + eT + '_' + date + '_' + CC + '/' + eT + '_' + date + '_' + CC + '_' + vidNum + '.MP4')
#    os.rename('/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/ToBeCut/' + eT + '_' + date + '_' + CC + '_' + vidNum + '.csv','/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/Cut/' + eT + '/' + eT + '_' + date + '_' + CC + '/' + eT + '_' + date + '_' + CC + '_' + vidNum + '.csv')
