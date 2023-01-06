from ex01_custom_dataset import customDataset
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision import models
import torch.nn as nn
import torch
import torch.optim as optim

from ex03_utils import train ,test

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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
val_dataset = customDataset("./dataset/val" ,transform=val_transform)
test_dataset = customDataset("./dataset/test", transform=test_transform)
# train val test loader
train_loader = DataLoader(train_dataset, batch_size=126, shuffle=True, num_workers=4)
val_loader = DataLoader(val_dataset, batch_size=126 ,shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)

# model 처리 완료 !!
net = models.resnet18(pretrained=False)
in_feature_val = net.fc.in_features
net.fc = nn.Linear(in_feature_val, 4)
net.to(device)

# model loader
net.load_state_dict(torch.load("./best.pt", map_location=device))

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001)

if __name__ == '__main__':
    # train(100, train_loader, val_loader, net, optimizer, criterion, device, save_path="./best.pt")
    # def test(model, data_loader, device) :
    test(net, test_loader, device)