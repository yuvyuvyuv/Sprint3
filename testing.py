import cv2
import numpy as np


# def detect_qr_code(frame):
#     # Initialize the QRCode detector
#     detector = cv2.QRCodeDetector()
#
#     # Detect and decode the QR code
#     data, bbox, _ = detector.detectAndDecode(frame)
#
#     # Print debug information
#     print(f"Data: {data}")
#     print(f"Bounding Box: {bbox}")
#
#     return data, bbox


def main():
    # Open a connection to the camera
    cap = cv2.VideoCapture(1)  # 0 for the default camera

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect QR codes in the frame
        data, bbox = detect_qr_code(frame)

        # If a QR code is detected
        if bbox is not None and data:
            # Draw bounding box around the QR code
            bbox = np.int32(bbox)
            for i in range(len(bbox[0])):
                cv2.line(frame, tuple(bbox[0][i]), tuple(bbox[0][(i + 1) % len(bbox[0])]), color=(0, 255, 0),
                         thickness=2)
            # Display the decoded data
            cv2.putText(frame, data, (bbox[0][0][0], bbox[0][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # Print the decoded data to the console
            print("QR Code Data:", data)

        # Display the resulting frame
        cv2.imshow('Frame', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release everything when the job is finished
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
