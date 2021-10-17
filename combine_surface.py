# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 18:18:29 2021

@author: rober
"""

import random

import numpy as np

import enumerate_surface

# Cache all the 4x4 surfaces
FOUR_BY_FOUR = enumerate_surface.all_surfaces(4, 4)

def get_random_four_by_four():
    surface = random.choice(FOUR_BY_FOUR)
    np_surface = np.zeros((4, 4), dtype=np.int32)
    
    for x in range(4):
        for y in range(4):
            np_surface[x, y] = surface[x, y]
    
    return np_surface

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
    Return whether the two given surfaces are compatible lengthwise,
    that is, whether adjacent values differ by at most one.
    """
    length, width = surface_1.shape
    for y in range(width):
        diff = abs(surface_1[length-1, y] - surface_2[0, y])
        if diff >= 2:
            return False
    
    return True

def lengthwise_append(surface_1, surface_2):
    return np.concatenate((surface_1, surface_2), axis=0)

def widthwise_compatible(surface_1, surface_2):
    """
    Return whether the two given surfaces are compatible widthwise,
    that is, whether adjacent values differ by at most one.
    """
    length, width = surface_1.shape
    for x in range(length):
        diff = abs(surface_1[x, width-1] - surface_2[x, 0])
        if diff >= 2:
            return False
    
    return True

def widthwise_append(surface_1, surface_2):
    return np.concatenate((surface_1, surface_2), axis=1)

def get_random_surface(num_steps):
    # If we don't do any doubling steps, just return a 4x4
    if num_steps == 0:
        return get_random_four_by_four()
    
    # If we do double,
    # get two double-length surfaces and combine them
    
    # Keep going until you get a match
    # for perfect sampling
    while True:
        # Get the two subsurfaces
        subsurface_1 = get_random_double_surface(num_steps)
        subsurface_2 = get_random_double_surface(num_steps)
        
        # Get the random displacement
        displacement = random.randint(-1, 1)
        
        # Align the subsurfaces using the displacement
        _, width = subsurface_1.shape
        subsurface_2_ul = subsurface_1[0, width-1] + displacement
        subsurface_2 += subsurface_2_ul
        
        # See if the subsurfaces match
        # if they match, we're done
        if widthwise_compatible(subsurface_1, subsurface_2):
            return widthwise_append(subsurface_1, subsurface_2)
        
        # They didn't match, so go again

def get_random_double_surface(num_steps):
    # Keep doing this until it works
    # for perfect sampling
    while True:
        # Get the two subsurfaces
        subsurface_1 = get_random_surface(num_steps-1)
        subsurface_2 = get_random_surface(num_steps-1)
        
        # Get the random displacement
        displacement = random.randint(-1, 1)
        
        # Align the surfaces using the displacement
        length, _ = subsurface_1.shape
        subsurface_2_ul = subsurface_1[length-1, 0] + displacement
        subsurface_2 += subsurface_2_ul
        
        # See whether the subsurfaces match
        # if they match, we're done
        if lengthwise_compatible(subsurface_1, subsurface_2):
            return lengthwise_append(subsurface_1, subsurface_2)
        
        # They didn't match, so go again