# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 13:16:54 2021

@author: Robert Morton
"""

import random

import numpy as np

# Surfaces will be represented with Numpy arrays for fast math

DTYPE = np.float64

def get_random_walk(length, step=None):
    """
    Return a random walk of the given length.
    
    Parameters:
        length int:
            The length of the random walk.
        step () -> number:
            The step function.
    
    Return:
        A random walk of the given length using the given step function.
    """
    if step is None:
        step = lambda: random.uniform(-1, 1)
    
    walk = np.zeros(length, dtype=DTYPE)
    for i in range(1, length):
        walk[i] = walk[i-1] + step()
    
    return walk

def constrained_step(prev_val, parallel_val):
    lower_bound = max(prev_val - 1, parallel_val - 1)
    upper_bound = min(prev_val + 1, parallel_val + 1)
    
    return random.uniform(lower_bound, upper_bound)

def get_parallel_random_walk(length, walk, step=constrained_step):
    """
    Return a random walk restrained by a given random walk.
    
    Parameters:
        length int:
            The length of the walk.
        walk array:
            The walk to be restrained by.
        step (prev_val, parallel_val) -> number:
            The step function.
    
    Return:
        A random walk constrained by the given walk.
    """
    walk = np.zeros(length, dtype=DTYPE)
    

def get_random_walk_surface(length, width):
    pass