#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DLC Video Selection

Created on Tue Jan 22 12:15:44 2019
@author: kkrista

This script will search through files in a specified directory in order to 
randomly select 200 videos, of which a random frame will be selected to define
the training set for DLC.
"""

import os
import random
import numpy as np

dir = '/media/kkrista/KRISTAEHD/DLCSR/leftPaw/'

trainFiles = [None] * 50

allFiles = os.listdir(dir)

allFiles = allFiles[3:]

maxNum = len(allFiles)

vidInd = random.sample(range(0,maxNum),50)

for num in vidInd:
    vidNum = vidInd.index(num)
    trainFiles[vidNum] = allFiles[num]
    
np.savetxt("trainFiles.csv",trainFiles,delimiter=",",fmt='%s')

    
    
