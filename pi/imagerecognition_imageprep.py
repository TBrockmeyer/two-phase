# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 20:58:55 2016

@author: Michael Höh

Idea:
- load file
- do manual cropping
- compute mean across area along one axis, so that end up with 1D profile

"""


import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import os

folder = '/home/pi/PythonImage'

# load image
im1 = sp.misc.imread(file)

# trim image
trim = 1

if trim == 1:
    xmin = 650
    xmax = 1270
    #ymin = 550
    #ymax = 650
    
    #im2 = im1[xmin:xmax, ymin:ymax, :]
    im2 = im1[:, xmin:xmax, :]
else:
    im2 = im1

# compute means
im3 = sp.mean(im2, axis=1)

# merge into one
im4 = (im3[:,0] + im3[:,1] + im3[:,2])/3

# output
np.savetxt('extractsingle.csv', im4, delimiter=';')
