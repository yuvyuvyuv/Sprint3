import win32gui
import win32api
import time
from PIL import Image

import bytes_to_code


def draw_image(dc, x, y, image_path):
    print(image_path)
    image = Image.open(image_path)
    width, height = image.size

    for j in range(height):
        for i in range(width):
            r, g, b = image.getpixel((i, j))
            color = win32api.RGB(r, g, b)
            win32gui.SetPixel(dc, x + i, y + j, color)

# Get the device context for the entire screen
dc = win32gui.GetDC(0)

# Define the top-left corner of the image
x, y = 0, 0  # Top-left corner coordinates

# Path to the image file

image_path = bytes_to_code.generate_qr_code("data_for_checks\check_hadar.txt", "qr_code.png")

try:
    while True:
        # Draw the image
        draw_image(dc, x, y, image_path)
        time.sleep(0.001)
        # Erase the image by drawing it in black (assuming the background is black)
        draw_image(dc, x, y, 'path_to_black_image_file.png')  # Path to a black image of the same size
        time.sleep(0.001)
finally:
    # Release the device context
    win32gui.ReleaseDC(0, dc)
