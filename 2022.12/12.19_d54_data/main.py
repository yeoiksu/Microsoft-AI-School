from dataset_temp import CustomDataset
import albumentations as A
from albumentations.pytorch import ToTensorV2

from torchvision import transforms
from torch.utils.data import DataLoader
from torchvision import models
import hyper_parameter
from utils import *

import os
import torch
import torch.nn as nn
import torch.nn.functional as F

## Model Build 시작
device = torch.device("cpu") 

# train aug
train_transform = A.Compose([
    A.Resize(height= 100, width=100),
    ToTensorV2()
])

# val aug
val_transform = A.Compose([
    A.Resize(height= 100, width=100),
    ToTensorV2()
])

# dataset
train_dataset = CustomDataset("./2022.12/12.19_d54_data/data/train", transform= train_transform)
val_dataset   = CustomDataset("./2022.12/12.19_d54_data/data/val"  , transform= val_transform)

# data loader
train_loader = DataLoader(train_dataset, batch_size= hyper_parameter.batch_size, shuffle= True)
val_loader   = DataLoader(val_dataset  , batch_size= hyper_parameter.batch_size  , shuffle= False)

# for index, (image, target) in enumerate(train_loader):
#     print(index, image, target)


# model 
net = models.__dict__["resnet18"](pretrained = True)
# net = models.__dict__["resnet34"](pretrained = True)

# pretrained = true num_classes 5 : output 5종류
net.fc = nn.Linear(512,5)
net.to(device)

# criterion
criterion = nn.BCEWithLogitsLoss.to(device)

# optimizier
optim = torch.optim.Adam(net.parameters(), lr = hyper_parameter.lr)

# def train
train(
    number_epoch= hyper_parameter.epochs, 
    train_loader= train_loader,
    val_loader= val_loader,
    criterion= criterion,
    optimizer= optim,
    model= net,
    save_dir= "./2022.12/12.19_d54_data",
    device= device
    )

