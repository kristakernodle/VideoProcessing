#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 14:22:14 2019

@author: Krista
"""

import os
import cropFuncs as cropFunc

allSubjDir = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/'
cropParamsDir = allSubjDir + 'cropParams/'

CC1_directCrops = cropFunc.readfile(cropParamsDir + 'CC1_directCrops.csv')
CC1_leftCrops = cropFunc.readfile(cropParamsDir + 'CC1_leftCrops.csv')
CC1_rightCrops = cropFunc.readfile(cropParamsDir + 'CC1_rightCrops.csv')

CC2_directCrops = cropFunc.readfile(cropParamsDir + 'CC2_directCrops.csv')
CC2_leftCrops = cropFunc.readfile(cropParamsDir + 'CC2_leftCrops.csv')
CC2_rightCrops = cropFunc.readfile(cropParamsDir + 'CC2_rightCrops.csv')

CC1Dates=[]
CC2Dates=[]

for item in CC1_directCrops:
    date = item.split(',')[0]
    CC1Dates.append(date)
    
for item in CC2_directCrops:
    date = item.split(',')[0]
    CC2Dates.append(date)

subjList = os.listdir(allSubjDir)

for subj in subjList:
    # Walk through subject files

    if os.path.isdir(allSubjDir + subj):
        # If you have a subject directory

        subjTrainDir = allSubjDir + subj + '/Training'

        if os.path.isdir(subjTrainDir):
            # If you have a training directory in the subject directory

            trainingDays = os.listdir(subjTrainDir)

            for trainDay in trainingDays:
                # Walk through files and folders in training folder
                print(trainDay)
                if os.path.isdir(subjTrainDir + '/' + trainDay):
                    # If you have a training day directory

                    reachVidDirs = os.listdir(subjTrainDir + '/' + trainDay)
                    for reachVidDir in reachVidDirs:
                        # Walk through files in training day directory

                        if os.path.isdir(subjTrainDir + '/' + trainDay + '/' + reachVidDir):
                            # If you have a reach video directory
                            reachDir = subjTrainDir + '/' + trainDay + '/' + reachVidDir
                            reachVids = os.listdir(reachDir)
                            
                            for vid in reachVids:
                                # Walk through files in reach video directory
                                
                                if '._' in vid or ('mp4' not in vid and '.MP4' not in vid):
                                    # Skip invisible files
                                    continue

                                # Look at video files

                                vidIdentifiers = vid.split('_')
                                etNum = vidIdentifiers[0]
                                date = vidIdentifiers[1]
                                CCNum = vidIdentifiers[2]
                                
                                # Process based on calibration cube number
                                if '1' in CCNum:

                                    if date in CC1Dates:
                                        continue
                                    else:
                                        CC1Dates.append(date)
                                        
                                        [height, width, x1, x2, y1, y2] = cropFunc.getROI(reachDir + '/' + vid)

                                        CC1_directCrops.append((',').join([date,str(x1),str(x2),str(x1),str(y2)]))
                                        CC1_leftCrops.append((',').join([date,'0',str(x1),'0',str(y2)]))
                                        CC1_rightCrops.append((',').join([date,str(x1),str(width),'0',str(y2)]))
                                
                                elif '2' in CCNum:
                            
                                    if date in CC2Dates:
                                        continue
                                    else:
                                        CC2Dates.append(date)
                                        
                                        [height, width, x1, x2, y1, y2] = cropFunc.getROI(reachDir + '/' + vid)
                                        
                                        CC2_directCrops.append((',').join([date,str(x1),str(x2),str(x1),str(y2)]))
                                        CC2_leftCrops.append((',').join([date,'0',str(x1),'0',str(y2)]))
                                        CC2_rightCrops.append((',').join([date,str(x1),str(width),'0',str(y2)]))
                                        
                                
                        else:
                            # if you do not have a reach video directory, move on
                            continue
                else:
                    # If you do not have a training day directory, move on
                    continue
        else:
            # If you do not have a training directory, move on
            continue        
    else:
        # If you do not have a subject directory, move on
        continue                                    

cropFunc.writeToCSV(cropParamsDir + 'CC1_directCrops.csv',CC1_directCrops)
cropFunc.writeToCSV(cropParamsDir + 'CC1_leftCrops.csv',CC1_leftCrops)
cropFunc.writeToCSV(cropParamsDir + 'CC1_rightCrops.csv',CC1_rightCrops)
cropFunc.writeToCSV(cropParamsDir + 'CC2_directCrops.csv',CC2_directCrops)
cropFunc.writeToCSV(cropParamsDir + 'CC2_leftCrops.csv',CC2_leftCrops)
cropFunc.writeToCSV(cropParamsDir + 'CC2_rightCrops.csv',CC2_rightCrops)                                           
                                    
                                    
                
