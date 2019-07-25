#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
# import skimage
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

from skimage.feature import register_translation

import tifffile
import glob2
import os
import sys

if __name__ == "__main__":
    
   (input_dir, output_dir) = sys.argv[1:]
   print("input dir=%s" % input_dir)
   print("output_dir dir=%s" % output_dir)
