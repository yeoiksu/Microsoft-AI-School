import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import Dataset
import os
from torchvision.io import read_image

file_path = './2022.12/12.09_d48_image/data/selenium'
IMAGE_SIZE = 28

class CustomImageDataset(Dataset):
    def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
        self.img_labels = pd.read_csv(annotations_file, names=['file_name', 'label'], skiprows=[0])
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        try:
            image = read_image(img_path)
        except:
            print(self.img_labels.iloc[idx, 0])
            exit()
        label = int(self.img_labels.iloc[idx, 1])
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label

#### Define Neural Netowrk model
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(784, 512)  # input 28x28 = 784
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 128)
        self.fc4 = nn.Linear(128, 64)
        self.fc5 = nn.Linear(64, 32)
        self.fc6 = nn.Linear(32, 10)    # Output 0~9 = 10 labels

    def forward(self, x):
        x = x.float()
        h1 = F.relu(self.fc1(x.view(-1, 784)))
        h2 = F.relu(self.fc2(h1))
        h3 = F.relu(self.fc3(h2))
        h4 = F.relu(self.fc4(h3))
        h5 = F.relu(self.fc5(h4))
        h6 = self.fc6(h5)
        return F.log_softmax(h6, dim=1)

#### Prepare Data Loader for Training and Validation
transform = transforms.Compose([
                        transforms.ToTensor(),
                        transforms.Normalize((0.1307,), (0.3081,))
                        ])

#### vars and deivce 설정
epochs = 10         # 몇번 학습
lr = 0.001          # learning rate
momentum = 0.5      # optimizer 최적화 함수에 들어가는 관성계수
no_cuda = True      # cuda인지
seed = 1            # random seed
log_interval = 5 

use_cuda = not no_cuda and torch.cuda.is_available()
torch.manual_seed(seed)
# cuda면 cuda쓰고 아니면 cpu 사용
device = torch.device("cuda" if use_cuda else "cpu")  
kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else{}  
                # 1: 사용 프로세서 1로설정

batch_size = 16    # 한번 학습할때 몇개
test_batch_size = 16

dataset_train = CustomImageDataset(
    annotations_file= os.path.join(file_path, 'annotation_train.csv'),
    img_dir= file_path + '/train',
    )

dataset_test = CustomImageDataset(
    annotations_file= os.path.join(file_path, 'annotation_test.csv'),
    img_dir= file_path + '/test',
    )

train_loader = torch.utils.data.DataLoader(dataset_train, batch_size= batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset_test, batch_size=test_batch_size, shuffle=True, **kwargs)

model = Net().to(device)  # devce : cpu or gpu ?? 나는 cpu
optimizer = optim.SGD(model.parameters(), lr= lr, momentum= momentum)

#### model 생성, train 함수 생성, nll loss는 분류문제에 사용, softmax 함수와 함께 사용  
def train(log_interval, model, device, train_loader, optimizer, epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))

def test(log_interval, model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format
          (test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

for epoch in range(1, epochs+1):
    print(epoch)
    train(log_interval, model, device, train_loader, optimizer, epoch)
test(log_interval, model, device, test_loader)

torch.save(model, file_path + '/model.pt')  # 가중치