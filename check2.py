import cv2

def main():
    # Open a connection to the camera
    cap = cv2.VideoCapture(1)  # 0 for the default camera

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('data/output5.avi', fourcc, 20.0, (640, 480))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Write the frame to the output video file
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('Frame', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release everything when the job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
