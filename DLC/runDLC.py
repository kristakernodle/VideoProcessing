#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run files through DLC

Created on Mon Jul 15 11:17:56 2019

@author: kkrista
"""

# Import necessary packages
import os
import deeplabcut

# Import custom functions and variables
import animalInfo
import setDLCFunc

# User Define Variables
DLCDir = '/home/kkrista/Documents/SkilledReaching/'
cropParamsDir = '/home/kkrista/Documents/SkilledReaching/cropParams/'

# Find the files we want to run
# For debugging and initial code writing purposes, I've created a specific file to work out of

#### Docker Directory
dirToAnalyze = '/opt/usb/DLCSR/20190712/'

#### Linux Directory
#dirToAnalyze = '/media/kkrista/KRISTAEHD/DLCSR/20190712/'

##

# First, obtain subject directories that need to be analyzed
subjDirs = os.listdir(dirToAnalyze)
subjs = [item.strip('et') for item in subjDirs]

# Loop through subjects
for subj in subjs:
    
    [pawPref, nonPrefPaw] = animalInfo.pawPref(subj)
    boxNum = animalInfo.boxID(subj)
    
    # Read the csv files needed for cropping
    directView_allCrops = setDLCFunc.readfile(cropParamsDir + 'CC' + boxNum + '_directCrops.csv')
    mirrorView_allCrops = setDLCFunc.readfile(cropParamsDir + 'CC' + boxNum + '_' + nonPrefPaw + 'Crops.csv')
    
    # Find the configuration files
    allDLCNets = os.listdir(DLCDir + pawPref + 'PP/')
    directNet = [item for item in allDLCNets if 'Center' in item]
    mirrorNet = [item for item in allDLCNets if nonPrefPaw[1:] in item.strip(pawPref + 'PP')]
    directConfig = DLCDir + pawPref + 'PP/' + directNet[0] + '/config.yaml'
    mirrorConfig = DLCDir + pawPref + 'PP/' + mirrorNet[0] + '/config.yaml'
    
    # Get all training days
    trainDayDirList = os.listdir(dirToAnalyze + 'et' + subj + '/Training/')
    trainDayDirList = [dirToAnalyze + 'et' + subj + '/Training/' + item for item in trainDayDirList if os.path.isdir(dirToAnalyze + 'et' + subj + '/Training/'+ item)]
    
    for day in trainDayDirList:
        
        vidID = day.split('/')[-1]
        date = vidID.split('_')[1]
        CCNum = vidID.split('_')[2]
        
        # Verify that the cropping parameters we will be using are correct
        if 'CC' + boxNum != CCNum:
            print('CC Number for this video does not match that of animal')
            print('')
            print(day)
            continue
        
        
        # Find appropriate cropping parameters
        directViewCrops = [item for item in directView_allCrops if date in item]
        mirrorViewCrops = [item for item in mirrorView_allCrops if date in item]
        
        if len(directViewCrops) == 0 or len(mirrorViewCrops) == 0:
            print('Cropping parameters needed for this date')
            print('')
            print(day)
            continue
        
        directViewCrops = directViewCrops[0].split(',')
        mirrorViewCrops = mirrorViewCrops[0].split(',')
        
        # Edit the configuration files with the appropriate cropping parameters
        directConfig_edit = deeplabcut.auxiliaryfunctions.read_config(directConfig)
        if directConfig_edit['cropping'] is False:
            directConfig_edit['cropping'] = True
        directConfig_edit['x1'] = int(directViewCrops[1])
        directConfig_edit['x2'] = int(directViewCrops[2])
        directConfig_edit['y1'] = int(directViewCrops[3])
        directConfig_edit['y2'] = int(directViewCrops[4])
        
        deeplabcut.auxiliaryfunctions.write_config(directConfig,directConfig_edit)
        
        mirrorConfig_edit = deeplabcut.auxiliaryfunctions.read_config(mirrorConfig)
        if mirrorConfig_edit['cropping'] is False:
            mirrorConfig_edit['cropping'] = True
        mirrorConfig_edit['x1'] = int(mirrorViewCrops[1])
        mirrorConfig_edit['x2'] = int(mirrorViewCrops[2])
        mirrorConfig_edit['y1'] = int(mirrorViewCrops[3])
        mirrorConfig_edit['y2'] = int(mirrorViewCrops[4])
        
        deeplabcut.auxiliaryfunctions.write_config(mirrorConfig,mirrorConfig_edit)
        
        reachesDirList = os.listdir(day)
        reachesDirList = [day +'/'+ item for item in reachesDirList if os.path.isdir(day +'/'+ item)]

        for reachFolder in reachesDirList:
            allReaches = os.listdir(reachFolder)
            allReaches = [reachFolder +'/'+ reach for reach in allReaches if '._' not in reach]
            
            deeplabcut.analyze_videos(directConfig,allReaches,save_as_csv=True)
            deeplabcut.analyze_videos(mirrorConfig,allReaches,save_as_csv=True)
            
            

            
