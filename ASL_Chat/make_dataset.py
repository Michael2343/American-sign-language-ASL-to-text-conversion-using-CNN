""" 
This script captures images from a video feed, detects objects using a YOLOv5 model,
crops the detected objects, and saves them into training and testing directories.
It also includes functions to create a countdown before capturing photos and to create
directories if they don't exist.
The script is designed to collect data for training a model to recognize characters
from the video feed.  
"""

import cv2
import torch
from PIL import Image
import time
from densenet import *
import os  

# Function to create a countdown
def countdown(sec):
    for i in range(sec, 0, -1):
        print(i)
        time.sleep(1)
    print("GO!")
    
# Function to create a directory if it doesn't exist
def make_path(path):
    if not os.path.exists(path):
        try:
        # Create the target directory
            os.makedirs(path)
            print("Directory created successfully.")
        except FileNotFoundError:
            print("Parent directory not found.")
        except PermissionError:
            print("Permission denied to create directory.")
        except Exception as e:
            print("An error occurred:", e)
    else:
        print("Directory already exists.")
    
# Model
path = 'yolov5/yolov5l6_v3.pt' #base+c+h
model = torch.hub.load('yolov5', 'custom', path=path, source='local',force_reload = True) 
dataset = "dataset"
pathLetter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# pathLetter = ["Z_DELETE","Z_ENTER","Z_SPACE"]

number_photos = 20
number_test = 4

vid = cv2.VideoCapture(0) 

# Iterate through each character
for ch in pathLetter:
    
    path_train = os.path.join(dataset,"train", ch)
    make_path(path_train)
    path_test = os.path.join(dataset, "test",ch)
    make_path(path_test)
    
    # define a video capture object 
    cnt = 0
    print("Ready fot letter",ch)
    countdown(3)

    while cnt <=number_photos:
        ret, frame = vid.read() 
        
        opencv_image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # # Create a PIL Image from the NumPy array
        # pil_image = Image.fromarray(opencv_image_rgb)
        
        # save_path = f"{dataset}/{pathLetter}"
        # save_photo = f"{save_path}/{pathLetter}_{cnt}.jpg"
        # pil_image.save(save_photo)
        # print(f"PHOTO SAVE: {save_photo}")
        # time.sleep(2)
        # cnt = cnt +1

        results = model(opencv_image_rgb)  # includes NMS

        try:
            # Extract coordinates from results.xyxy[0]
            x1, y1, x2, y2, confidence, class_label = results.xyxy[0][0].cpu().numpy()

            # Create a PIL Image from the NumPy array
            opencv_image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create a PIL Image from the NumPy array
            pil_image = Image.fromarray(opencv_image_rgb)
            
            # Crop the region based on the coordinates
            cropped_img = pil_image.crop((x1, y1, x2, y2))
    
            if cnt <= number_photos - number_test:
                save_path = path_train
            else:
                save_path = path_test

            save_photo = f"{save_path}/{ch}_{cnt}.jpg"
            cropped_img.save(save_photo)
            print(f"PHOTO SAVE: {save_photo}")
            cnt = cnt +1
            time.sleep(1)

            # densnet = make_densenet(type=DENSENET_TYPE).to(DEVICE)
            # _,_, probs = densnet.densenet_detect(cropped_img)
            # x=sum(probs[0])
            # print(x, probs)
            
            
        except Exception as e:
            print(e)
            
        if cv2.waitKey(1) & 0xFF == ord('q'): 
                break
                