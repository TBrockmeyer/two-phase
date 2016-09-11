# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 09:07:34 2016

@author: Michael Höh
"""

from picamera import PiCamera
from time import sleep

camera = PiCamera()


camera.start_preview()
sleep(10000)
camera.stop_preview()

