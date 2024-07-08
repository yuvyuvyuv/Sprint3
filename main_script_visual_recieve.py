# in this module i want to use a YXF-QQSJ-8807-125 camera to capture a
# screen and use a homography in order to get a qr that is on the screen, that qr
# will be decoded and the data will be used to generate a txt/jpg file

import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode
import subprocess
import os
from PIL import Image


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
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect Data Matrix barcodes in the image
    barcodes = decode(image)
    return barcodes[0] if barcodes else None


def detect_qr_code(frame):
    # Initialize the QRCode detector
    detector = cv2.QRCodeDetector()

    # Detect and decode the QR code
    data, bbox, _ = detector.detectAndDecode(frame)

    return data, bbox


def show_image(path):
    image = cv2.imread(path)
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def generate_output_file(data, frame, i):
    # lets decode the qr code
    data = data.decode("utf-8")
    txt_file_path = 'output' + str(i) + '.txt'
    with open(txt_file_path, 'w') as file:
        file.write(data)
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
            if 0.2 *w * h< area < 0.8 * w * h:  # Adjust the threshold as needed
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
        # detect wqr
        org_frame = frame
        data, bbox = detect_qr_code(frame)
        print(f"bbox: {bbox}")
        if bbox is not None:
            rec = bbox[0]
        data_matrix = None
        # check if qr code is detected
        if bbox is not None:
            # we get the corners of the qr code, lets enlarge it
            # src_points = np.array([[rec[0][0], rec[0][1]], [rec[1][0], rec[1][1]], [rec[2][0], rec[2][1]],
            #                         [rec[3][0], rec[3][1]]], dtype=np.float32)
            # # now homography to the entire video frame
            # dst_points = np.array([[0, 0], [SCREEN_WIDTH, 0], [SCREEN_WIDTH, SCREEN_HEIGHT], [0, SCREEN_HEIGHT]],
            #                        dtype=np.float32)
            # rectified_data_matrix_image = apply_homography(frame, src_points, dst_points)
            # frame = rectified_data_matrix_image
        # Step 2: Detect the Data Matrix
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            data_matrix = detect_data_matrix(pil_image)
            frame = pil_image
        if data_matrix is not None:
            # print(data_matrix, bbox)
            j += 1
            generate_output_file(data_matrix, frame, j)
            print("Data Matrix found in frame", i)
        else:
            # Data Matrix not detected, apply homography to the entire screen
            print("No Data Matrix detected in the current frame", i)

        # Display the captured frame
        cv2.imshow('Video Stream', org_frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
