import cv2
import numpy as np
from pyzbar.pyzbar import decode as zbar_decode, _pixel_data
import subprocess
import os
import main_script_visual_recieve

# get hello test image

# (pixels, width, height)
if image is None:
    raise ValueError("Failed to load image")
image_format = [image, image.shape[1], image.shape[0]]
image_format = _pixel_data(image_format)
data_matrices = zbar_decode(image)
if data_matrices:
    main_script_visual_recieve.generate_output_file(data_matrices[0])