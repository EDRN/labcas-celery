#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Image alignment (translation) of multi-channel frames
    
    A tissue image consists of multiple rounds of scanning.  Each round is saved 
    in a subfolder.  Within each round, there are DAPI and several non-DAPI 
    channels present, as individual TIF files.  Within each round, non-DAPI 
    channels are assumed to be aligned with the DAPI channel of that round.  
    However, different rounds may be translated across rounds.
    
    This script aligns all channels across all rounds.  First, a random round
    is fixed.  Then, all other rounds are aligned to the fixed round by first 
    aligning the DAPI channels and subsequently translating the non-DAPI channels
    of that round.  Output is written to a new folder with the same structure.  
    
    Some of the frame sizes are found to be inconsistent across individual frames.
    We 0-pad all frames to the size of the largest frame.
'''

import numpy as np
import sys

from PIL import Image
# need to increase the limit to accommodate large size images
# may want to check the physical memory limitations if any
# each frame can grow up to ~3GB in size
Image.MAX_IMAGE_PIXELS = None

from skimage.feature import register_translation

import tifffile
import glob2
import os


def pad_frame(f1, mx, my):
    ''' pad smaller sized frames to the largest frame size '''
    if f1.shape[0] < mx:
        f1 = np.pad(f1, [(0,mx-f1.shape[0]), (0,0)], mode='constant')
    if f1.shape[1] < my:
        f1 = np.pad(f1, [(0,0), (0,my-f1.shape[1])], mode='constant')
    return f1


def get_max_frame_size(tif_files):
    ''' guard for inconsistent frame sizes, use the largest frame size for all'''
    maxx = 0
    maxy = 0
    for f in tif_files:
        tif = tifffile.TiffFile(f)
        x, y = tif.pages[0].shape[0:2]
        maxx = max(maxx,x)
        maxy = max(maxy,y)
    return maxx, maxy        


def register_folder(fixed_dapi, dapi_file, mx, my, in_folder, out_folder):
    ''' each folder can be registered asynchronously '''

    # this is the folder to be registered against fixed_dapi
    dapi_folder = os.path.split(dapi_file)[0]
    # all the files in this folder
    files = glob2.glob(os.path.join(dapi_folder,'*.tif'))
    # these are non-dapi channels that will be translated
    # after registering the dapi channel
    non_dapi_files = [f for f in files if f.lower().find('dapi')==-1]
    
    # register dapi channels
    im1 = tifffile.imread(fixed_dapi)
    im1 = np.squeeze(im1)
    im1 = pad_frame(im1,mx,my)

    im2 = tifffile.imread(dapi_file)
    im2 = np.squeeze(im2)
    im2 = pad_frame(im2,mx,my)
    
    print('Registering:')
    print('Fixed: ',fixed_dapi)
    print('With: ',dapi_file)
    shift, error, diffphase = register_translation(im1, im2, upsample_factor=2)
    
    im2 = np.roll(im2, shift.astype(int), [0,1])
    print('Writing: ',dapi_file.replace(in_folder,out_folder))
    tifffile.imwrite(dapi_file.replace(in_folder,out_folder), data=im2)

    # construct an rgb frame for visual validation
    # remove the comments below to print out validation frames
    # im_zero = np.zeros((maxx,maxy), dtype=np.uint8)
    # rgb = np.dstack([im1, im_zero, im2])
    # rgb_file = df.replace('.tif','_rgb.tif')
    # tifffile.imwrite(rgb_file.replace(inputpath.split(os.path.sep)[-2],outputpath.split(os.path.sep)[-2]),data=rgb)

    # translate all non-dapi channels in this round
    for f in non_dapi_files:
        im2 = tifffile.imread(f)
        im2 = np.squeeze(im2)
        im2 = pad_frame(im2, mx, my)
        im2 = np.roll(im2, shift.astype(int), [0,1])
        print('Writing: ',f.replace(in_folder,out_folder))        
        tifffile.imwrite(f.replace(in_folder,out_folder), data=im2)

    return 'done: '+dapi_file


def main(input_path, output_path, parallel=1):
    # split processing over multiple cores
    # or just turn it off and call registration sequentially
    #parallel = 1

    input_folder = input_path.split(os.path.sep)[-2]
    output_folder = output_path.split(os.path.sep)[-2]
    
    # copy folder structure
    for dirpath, dirnames, filenames in os.walk(input_path):
        structure = os.path.join(output_path, dirpath[len(input_path):])
        if not os.path.isdir(structure):
            os.mkdir(structure)
        else:
            print('Folder already exists.')
    
    
    # we'll scan all files for the largest image size
    tif_files = glob2.glob(os.path.join(input_path, '**/*.tif'))
    
    # all dapi-channels
    dapi_files = [f for f in tif_files if f.lower().find('dapi') > 0]
    
    # largest image size
    mx,my = get_max_frame_size(tif_files)
    
    # anchor round, againt which we register all other rounds
    dapi_fixed = dapi_files.pop()
    
    # make a copy of the fixed foldern to the destination
    fixed_folder = os.path.split(dapi_fixed)[0]
    fixed_files = glob2.glob(os.path.join(fixed_folder, '**/*.tif'))
    for f in fixed_files:
        im1 = tifffile.imread(f)
        im1 = np.squeeze(im1)
        im1 = pad_frame(im1, mx, my)
        tifffile.imwrite(f.replace( input_folder , output_folder ),data=im1)
        
    if parallel:
        import multiprocessing as mp
        pool = mp.Pool(mp.cpu_count())
        results = [pool.apply_async(register_folder, args=(dapi_fixed, f, mx, my, input_folder, output_folder)) for f in dapi_files]
        pool.close()
        pool.join()
        [print(r) for r in results]
    else:
        for f in dapi_files:
            register_folder(dapi_fixed, f, mx, my, input_folder, output_folder)


if __name__ == "__main__":
    
   (input_path, output_path) = sys.argv[1:]
   print("input_path = %s" % input_path)
   print("output_path = %s" % output_path)
   main(input_path, output_path)

