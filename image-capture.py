# Import necessary libraries
from picamera2 import Picamera2, Preview
from libcamera import controls
import time
from time import sleep
import os

# Initialize the camera
picam2 = Picamera2()

# Create a configuration for the camera preview
camera_config = picam2.create_preview_configuration()

# Ask the user for the duration of the timelapse in minutes
duration = input("Enter the duration of the timelapse in minutes: ")
# Ask the user for the interval between each image capture in seconds
interval = input("Enter the interval in which images are taken in seconds: ")
# Ask the user if they want to enable live preview
preview = input("Enable live preview? (0 for no, 1 for yes): ")
# Ask the user for the path to the folder where the images will be saved
path = input("Enter path to save folder: ")

# If the provided duration is not a valid number, set it to a default value of 10 minutes
if duration.isdigit() is False:
    duration = 10 * 60
else:
    duration = int(duration) * 60

# If the provided interval is not a valid number, set it to a default value of 5 seconds
if interval.isdigit() is False:
    interval = 5
else:
    interval = int(interval)

# If the provided preview option is not a valid number, set it to a default value of 0 (no preview)
if preview.isdigit() is False:
    preview = 0
else:
    preview = int(preview)

# If the provided path does not exist, ask the user if they want to use a default path
if os.path.exists(path) is False:
    error = int(input("Path does not exist, do you want to use default path? 0 for no, 1 for yes: "))
    if error == 1:
        path = "/home/pi/Documents/image_capture/images"
    else:
        quit()

# Configure the camera with the created configuration
picam2.configure(camera_config)
# If the user chose to enable live preview, start the preview
if preview == 1:
    picam2.start_preview(Preview.QTGL)
# Start the camera
picam2.start()

# Calculate the end time of the timelapse
end = time.time() + duration
# Calculate the total number of images that will be captured
total_image_count = duration // interval
# Initialize a counter for the number of images taken
images_taken = 0
# Record the start time of the timelapse
start_time = time.time()

# Loop until all images have been captured
while images_taken < total_image_count:
    # Create a label for the current date and time
    date_label = (time.strftime("%y-%m-%d_%H:%M:%S"))
    # Capture an image
    r = picam2.capture_request()
    # Save the image with the date label in the filename
    r.save("main", f"{path}/{date_label}.png")
    # Release the capture request
    r.release()
    # Increment the counter for the number of images taken
    images_taken += 1
    # Print the number of images taken and the time elapsed
    print(f"Captured image {images_taken} of {total_image_count} at {time.time() - start_time:.2f}s")
    # Wait for the specified interval before capturing the next image
    time.sleep(interval - 0.0255)

# Print a message indicating that all images have been captured
print("Captured all images.")

# Stop the camera
picam2.stop()