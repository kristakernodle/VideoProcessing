#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 13:18:39 2018

@author: kkrista
"""
# Get filenames for all .csv files & all .mp4 files
import glob, os
import numpy as np
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

os.chdir('/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/ToBeCut')
csvs = glob.glob('./*_*_*_*.csv')
vids = glob.glob('./*_*_*_*.MP4')


# Begin loop for each video
for item in range(len(csvs)):
    
    # Get video information into useable variables
    filename = csvs[item].strip(('./' '.csv'))
    splitName = filename.split("_")
    eT = splitName[0]
    date = splitName[1]
    CC = splitName[2]
    vidNum = splitName[3]
    
    # Define the output directory
    
    outDir = '/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/Cut/' + eT + '/' + eT + '_' + date + '_' + CC + '/Reaches' + vidNum
    os.makedirs(outDir)
    
    # Import .csv files
    allReaches = np.genfromtxt(csvs[item], delimiter=',')
    
    cnt = 1
    
    # Iterate over number of reaches
    for reach in allReaches:
        if reach[0] != 0:                    
            ffmpeg_extract_subclip('/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/ToBeCut/' + eT + '_' + date + '_' + CC + '_' + vidNum + '.MP4', reach[1]+1, reach[1]+17, targetname = outDir + '/' + eT + '_' + date + '_' + vidNum + '_R' + str(cnt) + '.MP4')
            cnt = cnt + 1
            
    # Move completed files (csv & MP4) to the "Cut" directory
    os.rename('/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/ToBeCut/' + eT + '_' + date + '_' + CC + '_' + vidNum + '.MP4','/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/Cut/' + eT + '/' + eT + '_' + date + '_' + CC + '/' + eT + '_' + date + '_' + CC + '_' + vidNum + '.MP4')
    os.rename('/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/ToBeCut/' + eT + '_' + date + '_' + CC + '_' + vidNum + '.csv','/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/Cut/' + eT + '/' + eT + '_' + date + '_' + CC + '/' + eT + '_' + date + '_' + CC + '_' + vidNum + '.csv')
