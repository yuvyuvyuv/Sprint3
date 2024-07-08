# in this module i want to use a YXF-QQSJ-8807-125 camera to capture a
# screen and use a homography in order to get a qr that is on the screen, that qr
# will be decoded and the data will be used to generate a txt/jpg file

import cv2
import numpy as np
from pyzbar.pyzbar import decode as zbar_decode
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
    data_matrices = zbar_decode(image)
    if data_matrices:
        return data_matrices[0]  # Return the first detected Data Matrix
    return None


def show_image(path):
    image = cv2.imread(path)
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def generate_output_file(data, image):
    if data.endswith('.txt'):
        with open('output.txt', 'w') as file:
            file.write(data)
        print("TXT file generated")
        # now output it to the screen
        file_path = 'output.txt'
        open_in_notepad(file_path)
    elif data.endswith('.jpg'):
        cv2.imwrite('output.jpg', image)
        print("JPG file generated")
        show_image('output.jpg')
    else:
        print("Unknown data format")

    return


def main():
    camera = cv2.VideoCapture(1)  # Replace 0 with the appropriate camera index if necessary

    while True:
        # Step 1: Capture a frame from the camera
        frame = capture_frame(camera)

        # Step 2: Detect the Data Matrix
        data_matrix = detect_data_matrix(frame)

        if data_matrix:
            # Data Matrix detected
            points = data_matrix.polygon
            if len(points) == 4:
                src_points = np.array([
                    [points[0].x, points[0].y],
                    [points[1].x, points[1].y],
                    [points[2].x, points[2].y],
                    [points[3].x, points[3].y]
                ], dtype=np.float32)

                # Calculate width and height of the Data Matrix
                width = int(
                    max(np.linalg.norm(src_points[0] - src_points[1]), np.linalg.norm(src_points[2] - src_points[3])))
                height = int(
                    max(np.linalg.norm(src_points[0] - src_points[3]), np.linalg.norm(src_points[1] - src_points[2])))

                dst_points = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)

                # Step 3: Apply homography to the Data Matrix
                rectified_data_matrix_image = apply_homography(frame, src_points, dst_points)

                # Step 4: Decode the Data Matrix from the rectified image
                decoded_data_matrix = detect_data_matrix(rectified_data_matrix_image)
                if decoded_data_matrix:
                    data = decoded_data_matrix.data.decode('utf-8')
                    # Step 5: Generate output file
                    generate_output_file(data, rectified_data_matrix_image)
                else:
                    print("Failed to decode the Data Matrix from the rectified image")
        else:
            # Data Matrix not detected, apply homography to the entire screen
            print("No Data Matrix detected in the current frame")

        # Display the captured frame
        cv2.imshow('Video Stream', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
