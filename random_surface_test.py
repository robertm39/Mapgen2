# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 14:23:37 2021

@author: rober
"""

import numpy as np
import matplotlib.pyplot
from IPython.display import display
import random

from PIL import Image, ImageDraw

import random_surface
import enumerate_surface

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def plot_walk(walk):
    xs = list()
    ys = list()
    
    length = walk.shape[0]
    
    for x in range(length):
        xs.append(x)
        ys.append(walk[x])
    
    matplotlib.pyplot.scatter(xs, ys, marker='.')

def walk_test():
    walk = random_surface.get_random_walk(10)
    plot_walk(walk)

def get_water_level_image(surface, water_level, pixel_size):
    width, height = surface.shape
    
    image = Image.new('RGB', (width * pixel_size, height * pixel_size))
    draw = ImageDraw.Draw(image)
    
    for x in range(width):
        for y in range(height):
            color = GREEN
            if surface[x, y] <= water_level:
                color = BLUE
            
            ix = x * pixel_size
            iy = y * pixel_size
            
            draw.rectangle([ix, iy, ix+pixel_size-1, iy+pixel_size-1],
                           fill=color,
                           outline=None,
                           width=0)
    
    return image

def display_water_levels(surface, num_levels, pixel_size):
    min_value = np.amin(surface)
    max_value = np.amax(surface)
    
    step = (max_value - min_value) / (num_levels - 1)
    
    for i in range(num_levels):
        water_level = min_value + i * step
        image = get_water_level_image(surface, water_level, pixel_size)
        display(image)

def display_surface(surface):
    min_value = np.amin(surface)
    max_value = np.amax(surface)
    diff = max_value - min_value
    
    im_array = np.zeros_like(surface, dtype=np.uint8)
    width, height = surface.shape
    
    for x in range(width):
        for y in range(height):
            val = surface[x, y]
            proportion = (val - min_value) / diff
            intensity = round(255 * proportion)
            
            im_array[x, y] = intensity
    
    image = Image.fromarray(im_array, mode='L')
    
    # image = image.resize((200, 200), resample=Image.NEAREST)
    
    display(image)

def surface_test():
    length = 200
    width = 200
    
    surface = random_surface.get_random_surface(length, width)
    
    display_surface(surface)
    
    # display_water_levels(surface, 6, 1)
    
    # for z in range(width):
    #     s = '\t' + '{:.2f}\t' * length
    #     print(s.format(*surface[:, z]))

def get_layer(surface, length, y=0):
    return tuple([(x, surface[x, y]) for x in range(length)])

def get_layer_counts(surfaces, length, y=0):
    counts_from_tops = dict()
    for surface in surfaces:
        top = get_layer(surface, length, y=y)
        if not top in counts_from_tops:
            counts_from_tops[top] = 1
        else:
            counts_from_tops[top] += 1
    return counts_from_tops

def as_string(t_walk):
    return ('{:3d}' * len(t_walk)).format(*[y for _, y in t_walk])

def print_surface(surface, length, width):
    for y in range(width):
        layer = get_layer(surface, length, y)
        print(as_string(layer))

def all_surface_test():
    side = 4
    print('{}x{} surfaces:'.format(side, side))
    surfaces = enumerate_surface.all_surfaces(side, side)
    print('{} surfaces'.format(len(surfaces)))
    # counts_from_tops = get_layer_counts(surfaces, side)
    
    for _ in range(5):
        print('')
        surface = random.choice(surfaces)
        print_surface(surface, side, side)
    
    # for top, count in counts_from_tops.items():
    #     print('{}:  {} times'.format(as_string(top), count))

def main():
    # walk_test()
    # surface_test()
    all_surface_test()
    
if __name__ == '__main__':
    main()