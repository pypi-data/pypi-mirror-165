'''
stemdiff.io
-----------
Input/output functions for package ediff.    
'''

import numpy as np
from PIL import Image

def read_image(image_name, itype='8bit'):
    '''
    Read grayscale image into 2D numpy array.
    
    Parameters
    ----------
    image_name : string or pathlib object
        Name of image that should read into numpy 2D array.
    itype: string ('8bit'  or '16bit')
        type of the image: 8 or 16 bit grayscale    
        
    Returns
    -------
    2D numpy array
    '''
    img = Image.open(image_name)
    if itype=='8bit':
        arr = np.asarray(img, dtype=np.uint8)
    else:
        arr = np.asarray(img, dtype=np.uint16)
    return(arr)
