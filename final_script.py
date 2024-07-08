# this is the final script that will be used to run the entire project
# it should be a hidden file on a disk on key that will run directly from the disk
# on key after clicked on when connected to a computer
import create_audio_file_from_binary
import find_data
import wav_file_stuff
import bfsk
import sounddevice as sd
from nltk.corpus import words
import nltk

Fs = 44000  # Sampling frequency (Hz)


def use_modulation(binary_data):
    print("Modulating data...")
    return bfsk.generate_bfsk_signal(binary_data, 1000, 2000, Fs, 1, 1)


def get_all_paths():
    print('Getting all paths...')
    try:
        paths_in_order2 = find_data.rank_files(find_data.list_files_in_directory())
        print('Paths obtained successfully')
        return paths_in_order2
    except Exception as e:
        print(f"Error in getting paths: {e}")
        return []


def send_accoustic_signal(path):
    '''
    This function sends an accoustic signal, starts by reading a txt file in binary, modulating it and sending it
    :param path:
    :return:
    '''
    try:
        # get the binary data from the file
        binary_data = create_audio_file_from_binary.read_file_as_binary(path)
        print(f"Binary data read from {path}")
        # modulate the data
        modulated_data = use_modulation(binary_data)
        print("Data modulated")
        # send the data
        sd.play(modulated_data, Fs)
        sd.wait()  # Wait until the audio is done playing
        print("Data sent acoustically")
        return 0
    except Exception as e:
        print(f"Error in sending acoustic signal: {e}")
        return -1


def send_accoustic_signal_from_data(modulated_data):
    '''
    This function sends an accoustic signal
    :param path:
    :return:
    '''
    try:
        sd.play(modulated_data, Fs)
        sd.wait()  # Wait until the audio is done playing
        print("Data sent acoustically from provided modulated data")
        return 0
    except Exception as e:
        print(f"Error in sending acoustic signal from data: {e}")
        return -1


if __name__ == '__main__':
    print('Starting script...')
    try:
        # Ensure nltk words are available
        nltk.download("words")
        print("NLTK words downloaded")
    except Exception as e:
        print(f"Error downloading NLTK words: {e}")

    paths_in_order = get_all_paths()
    for path in paths_in_order:
        print(f"Processing file: {path}")
        send_accoustic_signal(path)
    print("Script finished")
    exit(0)
