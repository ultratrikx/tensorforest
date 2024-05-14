import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def read_bounding_boxes(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    boxes = [list(map(float, line.strip().split())) for line in lines]
    return boxes

def create_heatmap(image, boxes, cmap):
    heatmap = np.zeros_like(image[:, :, 0])
    for box in boxes:
        x, y, w, h = map(int, box)
        heatmap[y:y+h, x:x+w] += 1
    heatmap = cv2.applyColorMap(heatmap, cmap)
    return heatmap

image_folder = 'rotated_results'
label_folder = 'labels'

heatmap_results_folder = 'heatmap_results'

# Create the directory if it does not exist
if not os.path.exists(heatmap_results_folder):
    os.makedirs(heatmap_results_folder)

for image_name in os.listdir(image_folder):
    image_path = os.path.join(image_folder, image_name)
    image = cv2.imread(image_path)

    label_file_path = os.path.join(label_folder, image_name.replace('.jpg', '.txt'))

    # Check if the label file exists
    if not os.path.exists(label_file_path):
        print(f"No detections for {image_name}, skipping...")
        continue

    boxes = read_bounding_boxes(label_file_path)

    coniferous_boxes = [box[1:5] for box in boxes if box[0] == 0]
    deciduous_boxes = [box[1:5] for box in boxes if box[0] == 1]

    # Draw the filled bounding boxes on the image
    for box in coniferous_boxes:
        x, y, w, h = box
        x, w = x * image.shape[1], w * image.shape[1]  # Convert x and width to pixel coordinates
        y, h = y * image.shape[0], h * image.shape[0]  # Convert y and height to pixel coordinates
        if w <= 100 and h <= 100:  # Only draw the box if its width and height are less than or equal to 100
            cv2.rectangle(image, (int(x - w/2), int(y - h/2)), (int(x + w/2), int(y + h/2)), (0, 0, 255), -1)  # Red color for coniferous

    for box in deciduous_boxes:
        x, y, w, h = box
        x, w = x * image.shape[1], w * image.shape[1]  # Convert x and width to pixel coordinates
        y, h = y * image.shape[0], h * image.shape[0]  # Convert y and height to pixel coordinates
        if w <= 100 and h <= 100:  # Only draw the box if its width and height are less than or equal to 100
            cv2.rectangle(image, (int(x - w/2), int(y - h/2)), (int(x + w/2), int(y + h/2)), (255, 0, 0), -1)  # Blue color for deciduous

    cv2.imwrite(os.path.join(heatmap_results_folder, image_name), image)

    # Display the image with bounding boxes using matplotlib
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(image_name)
    plt.show()