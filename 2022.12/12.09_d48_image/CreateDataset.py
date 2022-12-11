import pandas as pd
import cv2
import torch
from torch.utils.data import Dataset
from torchvision.io import read_image
import os

df_dict = {
    'file_name' : [],
    'label' : []
}

test_dict = {
    'file_name' : [],
    'label' : []
}

IMG_SIZE = 28 # FashionMNIST와 같은 크기
root = './crawling/'

os.makedirs('./dataset/train/', exist_ok=True)
os.makedirs('./dataset/test/', exist_ok=True)

for idx, label in enumerate(os.listdir(root)):
    temp_path = os.path.join(root + label)
    cut_ = int(len(os.listdir(temp_path))*0.8)
    for file in os.listdir(temp_path)[:cut_]:
        img = cv2.imread(root + label + '/' + file)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        cv2.imwrite(f'./dataset/train/{file}', img)
        df_dict['file_name'].append(file)
        df_dict['label'].append(idx)
    
    for file in os.listdir(temp_path)[cut_:]:
        img = cv2.imread(root + label + '/' + file)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        cv2.imwrite(f'./dataset/test/{file}', img)
        test_dict['file_name'].append(file)
        test_dict['label'].append(idx)

df = pd.DataFrame(df_dict)
# print(df)
df.to_csv('./dataset/annotation.csv')

test_df = pd.DataFrame(test_dict)
test_df.to_csv('./dataset/test_annotation.csv')

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

dataset = CustomImageDataset(
    annotations_file = './dataset/annotation.csv',
    img_dir = './dataset/train'
)
test_dataset = CustomImageDataset(
    annotations_file = './dataset/test_annotation.csv',
    img_dir = './dataset/test'
)

train_loader = torch.utils.data.DataLoader(dataset, batch_size=8, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=8, shuffle=True)