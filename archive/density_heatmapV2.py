import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Define the class values
class_values = {
    'aspen': 0,  # VERY LOW
    'larch': 1,  # LOW
    'pine': 2,  # HIGH
    'white_spruce': 2,  # HIGH
    'black_spruce': 3,  # EXTREME
}



# MIGHT HAVE TO CHANGE THE CODE AS THE LABELSTXT FILE MIGHT SAVE THE CLASS VALUE AS AN INT ISNTEAD OF A STRING


def read_bounding_boxes(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    boxes = [line.strip().split() for line in lines]
    return boxes

def create_heatmap(image, boxes, class_values, cmap):
    heatmap = np.zeros_like(image[:, :, 0])
    for box in boxes:
        class_name, x_center, y_center, width, height, _ = box
        class_value = class_values.get(class_name, 0)
        x = int(float(x_center) * image.shape[1])
        y = int(float(y_center) * image.shape[0])
        w = int(float(width) * image.shape[1])
        h = int(float(height) * image.shape[0])
        heatmap[y-h//2:y+h//2, x-w//2:x+w//2] += class_value
    heatmap = cv2.applyColorMap(heatmap, cmap)
    return heatmap

image_folder = 'rotated_results'
label_folder = 'labels'

heatmap_results_folder = 'heatmap_results'

# Create the directory if it does not exist
if not os.path.exists(heatmap_results_folder):
    os.makedirs(heatmap_results_folder)

image_name = 'your_image.jpg'  # Replace with your image name
image_path = os.path.join(image_folder, image_name)
image = cv2.imread(image_path)

label_file_path = os.path.join(label_folder, image_name.replace('.jpg', '.txt'))

# Check if the label file exists
if not os.path.exists(label_file_path):
    print(f"No detections for {image_name}, skipping...")
else:
    boxes = read_bounding_boxes(label_file_path)
    heatmap = create_heatmap(image, boxes, class_values, cv2.COLORMAP_JET)
    cv2.imwrite(os.path.join(heatmap_results_folder, image_name), heatmap)

    # Display the image with bounding boxes using matplotlib
    plt.imshow(cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB))
    plt.title(image_name)
    plt.show()