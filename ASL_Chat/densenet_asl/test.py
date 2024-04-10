"""
This script tests the performance of a pre-trained DenseNet model on a custom dataset.
It loads necessary libraries, creates a custom dataset using ImageFolder, loads a pre-trained
DenseNet model, evaluates its performance on the test dataset, and writes the accuracy results
to a file.
"""
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from densenet import *
from torchvision.datasets import DatasetFolder
import torch
from CONST_DENSENET import *

# Function to test the pre-trained DenseNet model
def densenet_test():
    # Create a custom dataset using ImageFolder
    test_dataset = torchvision.datasets.ImageFolder(
        root=DATASET_PATH_TEST,
        transform=TRANSFORM_MEAN_STD
    )

    # Create a DataLoader for the test dataset
    test_loader = torch.utils.data.DataLoader(dataset = test_dataset,
                                            batch_size = BATCH_SIZE,
                                            shuffle = True)

    # Load the DenseNet model
    model = make_densenet(type=DENSENET_TYPE).to(DEVICE)
    trained_model = torch.load(PT_PATH+PT_FILE)
    model.load_state_dict(trained_model.state_dict())
    model.eval()

    # Perform inference on the test dataset
    with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in test_loader:
            images = images.to(DEVICE)
            labels = labels.to(DEVICE)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
        # Calculate accuracy
        acc = 100 * correct / total
        f = open(f'{PT_PATH}/params.txt', "a")
        f.write(f'Accuracy={acc}% on {DATASET_PATH_TEST}\n')
        f.close()
        print('Accuracy of the network on the test images: {}%'.format(acc))

# Entry point of the script
if __name__ == "__main__":
    torch.cuda.empty_cache()
    densenet_test()
    