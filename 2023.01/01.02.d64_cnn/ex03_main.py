from ex01_customdataset import customDataset
from torch.utils.data import DataLoader
from torchvision import transforms
import torch

train_transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.RandomHorizontalFlip(p=0.6),
    transforms.RandomRotation(20),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),

])
val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),

])
test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),

])

# train val test dataset
train_dataset = customDataset("./dataset/train", transform=train_transform)
val_dataset = customDataset("./dataset/val" ,transform=None)
test_dataset = customDataset("./dataset/test", transform=None)
# train val test loader
train_loader = DataLoader(train_dataset, batch_size=126, shuffle=True)
val_dataset = DataLoader(val_dataset, batch_size=126 ,shuffle=False)
test_dataset = DataLoader(test_dataset, batch_size=1, shuffle=False)


for i, (img, label) in enumerate(train_loader) :
    print(img, label)
    exit()