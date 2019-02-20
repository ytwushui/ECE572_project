#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 21:24:25 2018

@author: ywu
"""

from PIL import Image, ImageFilter
import cv2
import os

dataroot = os.getcwd() + "/equations/"
im=cv2.imread(dataroot+"SKMBT_36317040717260_eq2.png",1)

cv2.imshow("image",im)
cv2.waitKey(500)
cv2.dstroyAllWindows()