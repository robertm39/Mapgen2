# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 20:38:11 2021

@author: rober
"""

import numpy as np

def square_blur(surface):
    """
    Apply a square blur filter to the given surface.
    """
    width, height = surface.shape
    
    upper_left = surface[:-1, :-1]
    upper_right = surface[1:, :-1]
    lower_left = surface[:-1, 1:]
    lower_right = surface[1:, 1:]
    
    return sum([upper_left, upper_right, lower_left, lower_right]) / 4.0

def scale(surface):
    min_val = np.amin(surface)
    max_val = np.amax(surface)
    diff = max_val - min_val
    
    scaled = (surface - min_val) / diff
    scaled *= 255
    
    scaled = np.round(scaled)
    scaled = np.array(scaled, dtype=np.unit255)