# in this module i want to find a greyscale image, and convert it to a binary data format we can
# accoustically send and receive

# this module will contain functions for finding a greyscale image, and converting it to binary data
import os
import numpy as np
import cv2
import wave
import struct
import pyaudio  # for playing the wav file
import wav_file_stuff
import final_script

PATH = "C:\\Users\\Public\\Documents\\top_secret\\top_image.jpg"


def get_image():
    '''
    This function gets an image from a path
    :return: image
    '''
    return cv2.imread(PATH, cv2.IMREAD_GRAYSCALE)


def modulation(binary_data):
    # TODO: add modulation function from yubaum
    '''
    This function modulates the binary data
    :param binary_data:
    :return: modulated data
    '''
    return binary_data


def define_metadata(image):
    '''
    This function defines the metadata of the image
    :param image:
    :return: metadata
    '''
    return image.shape


def convert_image_to_binary(image):
    '''
    This function converts an image to binary data
    :param image:
    :return: binary data
    '''
    return image.tobytes()

if __name__ == "__main__":
    img = get_image()
    metadata = define_metadata(img)
    binary_data = convert_image_to_binary(img)
    modulated_data = modulation(binary_data)
    # wav_file_path = wav_file_stuff.create_wav_file_img(modulated_data)
    # final_script.send_accoustic_signal(wav_file_path)
    final_script.send_accoustic_signal_from_data(modulated_data)




