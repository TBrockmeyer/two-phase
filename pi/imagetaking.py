# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 09:07:34 2016

@author: Michael Höh
"""

from picamera import PiCamera

camera = PiCamera()

file = 'captured.jpg'
camera.capture(file)
