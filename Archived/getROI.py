#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:14:16 2019

@author: kkrista
"""

import cv2
import os
import numpy as np
import setDLCFunc

locVidDir = '/media/kkrista/KRISTAEHD/DLCSR/leftPaw/'
docVidDir = '/opt/usb/DLCSR/leftPaw/'
cropParamDir = '/home/kkrista/Documents/leftPP_Left-Krista-2019-01-24/cropParam.txt'
trainFcsv = '/home/kkrista/Documents/leftPP_Left-Krista-2019-01-24/trainFiles.csv'
trainCropParam = '/home/kkrista/Documents/leftPP_Left-Krista-2019-01-24/trainCropParam.txt'

f=setDLCFunc.readfile(cropParamDir)
ff=setDLCFunc.readfile(trainFcsv)

writeIt = open(cropParamDir,'w')
writeConfigCrop = open(trainCropParam,'w')

train=[]
g=[]
h=[]
origVids = []
configCrop = []
a=[]
compName=[]

cc=0
while cc < len(ff):
    train.append('/opt/usb/DLCSR/leftPaw/'+ff[cc])
    cc+=1

cc=0
while cc < len(f):
    g=f[cc].split('/')
    h=g[-1].split('_')
    vid=h[0]+'_'+h[1]+'_'+h[2]
    origVids.append(vid)
    cc+=2

os.chdir(locVidDir)
fullfiles = os.listdir()

dd=0
while dd < len(fullfiles):
    a=fullfiles[dd].split('_')
    b=a[0]+'_'+a[1]+'_'+a[2]
    compName.append(b)
    dd+=1

ii = 0
while ii < len(fullfiles):
    
    docVidPath = docVidDir + fullfiles[ii]
    locVidPath = locVidDir + fullfiles[ii]
    
    if compName[ii] not in origVids:
        origVids.append(compName[ii])
        vidcap = cv2.VideoCapture(locVidPath)
        success, image = vidcap.read()

        small = cv2.resize(image,(0,0),fx=0.5,fy=0.5)
        r = cv2.selectROI(small)

        r = np.array(r)
        r = 2*r

        x1 = str(r[0])
        x2 = str(r[0]+r[2])
        y1 = str(r[1])
        y2 = str(r[1]+r[3])

        writeIt.write("  %s:\n" % docVidPath)
        writeIt.write("    crop: %s, %s, %s, %s\n" %(x1,x2,y1,y2))
    else:
        writeIt.write("  %s:\n" % docVidPath)
        writeIt.write("    crop: %s, %s, %s, %s\n" %(x1,x2,y1,y2))
    
    if docVidPath in train:
        writeConfigCrop.write("  %s:\n" % docVidPath)
        writeConfigCrop.write("    crop: %s, %s, %s, %s\n" %(x1,x2,y1,y2))
        
    ii += 1

writeIt.close()
writeConfigCrop.close()




