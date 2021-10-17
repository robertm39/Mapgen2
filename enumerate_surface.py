# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 16:37:10 2021

@author: rober
"""

def near(i):
    return (i-1, i, i+1)

def union(p1, p2):
    return tuple(p for p in p1 if p in p2)

def all_surfaces(length=3, width=3, fixed=None, to_fix=None):
    if fixed is None:
        fixed = {(0, 0): 0}
        
        # What we should fix next
        to_fix = (1, 0) if length >= 2 else (0, 1)
    
    # If everything is fixed, we have a possibility
    if len(fixed) == length*width:
        return [fixed]
    
    # Determine what spot the next one should fix
    x, y = to_fix
    
    next_x = x + 1
    next_y = y
    
    if next_x >= length:
        next_x = 0
        next_y += 1
    
    next_to_fix = next_x, next_y
    
    # Determine what values we can fix the spot as
    
    # There's a value to the left and above
    if x > 0 and y > 0:
        prev_val_x = fixed[x-1, y]
        prev_val_y = fixed[x, y-1]
        
        possibilities = union(near(prev_val_x), near(prev_val_y))
    # There's a value to the left but not above
    elif x > 0 and y == 0:
        prev_val_x = fixed[x-1, y]
        possibilities = near(prev_val_x)
    # There's a value above but not to the left
    elif y > 0 and x == 0:
        prev_val_y = fixed[x, y-1]
        possibilities = near(prev_val_y)
    else:
        raise ValueError('x: {}, y: {}'.format(x, y))
    
    result = list()
    for value in possibilities:
        new_fixed = fixed.copy()
        new_fixed[to_fix] = value
        
        result_with_fixed = all_surfaces(length,
                                         width,
                                         fixed=new_fixed,
                                         to_fix=next_to_fix)
        result.extend(result_with_fixed)
    
    return result