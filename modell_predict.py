# Import the necessary libraries
from ultralytics import YOLO
import os
import time

# Load the YOLO model from the specified .tflite file
model = YOLO('/home/pi/Documents/tensor_forest/best_full_integer_quant_edgetpu.tflite')

# Specify the directory where the images are stored
directory = '/home/pi/Documents/tensor_forest/testv2'

# Iterate over the files in the specified directory
for filename in os.listdir(directory):
    # Record the start time of the image processing
    image_time = time.time()

    # Construct the full file path
    f = os.path.join(directory, filename)

    # Check if the file is an image file (.jpg or .png)
    if os.path.isfile(f) and filename.find("jpg" or "png") > 0:

        # Run the object detection model on the image
        result = model.predict(f"{directory}/{filename}", save=True, save_conf=True, save_txt=True, conf=0.2, iou=0.6,
                               project="results 1", name="results", exist_ok=True)

        # Get the class names from the results
        names = result[0].names

        # Initialize a list to store the number of objects detected per class
        class_detections_values = []

        # Count the number of objects detected for each class and add it to the list
        for k, v in names.items():
            class_detections_values.append(result[0].boxes.cls.tolist().count(k))

        # Create a dictionary mapping class names to the number of objects detected for that class
        classes_detected = dict(zip(names.values(), class_detections_values))

        # Print the time it took to process the image
        print(f"Image processed in {time.time() - image_time:.2f}s")

# Print the total time it took to process all images
print(f"All images processed in {time.time() - start_time:.2f}s")