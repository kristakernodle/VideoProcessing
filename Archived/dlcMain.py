#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 16:50:45 2019

@author: kkrista
"""

import setDLCFunc 

#Define local directories for video files
leftLocDir='/media/kkrista/KRISTAEHD/DLCSR/leftPaw/'
rightLocDir='/media/kkrista/KRISTAEHD/DLCSR/rightPaw/'

# Define docker container directories for vide files (kkristaEHD mounted at /opt/usb)
leftDocDir='/opt/usb/DLCSR/leftPaw/'
rightDocDir='/opt/usb/DLCSR/rightPaw/'

# Define local directories with the crop parameters for the training datasets
leftTrainCrop=''
rightTrainCrop=''

# Define location of crop parameter documents
leftCenterCropParam = '/home/kkrista/Documents/leftPP_Center-Krista-2019-01-23/cropParam.txt'
leftLeftCropParam = '/home/kkrista/Documents/leftPP_Left-Krista-2019-01-23/cropParam.txt'
leftRightCropParam = '/home/kkrista/Documents/leftPP_Right-Krista-2019-01-23/cropParam.txt'

rightCenterCropParam = '/home/kkrista/Documents/rightPP_Center-Krista-2019-01-23/cropParam.txt'
rightLeftCropParam = '/home/kkrista/Documents/rightPP_Left-Krista-2019-01-23/cropParam.txt'
rightRightCropParam = '/home/kkrista/Documents/rightPP_Right-Krista-2019-01-23/cropParam.txt'


# randVidSel(leftLocDir,50)
