"""
This script defines functions to load a DenseNet model, perform object detection using the model, 
and handle either static images or real-time video streams. It includes a function to load the DenseNet 
model, and to perform object detection on images. 
If it's set to process images, it loads images from specified paths and applies object detection. 
If it's set to process a video stream, it captures frames from the webcam, converts them to PIL images, and performs object detection.
"""

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from densenet import *
from PIL import Image
import torchvision.transforms.functional as TF
import torch
import time
from CONST_DENSENET import *

# Function to get the DenseNet model
def get_model():
    model = make_densenet(type=DENSENET_TYPE).to(DEVICE)
    trained_model = torch.load(PT_PATH+PT_FILE)
    model.load_state_dict(trained_model.state_dict())
    return model
    
model = get_model()
# print(model)

# Function to detect objects using DenseNet model
def densenet_detect(image):
    # Set the model to evaluation mode
    model.eval()
    start_time = time.time()

    # Apply the same transformations used during training
    processed_image = TRANSFORM_MEAN_STD(image)

    # Add a batch dimension to match the model's input shape
    processed_image = processed_image.unsqueeze(0)

    # Move the processed image to the device (GPU or CPU)
    processed_image = processed_image.to(DEVICE)

    # Make predictions
    with torch.no_grad():
        outputs = model(processed_image)
        probabilities = nn.functional.softmax(outputs, dim=1)

    # Get the predicted class and confidence score
    confidence_score, predicted_class = torch.max(probabilities, 1)

    end_time = time.time()

    print(f'The predicted class is: {predicted_class.item()} with conf= {confidence_score.item()*100}%')
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    print("")

# Entry point of the script
if __name__ == "__main__":
    if IMAGES_OR_CAM:
        # Load the image from a file
        # images_path = ['96.jpg','232.jpg','339.jpg']  # Replace with the actual path to your image

        for im in images_path:
            print(im)
            image = Image.open(im)
            densenet_detect(image)
    else:
        import cv2 
        # define a video capture object 
        vid = cv2.VideoCapture(0) 
        
        while(True): 
            
            # Capture the video frame 
            # by frame 
            ret, frame = vid.read() 
        
            opencv_image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create a PIL Image from the NumPy array
            pil_image = Image.fromarray(opencv_image_rgb)
            densenet_detect(pil_image)

            # the 'q' button is set as the 
            # quitting button you may use any 
            # desired button of your choice 
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break
                      