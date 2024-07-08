import numpy as np
import wave
import struct

# WANTED_LOCATION = "C:\\Users\\Public\\Documents\\top_secret"
LOCATION_FOR_CHECK = "Sprint3"
FILE_NAME = "check_hadar.txt"
WAV_FILE_NAME = "check_hadar.wav"
WAV_FILE_PATH = f"{LOCATION_FOR_CHECK}\\{WAV_FILE_NAME}"

# in this file, we have a txt file, we will read it as binary and create a wav file from it
# the wav file will be modulated according to another file


# reading the txt file as binary
def read_file_as_binary(file_path):
    with open(file_path, "rb") as file:
        return file.read()
