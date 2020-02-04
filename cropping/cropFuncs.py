#!/usr/bin/env python3

"""
Created on Thu Jan 24 15:57:44 2019

@author: kkrista
"""
import os
import random
import numpy as np
import cv2
from pathlib import Path

def readfile(F):
    with open(F) as f:
        return f.read().splitlines()

def writeToCSV(saveFullFilename,itemsList):
    # This function writes a list (any size) to a csv
    
    # INPUT:
        # saveFullFilename - full path directory, including filename and extension
        #       for saved file
        # itemsList - list that will be saved into file provided in saveFullFilename
    
    # OUTPUT:
        # File, specified by saveFullFilename
        
    with open(saveFullFilename,'w') as f:
        for item in itemsList:
            f.writelines("%s" % item)
            f.write("\n")
    f.close()

def randVidSel(vidDir,numVids,wrkDir):
    trainFiles = [None] * numVids
    allFiles = os.listdir(vidDir)
    maxNum = len(allFiles)
    print(maxNum)
    vidInd = random.sample(range(0,maxNum),numVids)
    
    for num in vidInd:
        vidNum = vidInd.index(num)
        trainFiles[vidNum] = allFiles[num]
    
    np.savetxt(wrkDir+"/trainFiles.csv",trainFiles,delimiter=",",fmt='%s')

def getROI(vidFile):
    vidcap = cv2.VideoCapture(vidFile)
    success, image = vidcap.read()
    if success is False:
        return print('Empty Video')
    small = cv2.resize(image,(0,0),fx=0.5,fy=0.5)
            
    r = cv2.selectROI(small)
    r = np.array(r)
    r = 2*r

    x1 = str(r[0])
    x2 = str(r[0]+r[2])
    y1 = str(r[1])
    y2 = str(r[1]+r[3])
                                            
    width = vidcap.get(3)
    height = vidcap.get(4)

    cv2.destroyAllWindows()
    vidcap.release()
    return height, width, x1, x2, y1, y2

# def getROI(locVidDir,docVidDir,wrkDir,trainFcsv):
#     cropParamDir=wrkDir+"/cropParameters.txt"
#     train=[]
#     g=[]
#     h=[]
#     origVids = []
#     a=[]
#     compName=[]
    
#     cropParamFile=Path(cropParamDir)
#     if cropParamFile.is_file():
#         f=readfile(cropParamDir)            
#         writeIt = open(cropParamDir,'w')
#     else:
#         writeIt = open(cropParamDir,'w+')
    
#     ff=readfile(wrkDir+"/trainFiles.csv")
    
#     cc=0
#     while cc < len(ff):
#         train.append(docVidDir+ff[cc])
#         cc+=1
        
#     os.chdir(locVidDir)
#     fullfiles = os.listdir()
            
#     ii = 0
#     while ii < len(fullfiles):
#         docVidPath = docVidDir + fullfiles[ii]
#         locVidPath = locVidDir + fullfiles[ii]
    
#         #if compName[ii] not in origVids:
#         #origVids.append(compName[ii])
            
#         vidcap = cv2.VideoCapture(locVidPath)
#         success, image = vidcap.read()
#         small = cv2.resize(image,(0,0),fx=0.5,fy=0.5)
            
#         r = cv2.selectROI(small)
#         r = np.array(r)
#         r = 2*r

#         x1 = str(r[0])
#         x2 = str(r[0]+r[2])
#         y1 = str(r[1])
#         y2 = str(r[1]+r[3])

#         writeIt.write("%s\n" % docVidPath)
#         writeIt.write("%s, %s, %s, %s\n" %(x1,x2,y1,y2))
        
#         #else:
#             #writeIt.write("%s:\n" % docVidPath)
#             #writeIt.write("crop: %s, %s, %s, %s\n" %(x1,x2,y1,y2))
        
#         ii += 1

#     writeIt.close()

def multiNet(projName,locVidDir,docVidDir):
    file=readfile('/home/kkrista/Documents/Script/dlcVar.txt')
    projNameInd=file.index("# Variables")+2
    locVidDirInd=projNameInd+3
    docVidDirInd=locVidDirInd+1
    
    writeFile=open('/home/kkrista/Documents/Script/dlcVar.txt','w')
    
    for line in file[0:projNameInd]:
        writeFile.write('%s\n' %line)
    writeFile.write('projName="%s"\n' %projName)
    for line in file[projNameInd+1:locVidDirInd]:
        writeFile.write('%s\n' %line)
    writeFile.write('locVidDir="%s"\n' %locVidDir)
    writeFile.write('docVidDir="%s"\n' %docVidDir)
    for line in file[docVidDirInd+1:]:
        writeFile.write('%s\n' %line)
        
    writeFile.close()
