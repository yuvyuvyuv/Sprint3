import find_data
import nltk
import qrcode
import binascii

def convert_to_qr(binary_data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(binary_data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    return qr_image


def get_all_paths():
    print('Getting all paths...')
    try:
        paths_in_order2 = find_data.rank_files(find_data.list_files_in_directory())
        print('Paths obtained successfully')
        return paths_in_order2
    except Exception as e:
        print(f"Error in getting paths: {e}")
        return []


def show_qr(qr_code):
    print("Showing QR code...")
    #  TODO: use hertz code to show

    return 0


def read_file_as_binary(file_path):
    '''
    This function reads a file as binary
    :param file_path:
    :return:  binary data
    '''
    print(f"Reading file as hex: {file_path}")
    with open(file_path[0], "rb") as file:
        return file.read()


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
        data = read_file_as_binary(path)
        qr_code = convert_to_qr(data)
        show_qr(qr_code)
        print(f"QR code for {path} shown")