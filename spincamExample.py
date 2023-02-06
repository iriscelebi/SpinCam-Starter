#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 12:58:55 2023

@author: iris.celebi
"""


import sys
import spincam
import os
import imageio
import numpy as np
import time

"""

Example code to acquire an image with FLIR cameras

"""



def find_and_init_cam():
    print('Connecting camera...')        
    spincam.find_cam('test')       
    spincam.init_cam()
    spincam.disable_auto_exp()
    spincam.disable_auto_gain()
    spincam.disable_auto_frame()
    spincam.set_gain(0)
    
    
def start_stream():
    print('Starting stream...')
    # Set buffer to newest only
    spincam.cam_node_cmd('TLStream.StreamBufferHandlingMode','SetValue','RW','PySpin.StreamBufferHandlingMode_NewestOnly')
    # Set acquisition mode to continuous
    spincam.cam_node_cmd('AcquisitionMode','SetValue','RW','PySpin.AcquisitionMode_Continuous')
    # Start acquisition
    spincam.start_acquisition()
    time.sleep(0.1)
    
    
    
def acquire_single():
    start_stream()
    num_to_avg = 10
    image_dict = spincam.get_image_and_avg(num_to_avg)
    
    name_format = 'image_name'
    directory = os. getcwd() # or your own directory via filedialog.askdirectory() + '/'
    directory = directory + '/'
    
    
    imName = directory + name_format + '.tiff'
    print('Starting save ' + imName)
    
    if 'data' in image_dict:
        data=image_dict['data'].astype(np.uint16)
        imageio.imwrite(imName, data)               #imageio.imwrite is for 2D data 
                                                    #imageio.mimwrite is for 3D data (zDim, xDim, yDim)
        print('Finished Acquiring ' + imName)
    spincam.end_acquisition()

def main():

    #whatever you want to do
    
	find_and_init_cam()
	acquire_single() #IMPORTANT NOTE: when you want to save an image stack (3D) you will need to use 
                    # imageio.mimwrite(imName, stack) instead
    

if __name__ == '__main__':

    sys.exit(main())