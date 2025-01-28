# BAR-CODE-DETECTION-AND-DECODING

## Objective 
The primary goal of this project was to develop a Python program capable of detecting 
and decoding barcodes in images using OpenCV for image preprocessing and the 
Pyzbar library for barcode decoding. The system preprocesses the input image, 
identifies potential barcode regions, and annotates the image with decoded barcode 
information. 

## Key Features 
1. Image Preprocessing 
  - The image is read and converted to grayscale to simplify subsequent 
processing. 
  - Gradients are computed using the Sobel operator to enhance edges. 
  - A difference between x-gradient and y-gradient highlights horizontal lines 
common in barcodes. 
- The result is blurred to smooth out high-frequency noise in the gradient 
representation of the image, and thresholded to obtain a binary image. 
2. Morphological Operations 
  - A rectangular kernel closing operation is applied to fill gap s between the 
vertical bars of the barcode. This kernel has a width that is larger than the 
height, thus allowing us to close the gaps between vertical stripes of the 
barcode. 
  - Erosions and dilations refine the barcode contours and remove noise. 
3. Contour Detection 
  - Contours are extracted from the preprocessed binary image to identify 
potential barcode regions. 
  - For each contour, the bounding box is determined, and the region is 
cropped for further analysis. 
4. Barcode Decoding and Annotation 
  - The cropped barcode regions are decoded using the Pyzbar library. 
  - If a barcode is successfully decoded, the detected data and type are printed 
and annotated on the original image. 
5. Visualization 
  - Detected barcodes are highlighted with green contours, and decoded 
information is displayed above the barcode. 
  - The final image is displayed using OpenCV’s imshow function.
    
## Code Workflow 
1. Preprocessing Image 
  - The `preprocess_image` function reads the image and applies gradients, 
blurring, and morphological operations to isolate barcode-like features. 
2. Barcode Detection 
  - The `detect_barcodes` function locates contours and analyzes each 
region for barcode data using Pyzbar. It also annotates the image with the 
detected barcode data. 
3. Annotation 
  - The `annotate_image` function displays the decoded data near the 
corresponding barcode region for easy identification. 
4. Execution 
  - The `main` function integrates all components, taking the input image path 
from the user, processing the image, and displaying the result. 
