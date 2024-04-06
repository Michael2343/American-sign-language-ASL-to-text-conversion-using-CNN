import torchvision.transforms as transforms
import torch

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
PYTORCH_MODEL = True 
CUSTOM_MODEL = False
IMAGES_OR_CAM = True #True-images False-cam

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
PT_PATH = 'models/20_03_2024_14_04_09/'
PT_FILE = 'densenet121_best.pt' 

#paths
DATASET_PATH_TRAIN = 'dataset_custom2/train'
DATASET_PATH_TEST = 'dataset_customGH/test'

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
BATCH_SIZE = 16
EPOCHS = 200

#Adam params (default)
LEARNING_RATE = 0.001
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
