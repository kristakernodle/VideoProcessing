#!/usr/bin/env python3

"""
SR_vidChop.py

The purpose of this script is to walk through a specified folder structure, 
identify .MP4 files, and perform a blue LED detection on them.

The required folder structure is:
    
    animalDir/et####/Training/day/*_0#.MP4
    
    animalDir       : a variable, defined immediately after import functions and prompted 
                      when this file is run on the command line
    et              : a required string to indicate folders with data you wish to analyzed
    Training        : required folder containing all days that will be analyzed
    day             : a variable, defined based on contents of 'Training' folder
    *.MP4           : the file that will be analyzed

INPUT
    Directory containing all files to be analyzed with the required folder structure (see above)

OUTPUT
    16 second videos cut at the first frame identified with a blue LED on.
    All output videos are .mp4's in subdirectories: animalDir/et####/Training/day/Reaches0#/

Dependencies:
    LEDDetection    : custom functions included with this file)
    ffmpeg 4.0.2

"""

__author__ = 'Krista Kernodle'
__copyright__ = 'Copyright 2018, The Leventhal Lab'
__license__ = 'GPL'
__version__ = '1.0.1'
__maintainer__ = 'Krista Kernodle'
__email__ = 'kkrista@umich.edu'
__status__ = 'Production'

# Import required functions
import os
import LEDDetection

# Define animal directory
animalDir = input("Type the directory containing all files to be analyzed: ")
if len(animalDir) < 1:
    animalDir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/'

# Initialize Variables
allAnimals=[]
allFolders = os.listdir(animalDir)

# Get all animal folders
for file in allFolders:
    if 'et' in file[:2]:
        # Collect the files that have 'et', denoting 'Ear Tag' into one list
        allAnimals.append(file)

# Loop through animals
for animal in allAnimals:

    # Define training directory for animal
    currAnDir=animalDir+animal+'/Training/'
        
    if not os.path.isdir(currAnDir):
        # If there is no 'Training' directory, skip this animal
        continue
    
    # Get contents of 'Training' directory
    allTrainDays=os.listdir(currAnDir)
    
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
        csvFiles=[file for file in allFiles if file.endswith('.csv')]
        existingReachDir=[file for file in allFiles if 'Reaches' in file]
        


        while len(csvFiles) <= len(vidFiles) and len(existingReachDir) < len(vidFiles):
            # When there is not a csv file for each vid file OR reach directory for each video file
            
            for vid in vidFiles:
                                
                if ('._' in vid) or ('.MP4' not in vid):
                    # If vid is an open/invisible file (._) or not a video, skip
                    continue
                
                # Save the filename
                fname = vid.strip('.MP4')
                
                if fname + '.csv' not in csvFiles:
                    # If the video has not already been analyzed             
                    
                    print('Beginning Analysis on: ' + vid) 

                    # Perform LED detection using imported function
                    csvFile, vidFrames, frameCnt = LEDDetection.LEDDetection(currDayDir,vid)
                
                    # Save csvFile (filename) into csvFiles (list of all csvFiles)
                    csvFiles.append(csvFile)

                else:
                    # If the video has already been analyzed, read in the csv file
                    with open(currDayDir + '/' + fname + '.csv') as f:
                        vidFrames = f.read().splitlines()
                    
                # Define full path for current video file
                currVidFile = currDayDir + '/' + vid
                
                # Define full path for output video files ('Reach' directory)
                outDir=currDayDir + '/Reaches' + fname[-2:]
                
                if ('Reaches'+ fname[-2:] not in existingReachDir) or len(os.listdir(outDir)) < len(vidFrames):
                    # If the reach directory does not already exist OR the outDir has fewer videos than vidFrames says there are trials
                    
                    if not os.path.isdir(outDir):
                        # If the reach directory does not already exist
                        os.makedirs(outDir)
                    
                    # Create trial counting variable
                    vidCnt=1

                    # Loop through each trial to cut into short trial videos
                    for reachVid in vidFrames:
                        
                        # This statement creates the string for trial counting (part of output video's filename)
                        if len(str(vidCnt))<2:
                            vidNum = '0' + str(vidCnt)
                        else:
                            vidNum=str(vidCnt)
                        
                        if reachVid + 960 > frameCnt:
                            numFrames = frameCnt - reachVid
                        else:
                            numFrames = 960
                        
                        # Define the command that will be used for cutting the videos
                        command = "ffmpeg -y -i " + currVidFile + " -vf select=" + '"' + "gte(n" + "\\" + "," + str(reachVid) + "),setpts=PTS-STARTPTS" + '"' + " -r 60 -c:v libx264 -frames:v "+str(numFrames)+" -t 16 " + outDir + "/" + fname + "_R" + vidNum + ".mp4"
                        # Run the system command
                        os.system(command)

                        # Increase the trial count 
                        vidCnt += 1
                else:
                    # If the reach directory already exists AND the outDir has the same number of vids as trials in vidFrames, skip
                    continue
