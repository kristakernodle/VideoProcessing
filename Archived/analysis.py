#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 15:16:49 2019

@author: kkrista
"""

import deeplabcut
import os
os.chdir('/home/kkrista/Documents/Script/PythonScripts/')
from setDLCFunc import readfile

config_path='/home/kkrista/Documents/rightPP_Center-Krista-2019-02-09/config.yaml'
crops=readfile('/home/kkrista/Documents/rightPP_Center-Krista-2019-02-09/cropParameters.txt')
vids = os.listdir('/opt/usb/DLCSR/rightPaw/')
allVids=['']*len(vids)
for ii in range(len(vids)):
    allVids[ii]='/opt/usb/DLCSR/rightPaw/'+vids[ii]


    
for ii in range(len(allVids)):
    if '710_20181126_01' in allVids[ii]:                                                               
        ind=crops.index(allVids[ii])
        params=crops[ind+1].split(', ')                                                   
	    cfg=deeplabcut.utils.auxiliaryfunctions.read_config(config_path)
        cfg['cropping']=true
	    cfg['x1']=int(params[0])
	    cfg['x2']=int(params[1])
	    cfg['y1']=int(params[2])
	    cfg['y2']=int(params[3])

	    deeplabcut.utils.auxiliaryfunctions.write_config(config_path,cfg)
	    print('CFG Updated')                                                                 
	    deeplabcut.analyze_videos(config_path,allVids[ii], shuffle=1, save_as_csv=True)
