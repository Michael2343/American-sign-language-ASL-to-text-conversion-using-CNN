import imageio
import imgaug as ia
import imgaug.augmenters as iaa
import imageio.v2 as imageio
from PIL import Image
import os

def make_aug(full_folder_path,jpg_file,input_img):
    path = full_folder_path + "/" + jpg_file
    
    #Vertical Flip
    vflip= iaa.Flipud(p=1.0) 
    input_vf= vflip.augment_image(input_img)

    im = Image.fromarray(input_vf)
    im.save(f"{path}_V.jpg")

    #Horizontal Flip
    hflip= iaa.Fliplr(p=1.0)
    input_hf= hflip.augment_image(input_img)

    im = Image.fromarray(input_hf)
    im.save(f"{path}_H.jpg")

    #crop 0.1 0.1
    crop1 = iaa.Crop(percent=(0.1, 0.1)) 
    input_crop1 = crop1.augment_image(input_img)

    im = Image.fromarray(input_crop1)
    im.save(f"{path}_C.jpg")

    #noise
    noise=iaa.AdditiveGaussianNoise(10,40)
    input_noise=noise.augment_image(input_img)

    im = Image.fromarray(input_noise)
    im.save(f"{path}_N.jpg")
    
    # roatation
    for i in range(2):
        rot = iaa.Affine(rotate=(-50,50))
        input_rot = rot.augment_image(input_img)
    
        im = Image.fromarray(input_rot)
        im.save(f"{path}_R{i}.jpg")
        
    # shear
    for i in range(2):
        shear = iaa.Affine(shear=(-50,50))
        input_shear=shear.augment_image(input_img)

        im = Image.fromarray(input_shear)
        im.save(f"{path}_S{i}.jpg")


def read_jpg_files(folder_path):
    current_script_path = os.path.dirname(os.path.abspath(__file__))
    full_folder_path = os.path.join(current_script_path, folder_path)
    arr = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for ch in arr:
        full_folder_path_letter = full_folder_path + "/" + ch + "/"
        jpg_files = [f for f in os.listdir(full_folder_path_letter) if f.lower().endswith(".jpg")]
        print(jpg_files)
        for jpg_file in jpg_files:
            file_path = os.path.join(full_folder_path_letter, jpg_file)

            try:
                # Read the image using imageio
                input_img = imageio.imread(file_path)
                print(f"Reading {full_folder_path} - {jpg_file}")

                # Process the image or perform any desired actions
                make_aug(full_folder_path_letter,jpg_file,input_img)

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

# Specify the relative path to the folder containing the JPG files
folder_path = ["dataset2/train","dataset2/test","dataset2/valid"]
folder_path = ["dataset_custom/train","dataset_custom/test"]

# Call the function
for path in folder_path:
    read_jpg_files(path)
