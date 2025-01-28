import cv2
import numpy as np
from pyzbar.pyzbar import decode

def preprocess_image(image_path):
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Compute gradient
    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(grad_x, grad_y)
    gradient = cv2.convertScaleAbs(gradient)

    # blur and threshold the image
    blurred = cv2.blur(gradient, (9, 9))

    _, binary = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY)
    
    # construct a closing kernel and apply it to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # perform a series of erosions and dilations
    closed_eroded = cv2.erode(closed, None, iterations = 8)
    closed_dilate = cv2.dilate(closed_eroded, None, iterations = 8)
    return image, closed_dilate

def detect_barcodes(image, preprocessed_image):
    # find the contours in the thresholded image
    (contours, _) = cv2.findContours(preprocessed_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        print("Barcodes detected:")
        for contour in contours:
            # Get bounding box for each contour
            rect = cv2.minAreaRect(contour)
            box = np.int0(cv2.boxPoints(rect))
            cv2.drawContours(image, [box], -1, (0, 255, 0), 1)

            # Crop the barcode region
            x, y, w, h = cv2.boundingRect(contour)
            barcode_roi = image[y:y+h, x:x+w]

            # Decode the barcode
            decoded_objects = decode(barcode_roi)
            if decoded_objects:
                for obj in decoded_objects:
                    barcode_data = obj.data.decode('utf-8')  # Decode bytes to string
                    barcode_type = obj.type
                    print(f"Type: {barcode_type}, Data: {barcode_data}")

                # Annotate the barcode with the decoded data
                annotate_image(image, barcode_data, x, y, w, h)
                
            else:
                print("No barcode detected in this region.")
    else:
        print("No contours found.")
        return image
    return image

def annotate_image(image, text, x, y, w, h):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_color = (0, 0, 255)
    thickness = 2
    line_type = cv2.LINE_AA

    # Calculate the position to place the text above the barcode
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = x + (w - text_size[0]) // 2 
    text_y = y - 10

    # Put the text above the barcode
    cv2.putText(image, text, (text_x, text_y), font, font_scale, font_color, thickness, line_type)

def main():
    # Input the image path from the user
    image_path = input("Enter the image path: ")

    # Preprocess the image
    image, processed_image = preprocess_image(image_path)

    # Detect and annotate barcodes
    image_with_barcodes = detect_barcodes(image, processed_image)

    # Display the image with detected barcodes
    cv2.imshow("Detected Barcodes", image_with_barcodes)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()