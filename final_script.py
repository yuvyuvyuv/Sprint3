# this is the final script that will be used to run the entire project
# it should be a hidden file on a disk on key that will run directly from the disk on key after clicked on when connected to a computer
import create_audio_file_from_binary
import find_data
import wav_file_stuff
import find_data


def use_modulation(binary_data):
    print('penis')
    # TODO: use yogev function here

def get_all_paths():
    paths_in_order = find_data.rank_files(find_data.list_files_in_directory())
    # TODO: add eithen's function here
    return paths_in_order


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
    wav_file_path = wav_file_stuff.create_wav_file(modulated_data)
    # now run the wav file:
    wav_file_stuff.play_wav_file(wav_file_path)



if __name__ == '__main__':
    paths_in_order = get_all_paths()
    for path in paths_in_order:
        send_accoustic_signal(path)
