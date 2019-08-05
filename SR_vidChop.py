#!/usr/bin/env python3

"""
Created on Thu Sep 27 13:18:39 2018

@author: kkrista
"""

import os
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
        while len(csvFiles) < len(vidFiles):
            
            for vid in vidFiles:
                                              
                # If vid is an open/invisible file (._) or not a video, skip
                if ('._' in vid) or ('.MP4' not in vid):
                    continue
                
                fname = vid.strip('.MP4')
                
                # If the video has not already been analyzed
                if fname + '.csv' not in csvFiles:
                                    
                    print('Beginning Analysis on: ' + vid) 
                
                    csvFile, vidFrames = LEDDetection.LEDDetection(currDayDir,vid)
                
                    # Save csvFile (filename) into csvFiles (list of all csvFiles)
                    csvFiles.append(csvFile)
                else:
                    with open(currDayDir + '/' + fname + '.csv') as f:
                        vidFrames = f.read().splitlines()
                        
                currVidFile = currDayDir + '/' + vid
                
                outDir=currDayDir + '/Reaches' + fname[-2:]
                
                # If the reach directory does not already exist
                if ('Reaches'+ fname[-2:] not in existingReachDir):
                    os.makedirs(outDir)
                        
                    vidCnt=1
                    
                    for reachVid in vidFrames:
                        
                        if len(str(vidCnt))<2:
                            vidNum = '0' + str(vidCnt)
                        else:
                            vidNum=str(vidCnt)
                        
                        command = "ffmpeg -y -i " + currVidFile + " -vf select=" + '"' + "gte(n" + "\\" + "," + reachVid + "),setpts=PTS-STARTPTS" + '"' + " -r 60 -c:v libx264 -frames:v 960 -t 16 " + outDir + "/" + fname + "_R" + vidNum + ".mp4"
                        #ffmpeg_extract_subclip(currDayDir + '/' + vid, startTime, endTime, targetname = outDir +'/' + fname + '_R' + vidNum + '.mp4')
                        os.system(command)
                        vidCnt += 1
                else:
                    continue
                
