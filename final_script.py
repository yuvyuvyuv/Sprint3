# this is the final script that will be used to run the entire project
# it should be a hidden file on a disk on key that will run directly from the disk on key after clicked on when connected to a computer
import create_audio_file_from_binary
import find_data
import wav_file_stuff
import find_data
import bfsk
import sounddevice as sd
from nltk.corpus import words

Fs = 44000  # Sampling frequency (Hz)


def use_modulation(binary_data):
    return bfsk.generate_bfsk_signal(binary_data, 1000, 2000, Fs, 1, 1)


def get_all_paths():
    print('penis0')
    paths_in_order2 = find_data.rank_files(find_data.list_files_in_directory())
    print('penis1')
    return paths_in_order2


def send_accoustic_signal(path):
    '''
    This function sends an accoustic signal, starts by reading a txt file in binary, modulating it and sending it
    :param path:
    :return:
    '''
    # get the binary data from the file
    binary_data = create_audio_file_from_binary.read_file_as_binary(path)
    # modulate the data
    modulated_data = use_modulation(binary_data)
    # send the data
    sd.play(modulated_data, Fs)
    '''wav_file_path = wav_file_stuff.create_wav_file(modulated_data)
    # now run the wav file:
    # wav_file_stuff.play_wav_file(wav_file_path)'''


def send_accoustic_signal_from_data(modulated_data):
    '''
    This function sends an accoustic signal
    :param path:
    :return:
    '''
    sd.play(modulated_data, Fs)
    '''wav_file_path = wav_file_stuff.create_wav_file(modulated_data)
    # now run the wav file:
    # wav_file_stuff.play_wav_file(wav_file_path)'''


if __name__ == '__main__':
    print('penis000')
    # TODO: uncomment
    # nltk.download("words")
    paths_in_order = get_all_paths()
    for path in paths_in_order:
        print(1)
        send_accoustic_signal(path)
