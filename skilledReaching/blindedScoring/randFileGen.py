#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 10:24:16 2019

@author: kkrista
"""
import random

def randFilenameGen():
    name = []
    el = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
    for x in range(10):
        a = random.randint(0,35)
        name.append(el[a])
    name = ''.join(name)
    return name