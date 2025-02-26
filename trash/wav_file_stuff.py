# this module contains functions for playing and saving wav files, and for reading files as binary data, etc
import numpy as np
import wave
import struct
import pyaudio # for playing the wav file


# TODO: update locations!!

# WANTED_LOCATION = "C:\\Users\\Public\\Documents\\top_secret"
LOCATION_FOR_CHECK = "Sprint3"
FILE_NAME = "../data_for_checks/check_hadar.txt"
WAV_FILE_NAME = "check_hadar.wav"
WAV_FILE_NAME2 = "check_hadar.wav"
WAV_FILE_PATH = f"{LOCATION_FOR_CHECK}\\{WAV_FILE_NAME}"
WAV_FILE_PATH2 = f"{LOCATION_FOR_CHECK}\\{WAV_FILE_NAME2}"


def create_wav_file(data):
    # TODO: update function and check if works
    '''
    This function creates a wav file
    :param data:
    :return: path of the wav file
    '''
    # create a wave file
    wave_file = wave.open(WAV_FILE_PATH, 'w')
    # set the parameters
    wave_file.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
    # write the data
    wave_file.writeframes(data)
    # close the file
    wave_file.close()
    return WAV_FILE_PATH


def create_wav_file_img(data):
    # TODO: update function and check if works
    '''
    This function creates a wav file
    :param data:
    :return: path of the wav file
    '''
    # create a wave file
    wave_file = wave.open(WAV_FILE_PATH, 'w')
    # set the parameters
    wave_file.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
    # write the data
    wave_file.writeframes(data)
    # close the file
    wave_file.close()
    return WAV_FILE_PATH


def play_wav_file(wav_file_path):
    '''
    This function plays a wav file
    :param wav_file_path:
    :return: nothing
    '''
    # open the file
    wave_file = wave.open(wav_file_path, 'r')
    # read the frames
    frames = wave_file.readframes(-1)
    # get the parameters
    params = wave_file.getparams()
    # close the file
    wave_file.close()
    # play the file
    play_obj = pyaudio.PyAudio().open(format=pyaudio.PyAudio().get_format_from_width(params[1]),
                                        channels=params[0],
                                        rate=params[2],
                                        output=True)
    play_obj.write(frames)
    play_obj.stop_stream()
    play_obj.close()
    return
