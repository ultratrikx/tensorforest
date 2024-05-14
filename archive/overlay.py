import os
import csv
import simplekml

# Load the GPS coordinates
gps_coordinates = {}
with open('gps_coordinates.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header
    for row in reader:
        filename, lat, lon = row
        gps_coordinates[filename] = (float(lat), float(lon))

# Create a new KML object
kml = simplekml.Kml()

# Loop through each image and its corresponding GPS coordinates
image_folder = 'results/'
for filename in os.listdir(image_folder):
    if filename in gps_coordinates:
        lat, lon = gps_coordinates[filename]
        path = os.path.join(image_folder, filename)

        # Create a new overlay
        overlay = kml.newgroundoverlay(name=filename)
        overlay.icon.href = path
        overlay.latlonbox.north = lat + 0.001  # Adjust these values as needed
        overlay.latlonbox.south = lat - 0.001
        overlay.latlonbox.east = lon + 0.001
        overlay.latlonbox.west = lon - 0.001

        # Create a new Placemark object and assign the LookAt object to it
        placemark = kml.newpoint(name=filename)


        # Create a new LookAt object and set its properties
        lookat = simplekml.LookAt()
        lookat.longitude = lon
        lookat.latitude = lat
        lookat.altitude = 142.4866690964714  # Adjust this value as needed
        lookat.heading = 279.8065332338992  # Adjust this value as needed
        lookat.tilt = 0
        lookat.gxfovy = 35
        lookat.range = 218.0450042969824
        lookat.altitudemode = simplekml.AltitudeMode.absolute

        placemark.lookat = lookat



# Save the KML object to a file
kml.save('aimage_overlay.kml')