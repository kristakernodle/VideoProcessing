#!/usr/bin/env python3

'''
grooming_vidChop.py

Cuts videos based on start and stop times identified in csv files. 

CSV files must have the following structure:
    | start mins | start secs | end mins | end secs |

Created on Thu Apr 25 2019
Author: Krista Kernodle
'''

# USER DEFINED VARIABLES
animalDir = '/Volumes/HD_Krista/Experiments/groomingExp/'


# Required Packages & Functions:
import sys
import os
import setDLCFunc
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# Initialize variables
animalFolders=[]

# Navigate to animal directory 
os.chdir(animalDir)

# Get all animal folders (identified with "et" at the beginning)
allItems=os.listdir()
for item in allItems:
    if item[:2] == 'et':
        animalFolders.append(item)

# Start processing one animal folder at a time
for animal in animalFolders:

    # Enter this animal's folder
    os.chdir(animalDir + animal)

    # Get all files in this directory
    allFiles=os.listdir()

    # Sort files into csv files and mp4 files
    allVids = [file for file in allFiles if file.endswith('.MP4') and '._' not in file]
    csvFiles = [file for file in allFiles if file.endswith('.csv') and '._' not in file]

    # Get any chopped video folders that already exist 
    existingDir = [file for file in allFiles if 'cut' in file]

    # Start analyzing by video
    for vid in allVids:

        filename = vid.split('.')
        filename = filename[0]

        # If the video has a csv file associated with it and was not previously cut
        if (filename + '.csv' in csvFiles) and (filename + '_cut' not in existingDir):
            
            print(filename,end='\n')
            
            # Read in the csv file
            csv = setDLCFunc.readfile(filename+'.csv')

            vidNum=0

            for times in csv:

                vidNum += 1

                if vidNum < 10:
                    indexVar = '0'+str(vidNum)
                else:
                    indexVar = str(vidNum)
                
                # Get start and end times
                times = times.split(',')

                if '\ufeff8' in times[0]:
                    continue
                
                startTime = int(times[0]) * 60 + int(times[1])
                endTime = int(times[2]) * 60 + int(times[3])

                # Define inputs for ffmpeg_extract_subclip
                fullVidDir=animalDir + animal + '/' + vid
                outDir = animalDir + animal + '/' + filename + '_cut/'
                outFile = outDir + filename + '_V' + indexVar + '.mp4'

                # Make the output directory
                if not os.path.isdir(outDir):
                    os.makedirs(outDir)

                # Cut Video
                ffmpeg_extract_subclip(fullVidDir, startTime, endTime, targetname = outFile)
        
        # If the video doesn't have a csv file OR if the cut directory already exists    
        else:
            continue

