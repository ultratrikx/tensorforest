import csv
import os
from PIL import Image

# Load the GPS coordinates and headings
gps_coordinates = {}
headings = {}
with open('gps_coordinates.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header
    for row in reader:
        filename, lat, lon, heading = row
        gps_coordinates[filename] = (float(lat), float(lon))
        headings[filename] = float(heading)

# Calculate the number of columns
num_columns = len(set(lon for lat, lon in gps_coordinates.values()))

# Create a new folder for the rotated images
rotated_folder = 'rotated_results/'
os.makedirs(rotated_folder, exist_ok=True)

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

# Rotate each image based on its heading and save it in the new folder
for filename in os.listdir('results/'):
    if filename in headings:
        img = Image.open(f'results/{filename}')
        img = img.rotate(360 - headings[filename], resample=Image.BICUBIC, expand=True)
        img = trim(img)  # Trim the image to remove black edges
        img.save(f'{rotated_folder}/{filename}')

# Sort the images in the new folder based on their GPS coordinates
sorted_filenames = sorted(os.listdir(rotated_folder), key=lambda filename: gps_coordinates.get(filename, (float('inf'), float('inf'))))

# Save the sorted filenames in a text file for the image_stitch.py script to use
with open('sorted_filenames.txt', 'w') as f:
    for filename in sorted_filenames:
        f.write(f'{filename}\n')

print(f'Number of columns: {num_columns}')