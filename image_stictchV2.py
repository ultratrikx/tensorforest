import cv2
import numpy as np
import os

# Load the images
image_folder = 'images/'
image_files = sorted([f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))])  # Sort the filenames alphabetically
images = [cv2.imread(os.path.join(image_folder, f)) for f in image_files]

# Check if all images are loaded correctly
for i, img in enumerate(images):
    if img is None:
        print(f"Image {image_files[i]} could not be loaded")
        exit(1)

# Initialize the stitcher
stitcher = cv2.Stitcher_create()

# Stitch the images together
status, stitched_image = stitcher.stitch(images)

# Check if the stitching was successful
if status == cv2.Stitcher_OK:
    # Save the stitched image
    cv2.imwrite('stitched_image.jpg', stitched_image)
else:
    print('Error during stitching, status code =', status)