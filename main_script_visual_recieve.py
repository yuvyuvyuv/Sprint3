# in this module i want to use a YXF-QQSJ-8807-125 camera to capture a
# screen and use a homography in order to get a qr that is on the screen, that qr
# will be decoded and the data will be used to generate a txt/jpg file
import cv2
import numpy as np
from pyzbar.pyzbar import decode

# TODO: find actual resolution
SCREEN_WIDTH = 1920  # Replace with actual screen width
SCREEN_HEIGHT = 1080  # Replace with actual screen height


def capture_image():
    camera = cv2.VideoCapture(0)  # Replace 0 with the appropriate camera index if necessary
    ret, frame = camera.read()
    camera.release()
    if not ret:
        raise ValueError("Failed to capture image")
    return frame


def apply_homography(image, src_points, dst_points):
    homography_matrix, _ = cv2.findHomography(src_points, dst_points)
    height, width = image.shape[:2]
    rectified_image = cv2.warpPerspective(image, homography_matrix, (width, height))
    return rectified_image


def detect_qr_code(image):
    qr_codes = decode(image)
    if qr_codes:
        return qr_codes[0]  # Return the first detected QR code
    return None


def show_output_file(type):
    # TODO: show output file!!
    pass


def generate_output_file(qr_data, image):
    # TODO: depends on yubar's way of encoding!!!
    type = -1
    if qr_data.endswith('.txt'):
        with open('output.txt', 'w') as file:
            file.write(qr_data)
        print("TXT file generated")
        type = 0 # txt
    elif qr_data.endswith('.jpg'):
        cv2.imwrite('output.jpg', image)
        print("JPG file generated")
        type = 1 # jpg
    else:
        print("Unknown data format")
    show_output_file(type)
    return



def detect_screen_points():
    # TODO: need to do automatically
    print("Please click on the four corners of the screen in the following order:")
    print("Top-left, Top-right, Bottom-right, Bottom-left")
    # get from user
    p1 = tuple(map(int, input("Top-left: ").split(',')))
    p2 = tuple(map(int, input("Top-right: ").split(',')))
    p3 = tuple(map(int, input("Bottom-right: ").split(',')))
    p4 = tuple(map(int, input("Bottom-left: ").split(',')))
    return p1, p2, p3, p4


def main():
    # Step 1: Capture the image from the camera
    frame = capture_image()

    # Step 2: Detect the QR code
    qr_code = detect_qr_code(frame)

    if qr_code:
        # QR code detected
        points = qr_code.polygon
        if len(points) == 4:
            src_points = np.array([(p.x, p.y) for p in points], dtype=np.float32)

            # Calculate width and height of the QR code
            width = int(
                max(np.linalg.norm(src_points[0] - src_points[1]), np.linalg.norm(src_points[2] - src_points[3])))
            height = int(
                max(np.linalg.norm(src_points[0] - src_points[3]), np.linalg.norm(src_points[1] - src_points[2])))

            dst_points = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)

            # Step 3: Apply homography to the QR code
            rectified_qr_image = apply_homography(frame, src_points, dst_points)

            # Step 4: Decode the QR code from the rectified image
            decoded_qr_code = detect_qr_code(rectified_qr_image)
            if decoded_qr_code:
                qr_data = decoded_qr_code.data.decode('utf-8')
                # Step 5: Generate output file
                generate_output_file(qr_data, rectified_qr_image)
            else:
                print("Failed to decode the QR code from the rectified image")
        else:
            print("QR code is not a quadrilateral")
    else:
        # QR code not detected, apply homography to the entire screen
        print("No QR code detected, applying homography to the screen")
        p1, p2, p3, p4 = detect_screen_points()
        screen_points = np.array([p1,p2, p3, p4],
                                 dtype=np.float32)  # Replace with actual screen coordinates
        screen_width = SCREEN_WIDTH  # Replace with actual screen width
        screen_height = SCREEN_HEIGHT  # Replace with actual screen height
        screen_dst_points = np.array([[0, 0], [screen_width, 0], [screen_width, screen_height], [0, screen_height]],
                                     dtype=np.float32)

        rectified_screen_image = apply_homography(frame, screen_points, screen_dst_points)

        # Optionally display the rectified screen image
        cv2.imshow('Rectified Screen Image', rectified_screen_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
