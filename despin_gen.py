# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 09:31:51 2021

@author: rober
"""

import numpy as np

def random_diffs(length, width):
    """
    Return random differences along the length and width dimensions.
    """
    # Differences along the length (x) dimension.
    l_diffs = np.random.rand(length-1, width) * 2 - 1
    
    # Differences along the width (y) dimension.
    w_diffs = np.random.rand(length, width-1) * 2 - 1
    
    return l_diffs, w_diffs

def despin_matrix_row(l_diffs, w_diffs, x, y):
    """
    Return one row of the despinning matrix and the corresponding target value.
    """
    
    # Calculate the current spin
    l_spin = l_diffs[x, y + 1] - l_diffs[x, y]
    w_spin = w_diffs[x, y] - w_diffs[x + 1, y]
    spin = l_spin + w_spin
    
    width = l_diffs.shape[1]
    length = w_diffs.shape[0]
    
    # Calculate the coefficients for the current row
    spin_coeffs = np.zeros((length-1, width-1))
    
    # The spin for the current coords
    spin_coeffs[x, y] = 4
    
    # The interfering spin from the surrounding coords, if applicable
    if x >= 1:
        spin_coeffs[x - 1, y] = -1
    
    if x < length - 2:
        spin_coeffs[x + 1, y] = -1
    
    if y >= 1:
        spin_coeffs[x, y - 1] = -1
    
    if y < length - 2:
        spin_coeffs[x, y + 1] = -1
    
    # Flatten the coefficient matrix to get a row
    row = np.reshape(spin_coeffs, -1)
    
    return row, spin

def despin_diffs(l_diffs, w_diffs):
    """
    Remove spin from the given differences.
    """
    
    width = l_diffs.shape[1]
    length = w_diffs.shape[0]
    
    # Assemble a matrix to represent the linear equation.
    rows = list()
    spins = list()
    for x in range(length-1):
        for y in range(width-1):
            # Get the spin coeffs and target spin for this spot
            row, spin = despin_matrix_row(l_diffs, w_diffs, x, y)
            rows.append(row)
            spins.append(spin)
    
    # Assemble the spin matrix and spins
    spin_matrix = np.stack(rows, axis=1)
    spins = np.matrix(spins).T
    
    # Get the despins
    despins = np.linalg.solve(spin_matrix, spins)
    
    print(despins)

def get_spins(l_diffs, w_diffs):
    left_w_diffs = w_diffs[:-1, :]
    right_w_diffs = w_diffs[1:, :]
    
    top_l_diffs = l_diffs[:, :-1]
    bottom_l_diffs = l_diffs[:, 1:]
    
    l_spin = bottom_l_diffs - top_l_diffs
    w_spin = left_w_diffs - right_w_diffs
    
    return l_spin + w_spin

def get_step(spins):
    length = spins.shape[0] + 1
    width = spins.shape[1] + 1
    
    shifted_spins_1 = np.concatenate((spins[1:, :], np.zeros((1, width-1))), axis=0)
    shifted_spins_2 = np.concatenate((np.zeros((1, width-1)), spins[:-1, :]), axis=0)
    
    shifted_spins_3 = np.concatenate((spins[:, 1:], np.zeros((length-1, 1))), axis=1)
    shifted_spins_4 = np.concatenate((np.zeros((length-1, 1)), spins[:, :-1]), axis=1)
    
    total_shifted = shifted_spins_1 + shifted_spins_2 + shifted_spins_3 + shifted_spins_4
    mean_shifted = total_shifted / 4
    
    return spins + mean_shifted
    # return -mean_shifted

def despin_step(l_diffs, w_diffs, spins, alpha, prev_step=0, momentum=0):
    width = l_diffs.shape[1]
    length = w_diffs.shape[0]
    
    # spin_inc = spins * alpha
    spin_inc = get_step(spins) * alpha + prev_step * momentum
    
    # The spins for w_diffs[x, y]
    # add a column of zeros to end the spins
    padded_spins_1 = np.concatenate((spin_inc, np.zeros((1, width-1))), axis=0)
    w_diffs = w_diffs - padded_spins_1
    
    # The spins for w_diffs[x + 1, y]
    # add a column of zeros to the beginning of the spins
    padded_spins_2 = np.concatenate((np.zeros((1, width-1)), spin_inc), axis=0)
    w_diffs = w_diffs + padded_spins_2
    
    # The spins for l_diffs[x, y]
    # add a row of zeros to the end of the spins
    padded_spins_3 = np.concatenate((spin_inc, np.zeros((length-1, 1))), axis=1)
    l_diffs = l_diffs + padded_spins_3
    
    # The spins for l_diffs[x, y+1]
    # add a row of zeros to the beginning of the spins
    padded_spins_4 = np.concatenate((np.zeros((length-1, 1)), spin_inc), axis=1)
    l_diffs = l_diffs - padded_spins_4
    
    return l_diffs, w_diffs, spin_inc

def iter_despin_diffs(l_diffs, w_diffs, num_iters=1, alpha=1/4):
    step = 0
    for i in range(num_iters):
        spins = get_spins(l_diffs, w_diffs)
        
        i += 1
        if i % 100 == 0:
            norm = np.sqrt(np.mean(spins * spins))
            print('{:6d}: spins norm: {}'.format(i, norm))
        
        l_diffs, w_diffs, step = despin_step(l_diffs,
                                             w_diffs,
                                             spins,
                                             alpha,
                                             prev_step=step,
                                             momentum=0.99)
    
    spins = get_spins(l_diffs, w_diffs)
    norm = np.sqrt(np.mean(spins * spins))
    print('\nspins norm: {}'.format(norm))
    # print('')
    # print('spins:')
    # print(spins)
    
    return l_diffs, w_diffs

def get_surface_from_diffs(l_diffs, w_diffs):
    length = w_diffs.shape[0]
    width = l_diffs.shape[1]
    
    surface = np.zeros((length, width))
    
    # Construct the surface one row at a time
    # if the given differences are circularity-free, order doesn't matter
    for y in range(width):
        # Get the start value
        if y > 0:
            surface[0, y] = surface[0, y - 1] + w_diffs[0, y - 1]
        
        for x in range(1, length):
            surface[x, y] = surface[x - 1, y] + l_diffs[x - 1, y]
    
    return surface