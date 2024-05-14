image_stictch.pyfrom PIL import Image
import os

# Load all the images
image_folder = 'rotated_results/'
image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
images = [Image.open(os.path.join(image_folder, f)) for f in image_files]

# Sort the images based on GPS coordinates
# This step will depend on how your GPS coordinates are stored and associated with each image
# For the sake of this example, we'll assume that the images are already sorted in the correct order

# Create a new blank image
# We'll assume that all images are the same size and that they form a grid with a fixed number of columns
image_size = images[0].size
num_images = len(images)
num_columns = 3  # Change this to the number of columns you want
num_rows = num_images // num_columns + (num_images % num_columns != 0)
stitched_image = Image.new('RGB', (image_size[0] * num_columns, image_size[1] * num_rows))

# Paste each image into the correct position
for i, img in enumerate(images):
    x = i % num_columns
    y = i // num_columns
    stitched_image.paste(img, (x * image_size[0], y * image_size[1]))

# Save the stitched image
stitched_image.save('stitched_image.jpg')