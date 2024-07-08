import qrcode
from pylibdmtx.pylibdmtx import encode
from PIL import Image
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

def scale_image(image_path, scale_factor):
    # Open an image file
    image = Image.open(image_path)
    # Calculate the new size
    new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
    # Resize the image
    resized_image = image.resize(new_size)
    return resized_image


def add_red_frame(image, frame_width=10):
    # Calculate the size of the new image with the frame
    new_width = image.width + 2 * frame_width
    new_height = image.height + 2 * frame_width

    # Create a new image with a red background
    framed_image = Image.new("RGB", (new_width, new_height), "red")

    # Paste the original image onto the center of the new image
    framed_image.paste(image, (frame_width, frame_width))

    return framed_image


def draw_img(image_path, duration_ms, x, y, frame_width=10):
    # Load the image using PIL
    image = scale_image(image_path, 3)

    # Add a red frame around the image
    framed_image = add_red_frame(image, frame_width)

    # Create a Tkinter window
    window = tk.Tk()
    window.attributes("-topmost", True)
    window.attributes("-fullscreen", True)
    window.title("Image Display")

    # Convert the framed image to a format Tkinter can use
    tk_image = ImageTk.PhotoImage(framed_image)

    # Set window size and position
    window.geometry(f"{framed_image.width}x{framed_image.height}+{x}+{y}")

    # Create a label to hold the image
    label = tk.Label(window, image=tk_image)
    label.image = tk_image  # Keep a reference to the image
    label.pack()

    # Define a function to close the window
    def close_window():
        window.destroy()

    # Schedule the window to close after duration_ms milliseconds
    window.after(duration_ms, close_window)

    # Start the Tkinter main loop
    window.mainloop()

def generate_data_matrix_from_text(binary_data, output_file):
    text_data = binary_data.encode('utf-8')
    encoded = encode(text_data)
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    img.save(output_file)
    draw_img(output_file, 6000, 0, 0)
    return output_file

def generate_data_matrix(input_file, output_file):
    with open(input_file, 'rb') as file:
        binary_data = file.read()
    encoded = encode(binary_data)
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    img.save(output_file)
    return output_file


def generate_qr_code(input_file, output_file):
    # Read binary data from file
    with open(input_file, 'rb') as file:
        binary_data = file.read()
    print("binary data type is "+str(type(binary_data)))
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


def generate_qr_data_from_text(binary_data, output_file):

    text_data = binary_data.encode('utf-8')
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(text_data)
    qr.make(fit=True)

    # Create QR code image
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Save QR code image to file
    qr_image.save(output_file)

    draw_img(output_file, 2000, 0, 0)

    print(f"QR code saved as {output_file}")
    return output_file




if __name__ == "__main__":
    input_file = "data_for_checks\check_hadar.txt"  # Replace with your binary file path
    output_file = input_file[:-3]+"png"  # Output QR code file name

    generate_data_matrix(input_file, output_file)
