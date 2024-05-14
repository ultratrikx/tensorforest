import os
import cv2
import numpy as np

# Define the class values and corresponding colors
class_values = {
    0: (0, 255, 255),  # aspen - VERY LOW (Yellow)
    1: (0, 165, 255),  # larch - LOW (Orange)
    2: (0, 0, 255),  # pine - HIGH (Red)
    3: (0, 0, 128),  # white_spruce - EXTREME (Maroon Red)
    4: (0, 0, 128),  # black_spruce - EXTREME (Maroon Red)
    5: (0, 0, 255),  # coniferous - HIGH (Red)
    6: (0, 165, 255),  # deciduous - LOW (Orange)
}

# Define the directory where the images are stored
image_folder = 'LOL'

# Function to read bounding boxes from a file
def read_bounding_boxes(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    boxes = [line.strip().split() for line in lines]
    return boxes

# Function to create a heatmap from the bounding boxes
def create_heatmap(image, boxes, class_values):
    for box in boxes:
        class_name, x_center, y_center, width, height, _ = box
        color = class_values.get(int(class_name), (0, 0, 0))
        x = int(float(x_center) * image.shape[1])
        y = int(float(y_center) * image.shape[0])
        w = int(float(width) * image.shape[1])
        h = int(float(height) * image.shape[0])
        cv2.rectangle(image, (x-w//2, y-h//2), (x+w//2, y+h//2), color, -1)
    return image

# Function to create a legend for the heatmap
def create_legend(class_values):
    labels = ["VERY LOW", "LOW", "HIGH", "EXTREME"]
    colors = [class_values[i] for i in range(len(class_values))]  # Get colors from class_values

    legend = np.zeros((100, 500, 3), dtype='uint8')
    for i, (label, color) in enumerate(zip(labels, colors)):
        cv2.rectangle(legend, (i*70, 0), ((i+1)*70-10, 50), color, -1)
        cv2.putText(legend, label, (i*70+5, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    return legend

# Create the legend
legend = create_legend(class_values)

# Iterate over the files in the image folder
for file_name in os.listdir(image_folder):
    if not file_name.endswith('.jpg' or '.jpeg' or '.png'):
        continue  # Skip non-image files
    image_path = os.path.join(image_folder, file_name)
    image = cv2.imread(image_path)

    label_folder = os.path.join(image_folder, 'labels')
    label_file_path = os.path.join(label_folder, file_name.replace('.jpg', '.txt'))

    boxes = read_bounding_boxes(label_file_path)
    if not boxes:
        print(f"No detections for {file_name}, skipping...")
        continue

    heatmap = create_heatmap(image, boxes, class_values)

    # Save the heatmap image
    output_folder = os.path.join(image_folder, 'heatmap_results')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cv2.imwrite(os.path.join(output_folder, file_name), heatmap)
    cv2.imwrite(os.path.join(output_folder, 'legend.jpg'), legend)