from pydub import AudioSegment
import sys
import os
import pygame

def play_wav(wav_path):
    # Check if the input file exists
    if not os.path.isfile(wav_path):
        print(f"File not found: {wav_path}")
        return

    try:
        # Initialize pygame mixer
        pygame.mixer.init()
        # Load the wav file
        pygame.mixer.music.load(wav_path)
        # Play the wav file
        pygame.mixer.music.play()
        print(f"Playing: {wav_path}")

        # Keep the script running until the audio is finished
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        print(f"Finished playing: {wav_path}")
    except Exception as e:
        print(f"An error occurred while playing the file: {e}")

def convert_m4a_to_wav(m4a_path):
    # Check if the input file exists
    if not os.path.isfile(m4a_path):
        print(f"File not found: {m4a_path}")
        return None

    # Define the output path for the wav file
    wav_path = os.path.splitext(m4a_path)[0] + ".wav"

    # Load the m4a file
    try:
        audio = AudioSegment.from_file(m4a_path, format="m4a")
        # Export the file as wav
        audio.export(wav_path, format="wav")
        print(f"File successfully converted to: {wav_path}")
        return wav_path
    except Exception as e:
        print(f"An error occurred while converting the file: {e}")
        return None

if __name__ == "__main__":
    path_to_audio = input("Enter the path to the audio file: ").strip('"')
    wav_path = convert_m4a_to_wav(path_to_audio)
    if wav_path:
        play_wav(wav_path)
