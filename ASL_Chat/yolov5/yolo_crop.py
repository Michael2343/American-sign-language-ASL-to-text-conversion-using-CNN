import os
import cv2

def read_bbox_from_txt(file_path):
    with open(file_path, 'r') as file:
        line = file.readline().strip().split()
        # Assuming the format is: [class] [center_x] [center_y] [width] [height]
        class_label = int(line[0])
        center_x, center_y, width, height = map(float, line[1:])
        return class_label, center_x, center_y, width, height

def crop_image(image_path, bbox):
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    class_label, center_x, center_y, rel_width, rel_height = bbox

    # Convert normalized coordinates to absolute pixel values
    abs_width = int(rel_width * width)
    abs_height = int(rel_height * height)
    abs_x = int((center_x - rel_width/2) * width)
    abs_y = int((center_y - rel_height/2) * height)

    # Crop the image
    cropped_image = image[abs_y:abs_y+abs_height, abs_x:abs_x+abs_width]

    return cropped_image

def crop_and_save_all_images(images_folder, labels_folder, crop_folder):
    # Make sure the crop folder exists
    os.makedirs(crop_folder, exist_ok=True)

    # Get a list of all image files in the images folder
    image_files = [file for file in os.listdir(images_folder) if file.endswith(('.jpg', '.jpeg', '.png'))]

    for image_file in image_files:
        # Construct paths for the current image and label file
        image_path = os.path.join(images_folder, image_file)
        label_file = os.path.join(labels_folder, image_file.replace('.jpg', '.txt'))

        # Read bounding box information from the label file
        bbox = read_bbox_from_txt(label_file)

        # Crop the image based on the bounding box
        cropped_image = crop_image(image_path, bbox)

        # Save the cropped image to the crop folder
        save_path = os.path.join(crop_folder, image_file)
        cv2.imwrite(save_path, cropped_image)
        print(f"Cropped image saved at: {save_path}")

if __name__ == "__main__":
    # Folders
    images_folder = "images"
    labels_folder = "labels"
    crop_folder = "crop"

    # Crop and save all images
    crop_and_save_all_images(images_folder, labels_folder, crop_folder)
