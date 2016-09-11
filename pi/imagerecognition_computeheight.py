# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 18:32:33 2016

@author: Michael Höh

Idea:
- load file with previously computed 1D profile across the interface
- do some analysis on properties of curves - needs some more work
- fit sigmoid function to curve, plot, output plot
- get height from sigmoid, output
"""

import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import os

folder = '/home/pi/PythonImage'
file = 'extracteddata.csv'

data = np.loadtxt(os.path.join(folder, file), delimiter=';')
data = data.T

for k, i in enumerate(data):
    plt.plot(i, label=str(k))
plt.legend()

# algo determining basic things for curve fitting
# i.e. determinig if upper or lower phase is the one with higher grey value
# i.e. determining if interface layer shows higher grey value than other parts

# first check stds
datastd = np.std(data, axis=1)
datamean = np.mean(data, axis=1)
datarelstd = datastd/datamean

# discard if relstd < 2%
datasel = datarelstd > 0.02

# smooth curve 
import scipy.signal as sps
data_sg = sps.savgol_filter(data, window_length = 11, polyorder = 1, axis=1)

# determine if there is a hill in between the start and end
# so essentially if x_middle >/< x_start | x_middle >/< x_end
i = 1

for i in range(8):
    length = data_sg[i].shape[0]
    len_offset = np.int(np.round(0.1*length))
    mean_start = np.mean(data_sg[i, :len_offset])
    mean_end = np.mean(data_sg[i, length - len_offset:length])
    max_middle = np.max(data_sg[i, len_offset:length-len_offset])
    min_middle = np.min(data_sg[i, len_offset:length-len_offset])
    
    offset_factor = 0.2
    
    if mean_end > mean_start:
        if (mean_end < 1+offset_factor * max_middle or
            mean_start * (1-offset_factor) > min_middle):
            print(i) 
    if mean_end < mean_start:
        if (mean_end > 1+offset_factor * max_middle or
            mean_start * (1-offset_factor) < min_middle):
            print(i) 

fittedparams = np.zeros([len(data),4])
heightmm = np.zeros([len(data),1])

# run through all samples, fit sigmoid, plot curves and output
for i in range(len(data)):
    fig = plt.figure()
    #sel = 7
    sel = i
    data_single = data[sel]
    
    # curve fitting
    import scipy.optimize as spio
    
    def sigmoid_function(xdata, x0, k, a, b):
        y = a + b*(1 - np.exp(-k*(xdata-x0)) / (1 + np.exp(-k*(xdata-x0))))
        return y
    
    xdata = np.arange(len(data_single))
    ydata = data_single
    
    initial_guess = [300, 0.05, 75, 120]
    
    popt, pcov = spio.curve_fit(sigmoid_function, xdata, ydata, p0=initial_guess)
    fittedparams[i] = popt    
    
    plt.plot(sigmoid_function(xdata, popt[0], popt[1], popt[2], popt[3]), label='fitted curve')
    plt.plot(xdata, ydata, label='measurement')
    plt.legend(bbox_to_anchor=(1.45, 1.02),)
    plt.xlabel('height')
    plt.ylabel('intensity')
    
    fig.savefig("curve_"+str(i)+".png", dpi=300, bbox_inches='tight') 

    # calc height im mm
    # 1 pixel = 0.0333mm
    heightmm[i] = (fittedparams[i, 0] + 240)*11/330 

# export computed height and fit parameters
np.savetxt('curve_heightmm.txt', heightmm, delimiter=';')
np.savetxt('curve_fittedparams.txt', fittedparams, delimiter=';')
