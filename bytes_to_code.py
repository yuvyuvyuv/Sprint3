import qrcode

def generate_qr_code(input_file, output_file):
    # Read binary data from file
    with open(input_file, 'rb') as file:
        binary_data = file.read()

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

    print(f"QR code saved as {output_file}")
    return output_file

if __name__ == "__main__":
    input_file = "data_for_checks\check_hadar.txt"  # Replace with your binary file path
    output_file = "qr_code.png"  # Output QR code file name

    generate_qr_code(input_file, output_file)
