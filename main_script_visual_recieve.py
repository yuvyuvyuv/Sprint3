# in this module i want to use a YXF-QQSJ-8807-125 camera to capture a
# screen and use a homography in order to get a qr that is on the screen, that qr
# will be decoded and the data will be used to generate a txt/jpg file

import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode
import subprocess
import os

# TODO: find actual resolution
SCREEN_WIDTH = 1920  # Replace with actual screen width
SCREEN_HEIGHT = 1080  # Replace with actual screen height


def open_in_notepad(file_path):
    if os.path.exists(file_path):
        subprocess.run(['notepad.exe', file_path])
    else:
        print(f"The file {file_path} does not exist")


def capture_frame(camera):
    ret, frame = camera.read()
    if not ret:
        raise ValueError("Failed to capture frame")
    return frame


def apply_homography(image, src_points, dst_points):
    homography_matrix, _ = cv2.findHomography(src_points, dst_points)
    height, width = image.shape[:2]
    rectified_image = cv2.warpPerspective(image, homography_matrix, (width, height))
    return rectified_image


def detect_data_matrix(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect Data Matrix barcodes in the image
    barcodes = decode(gray_image)
    return barcodes[0] if barcodes else None


def show_image(path):
    image = cv2.imread(path)
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def generate_output_file(barcode, image, i):
    # Extract the bounding box location of the barcode and draw a rectangle around it
    # (x, y, w, h) = barcode.rect.left, barcode.rect.top, barcode.rect.width, barcode.rect.height
    # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # The barcode data is a bytes object so if we want to draw it on our output image
    # we need to convert it to a string first
    barcode_data = barcode.data.decode("utf-8")
    # now to create the file
    # create a txt file
    txt_file_path = 'output' + str(i) + '.txt'
    with open(txt_file_path, 'w') as file:
        file.write(barcode_data)
    # create a jpg file
    open_in_notepad(txt_file_path)
# Save the output image with annotations
#     output_path = "output.jpg"
#     cv2.imwrite(output_path, image)
#     show_image(output_path)


def detect_red_hollow_rectangles(frame):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of red color in HSV
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # Create a mask for red color
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_rectangles = []

    for cnt in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Check if the approximated contour has 4 vertices (a rectangle)
        if len(approx) == 4:
            area = cv2.contourArea(cnt)
            # Check if the rectangle is hollow by comparing the area with the bounding box area
            x, y, w, h = cv2.boundingRect(cnt)
            if area < 0.8 * w * h:  # Adjust the threshold as needed
                detected_rectangles.append(approx)

    return detected_rectangles


def main():
    i =0
    camera = cv2.VideoCapture(1)  # Replace 0 with the appropriate camera index if necessary
    j=0
    while True:
        i += 1
        # Step 1: Capture a frame from the camera
        frame = capture_frame(camera)

        recs = detect_red_hollow_rectangles(frame)
        if recs:
            print("Rectangle found in frame", i)
            for rec in recs:
                # 4 points of the rectangle
                src_points = np.array([
                    [rec[0][0][0], rec[0][0][1]],
                    [rec[1][0][0], rec[1][0][1]],
                    [rec[2][0][0], rec[2][0][1]],
                    [rec[3][0][0], rec[3][0][1]]
                ], dtype=np.float32)
                # now homography to the entire video frame
                dst_points = np.array([[0, 0], [SCREEN_WIDTH, 0], [SCREEN_WIDTH, SCREEN_HEIGHT], [0, SCREEN_HEIGHT]],
                                       dtype=np.float32)
                rectified_data_matrix_image = apply_homography(frame, src_points, dst_points)
                frame = rectified_data_matrix_image
        # Step 2: Detect the Data Matrix
        data_matrix = detect_data_matrix(frame)

        if data_matrix:
            j += 1
            generate_output_file(data_matrix, frame, j)
            print("Data Matrix found in frame", i)
        else:
            # Data Matrix not detected, apply homography to the entire screen
            print("No Data Matrix detected in the current frame", i)

        # Display the captured frame
        cv2.imshow('Video Stream', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
