import qrcode
from pylibdmtx.pylibdmtx import encode
from PIL import Image
import binascii

def generate_data_matrix(input_file, output_file):
    with open(input_file, 'rb') as file:
        binary_data = file.read()
    binary_data = binascii.hexlify(binary_data).decode('utf-8')
    encoded = encode(binary_data)
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    img.save(output_file)
    return output_file


def generate_qr_code(input_file, output_file):
    # Read binary data from file
    with open(input_file, 'rb') as file:
        binary_data = file.read()
    binary_data = binascii.hexlify(binary_data).decode('utf-8')

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(binary_data)
    qr.make(fit=True)

    # Create QR code image
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Save QR code image to file
    qr_image.save(output_file)

    return output_file

if __name__ == "__main__":
    input_file = "yuval_test.txt"  # Replace with your binary file path
    output_file = input_file[:-3]+"png"  # Output QR code file name

    generate_qr_code(input_file, output_file)
