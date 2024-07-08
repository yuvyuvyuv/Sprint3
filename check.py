import cv2

import main_script_visual_recieve

def detect_and_decode_datamatrix(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect Data Matrix barcodes in the image
    barcodes = decode(gray_image)

    results = []
    for barcode in barcodes:
        # Extract the bounding box location of the barcode and draw a rectangle around it
        (x, y, w, h) = barcode.rect.left, barcode.rect.top, barcode.rect.width, barcode.rect.height
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # The barcode data is a bytes object so if we want to draw it on our output image
        # we need to convert it to a string first
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = "DataMatrix"

        # Draw the barcode data and barcode type on the image
        text = f"{barcode_data} ({barcode_type})"
        cv2.putText(image, text, (x, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Collect the barcode type and data
        results.append((barcode_type, barcode_data))

    # Save the output image with annotations
    output_path = "data/hadar_text_test_annotated.png"
    cv2.imwrite(output_path, image)
    # main_script_visual_recieve.generate_output_file()
    return results, output_path

# Example usage
image_path = "data/hadar_text_test.png"
detect_and_decode_datamatrix(image_path)
