# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 18:18:29 2021

@author: rober
"""

def plus(surface, amount):
    result = dict()
    for coords, value in surface.items():
        result[coords] = value + amount
    return result

def lengthwise_match(surface_1, surface_2, length, width):
    """
    Return whether the two given surfaces match horizontally.
    """
    for y in range(width):
        # diff = abs(surface_1[length-1, y] - surface_2[0, y])
        if surface_1[length-1, y] != surface_2[0, y]:
            return False
    
    return True

def lengthwise_stitch(surface_1, surface_2, length, width):
    """
    Return the two sursfaces, appended along the length dimension.
    """
    
    # Start with the first surface
    result = surface_1.copy()
    
    # Add the second surface at the end
    for coords, value in surface_2.items():
        x, y = coords
        x += length - 1
        result[x, y] = value
    
    return result

# Now using numpy arrays
# which will make things much easier

def lengthwise_compatible(surface_1, surface_2):#, length, width):
    """
    Return whether the two given surfaces are compatible horizontally,
    that is, whether adjacent values differ by at most one.
    """
    length, width = surface_1.shape
    for y in range(width):
        diff = abs(surface_1[length-1, y] - surface_2[0, y])
        if diff >= 2:
            return False
    
    return True

def lengthwise_append(surface_1, surface_2):
    