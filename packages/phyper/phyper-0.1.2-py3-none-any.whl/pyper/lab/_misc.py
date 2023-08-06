#misc functions 
import re
import cv2
import png
import numpy as np
import os

import tifffile


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def read_png(path):
    #read image using openCV
    im = cv2.imread(path, cv2.IMREAD_ANYDEPTH)

    #check image metadata using png reader
    meta = png.Reader(path)
    meta.preamble()
    significant_bits = ord(meta.sbit)
    
    im = np.right_shift(im,16-significant_bits)
    return im

def imread(path):
    _, file_extension = os.path.splitext(path)
    if file_extension == '.png':
        return read_png(path)
    elif file_extension == '.tiff':
        return tifffile.imread(path)
    else:
        return cv2.imread(path, cv2.IMREAD_ANYDEPTH)