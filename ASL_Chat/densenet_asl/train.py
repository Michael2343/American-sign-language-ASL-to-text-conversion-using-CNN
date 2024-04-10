"""
This script trains a DenseNet model on a custom dataset. It loads necessary libraries, creates a custom
dataset using ImageFolder, sets up model training parameters, trains the model, and saves the best and last
trained models along with training logs.
"""

import torch
import torch.nn as nn
import torchvision
from densenet import *
from torchvision.datasets import DatasetFolder
import torch
from CONST_DENSENET import *
import sys
from datetime import datetime
import os 

# Function to train the DenseNet model
def densenet_train(batch,lr):

    # Create a custom dataset using ImageFolder
    train_dataset = torchvision.datasets.ImageFolder(
        root=DATASET_PATH_TRAIN,
        transform=TRANSFORM_MEAN_STD
    )

    # Instantiate loader objects to facilitate processing
    train_loader = torch.utils.data.DataLoader(dataset = train_dataset,
                                            batch_size = batch,
                                            shuffle = True)


    # Instantiate the DenseNet model
    model = make_densenet(type=DENSENET_TYPE).to(DEVICE)
    print(model.get_densenet_type())
    
    pre_trained_model = None 

    # Load pre-trained model if specified
    if PYTORCH_MODEL: 
        pre_trained_model = torch.load('models/pytorch/densenet'+DENSENET_TYPE+'.pt')
    if CUSTOM_MODEL:
        pre_trained_model = torch.load(PT_PATH+PT_FILE)
        
    if pre_trained_model != None:
        # Freeze pre-trained layers
        for param in pre_trained_model.parameters():
            param.requires_grad = False
        # Extract final layer
        final_layer = pre_trained_model.classifier

        # Input dimension of the final layer (can be found using print(final_layer))
        in_features = final_layer.in_features
        # Create new final layer for your NUM_CLASSES classes
        new_final_layer = nn.Linear(in_features, NUM_CLASSES)
        # Replace the final layer in the pre-trained model
        pre_trained_model.classifier = new_final_layer
        model.load_state_dict(pre_trained_model.state_dict(), strict=False)

    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(),lr=lr, betas=BETAS,eps=EPS, weight_decay=WEIGHT_DECAY)

    best_loss = [sys.maxsize,-1]
    best_model = None
    
    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    path = f"models/{dt_string}"
    os.mkdir(path)
    
    # Write training parameters to a file
    f = open(f'{path}/params.txt', "w")
    f.write(f'densenet{DENSENET_TYPE}\n')
    f.write(f'PYTORCH_MODEL={PYTORCH_MODEL}\n')
    f.write(f'BATCH_SIZE={batch}\n')
    f.write(f'EPOCHS={EPOCHS}\n')
    f.write(f'Adam params:\n')
    f.write(f'LEARNING_RATE={lr}\n')
    f.write(f'WEIGHT_DECAY={WEIGHT_DECAY}\n')
    f.write(f'BETAS={BETAS}\n')
    f.write(f'EPS={EPS}\n')
    
    print("start train")
    # We use the pre-defined number of epochs to determine how many iterations to train the network on
    for epoch in range(EPOCHS):
        model.train()
        #Load in the data in batches using the train_loader object
        for i, (images, labels) in enumerate(train_loader):  

            # Move tensors to the configured device
            images = images.to(DEVICE)
            labels = labels.to(DEVICE)
            
            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
        progress = 'Epoch [{}/{}], Loss: {:.8f}'.format(epoch+1, EPOCHS, loss.item())
        print(progress)
        f.write(f'{progress}\n')

        # Update best loss and model if current loss is better
        if loss.item()<best_loss[0]:
            best_loss = [loss.item(),epoch+1]
            best_model = model
    
    best_str = f"best loss:{best_loss[0]} at epoch {best_loss[1]}"
    print(best_str)
    f.write(f'{best_str}\n')

    f.close()
    
    # Save the model (best and last)
    torch.save(model, f'{path}/densenet'+DENSENET_TYPE+'_last.pt')
    torch.save(best_model, f'{path}/densenet'+DENSENET_TYPE+'_best.pt')

# Entry point of the script      
if __name__ == "__main__": 
    densenet_train(batch=16,lr=0.0001)
