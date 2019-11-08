#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 11:00:36 2019

@author: kkrista
"""

# Import required functions
import os
import LEDDetection

# Define animal directory
#animalDir = input("Type the directory containing all files to be analyzed: ")
#if len(animalDir) < 1:
    
dlVids = []
doBreak = False
animalDir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/'

# Initialize Variables
allAnimals=[]
allFolders = os.listdir(animalDir)



# Get all animal folders
for file in allFolders:
    if 'et' in file[:2]:
        # Collect the files that have 'et', denoting 'Ear Tag' into one list
        allAnimals.append(file)

allAnimals.sort()
# Loop through animals
for animal in allAnimals:
    
    # Define training directory for animal
    currAnDir=animalDir+animal+'/Training/'
        
    if not os.path.isdir(currAnDir):
        # If there is no 'Training' directory, skip this animal
        continue
    
    # Get contents of 'Training' directory
    allTrainDays=os.listdir(currAnDir)
    
    
    allTrainDays.sort()
    # Loop through training days
    for day in allTrainDays:

        if ('.MP4' in day):
            # Skip .MP4 files in 'Training' directory
            continue

        # Define training day directory
        currDayDir=currAnDir+day

        if not os.path.isdir(currDayDir):
            # Skip 'Training/*' items that are not directories
            continue

        # Identify where we're at in the code, in case of issues
        print('Checking: ' + day)

        # Get all contents of the training day directory
        allFiles=os.listdir(currDayDir)

        # Separate out files and directories by type
        vidFiles=[file for file in allFiles if file.endswith('.MP4')]
        allCsvFiles=[file for file in allFiles if file.endswith('.csv')]
        existingReachDir=[file for file in allFiles if 'Reaches' in file]
        
        csvFiles = [item for item in allCsvFiles if 'Scored' not in item]
        
        vidFiles.sort()
        csvFiles.sort()
        existingReachDir.sort()

        if len(csvFiles) == 0 and len(vidFiles) == 0:
            case = 0
        elif len(csvFiles) !=0 and len(vidFiles) == 0 and len(existingReachDir) == 0:
            case = 0
        elif len(csvFiles) == 0 and len(vidFiles) != 0:
            case = 1
        elif len(csvFiles) < len(vidFiles):
            case = 1
        elif len(csvFiles) > len(vidFiles) and len(existingReachDir) < len(csvFiles):
            case = 2
        elif len(csvFiles) == len(vidFiles) and len(existingReachDir) == 0:
            case = 2
        elif (len(csvFiles) == len(vidFiles) or len(csvFiles) == len(existingReachDir)) and len(existingReachDir) != 0:
            case = 2
        elif len(csvFiles) < len(vidFiles) and len(existingReachDir) == 0:
            case = 1
        else:
            print('found an exception that needs to be addressed:\n')
            print(day + '\n')
            print('csvFiles = ' + str(len(csvFiles)) + '\n')
            print('vidFiles = ' + str(len(vidFiles)) + '\n')
            print('existingReachDir = ' + str(len(existingReachDir)) + '\n')
            doBreak = True
            break
        
        if doBreak is True:
            break
        
        dlVids = LEDDetection.switcher(case, day, currDayDir, csvFiles,vidFiles,existingReachDir, dlVids)

    if doBreak is True:
        break
            
        
            

        
        