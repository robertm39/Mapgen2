# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 20:38:11 2021

@author: rober
"""

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