# Constants
PORT = 1234
HOME_PAGE = 0
HOST_PAGE = 1
CLIENT_PAGE = 2
CHAT_PAGE = 3

#Font
BASE_STYLE = (
    f'font-weight: bold; '
    f'font-style: italic; '
    f'font-family: halvetica; '
    f'font-size: 16px; '
    f'padding: 5px; '
    f'border-radius: 10px; '
    f'width: 425px;'
)

def generate_style(color):
    return BASE_STYLE + (
    f'color: {color}; '
    f'border: 1px solid {color}; '
    )

import torchvision.transforms as transforms
import torch

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#Densenet params               
GROWTH_RATE = 32
NUM_INIT_FEATURES = 64
BN_SIZE= 4
DROP_RATE = 0.2
NUM_CLASSES = 29
MEMORY_EFFICIENT = False

DENSENET_TYPE = "121" 
DENSENET_TYPE_DICT = {
   "121": [6, 12, 24, 16],   
   "169": [6, 12, 32, 32],
   "201": [6, 12, 48, 32]
}

#change path and file after train (for test and detect) 
PT_PATH = 'densenet_asl/models/20_03_2024_13_59_09/' #12_03_2024_13_30_53 + new 
PT_FILE = 'densenet121_best.pt' 

#paths
DATASET_PATH_TRAIN = 'densenet_asl/dataset/train'
DATASET_PATH_TEST = 'densenet_asl/dataset/test'


# transforms_norm from norm.py
# Mean: [0.5858049, 0.4458805, 0.33990178]
# Std: [0.19744971, 0.18429077, 0.19292982]

#transforms_norm according to https://pytorch.org/hub/pytorch_vision_densenet/
# Mean: [0.485, 0.456, 0.406]
# Std: [0.229, 0.224, 0.225]

NORM_MEAN = [0.485, 0.456, 0.406]
NORM_STD= [0.229, 0.224, 0.225]

TRANSFORM_CLEAN = transforms.Compose([transforms.Resize((224,224)),
                                     transforms.ToTensor()
                                     ])

TRANSFORM_MEAN_STD = transforms.Compose([transforms.Resize((224,224)),
                                     transforms.ToTensor(),
                                     transforms.Normalize(mean=NORM_MEAN,
                                        std=NORM_STD)
                                     ])

# Train params
BATCH_SIZE = 32
EPOCHS = 20

#Adam params (default)
LEARNING_RATE = 1e-3
WEIGHT_DECAY= 0
BETAS=(0.9,0.999)
EPS=1e-08

# load model densenet from pytorch
# train_model = torch.hub.load('pytorch/vision:v0.10.0', 'densenet121', pretrained=True) #121 169 201 on ImageNet
# torch.save(train_model, 'models/pytorch/densenet121.pt')
# train_model = torch.hub.load('pytorch/vision:v0.10.0', 'densenet169', pretrained=True) #121 169 201 on ImageNet
# torch.save(train_model, 'models/pytorch/densenet169.pt')
# train_model = torch.hub.load('pytorch/vision:v0.10.0', 'densenet201', pretrained=True) #121 169 201 on ImageNet
# torch.save(train_model, 'models/pytorch/densenet201.pt')
