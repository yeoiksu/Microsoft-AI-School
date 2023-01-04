from hw02_custom_dataset import CustomDataset
from hw04_utils import train, test_model

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
import albumentations as A
from torch.utils.data import DataLoader
from albumentations.pytorch import ToTensorV2
from timm.loss import BinaryCrossEntropy

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

train_transform = A.Compose([
    A.SmallestMaxSize(max_size= 256),
    A.Resize(height= 224, width= 224),
    A.HorizontalFlip(p= 0.5),
    A.VerticalFlip(p= 0.5),
    A.Normalize(mean = (0.485, 0.456, 0.406), std = (0.229, 0.224, 0.225)),
    ToTensorV2()
])
val_transform = A.Compose([
    A.SmallestMaxSize(max_size = 256),
    A.Resize(height=224, width=224),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2()
])

# dataset
train_dataset = CustomDataset("./0104/data_hw/train", transform= train_transform)
valid_dataset = CustomDataset("./0104/data_hw/test" , transform= val_transform)

# data loader
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
valid_loader = DataLoader(valid_dataset, batch_size=32, shuffle=False)
test_loader  = DataLoader(valid_dataset , batch_size=32, shuffle=False)

# model
# net = models.__dict__["resnet18"](pretrained=True)
# net.fc = nn.Linear(512,2)
# net.to(device)

net = models.__dict__["resnet50"](pretrained= True)
net.fc = nn.Linear(2048,2)
net.to(device)

criterion = BinaryCrossEntropy()
optimizer = optim.AdamW(net.parameters(), lr= 0.001)
save_dir = "./0104"
num_epoch = 100


if __name__ == "__main__":
    train(num_epoch, net, train_loader, valid_loader, criterion, 
        optimizer , save_dir, device)
    test_model(net, test_loader, device)
