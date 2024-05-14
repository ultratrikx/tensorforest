from PIL import Image
import csv
import os

# Load the GPS coordinates and find the max boundaries
gps_coordinates = {}
headings = {}
max_lat = max_lon = float('-inf')
min_lat = min_lon = float('inf')
with open('gps_coordinates.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header
    for row in reader:
        filename, lat, lon, heading = row
        lat = float(lat)
        lon = float(lon)
        gps_coordinates[filename] = (lat, lon)
        headings[filename] = float(heading)
        max_lat = max(max_lat, lat)
        min_lat = min(min_lat, lat)
        max_lon = max(max_lon, lon)
        min_lon = min(min_lon, lon)

# Calculate the size of the canvas
canvas_width = int((max_lon - min_lon + 0.0001) * 10000)  # Increase the factor to create a larger canvas
canvas_height = int((max_lat - min_lat + 0.0001) * 10000)  # Increase the factor to create a larger canvas

# Create a blank canvas
canvas = Image.new('RGB', (canvas_width, canvas_height))

# Loop through each image, its corresponding GPS coordinates, and its heading
image_folder = 'results/'
image_files = [filename for filename in os.listdir(image_folder) if filename in gps_coordinates]

image_added = False  # Flag to check if at least one image is added
for i, filename in enumerate(image_files):
    lat, lon = gps_coordinates[filename]
    heading = headings[filename]

    # Calculate the position of the image on the canvas
    x = int((lon - min_lon) * 10000) + i  # Add an offset to the x-coordinate
    y = int((max_lat - lat) * 10000) + i  # Add an offset to the y-coordinate

    # Open the image file
    img = Image.open(os.path.join(image_folder, filename))

    # Rotate the image based on its heading to be north
    img = img.rotate(360 - heading, resample=Image.LANCZOS, expand=True)

    # Check if the image exceeds the canvas boundaries after rotation
    if x + img.width > canvas_width or y + img.height > canvas_height:
        # Increase the size of the canvas to accommodate the image
        canvas_width = max(canvas_width, x + img.width)
        canvas_height = max(canvas_height, y + img.height)
        canvas = canvas.resize((canvas_width, canvas_height), Image.LANCZOS)

    # Paste the image into the correct position on the canvas
    canvas.paste(img, (x, y))
    image_added = True

# Save the canvas if at least one image is added
if image_added:
    canvas.save('canvas.jpeg')
else:
    print("No images were added to the canvas.")