from PIL import Image
import cv2

import numpy as np
import time

import torch
import torchvision
from torch.utils.data import Dataset
from torchvision import transforms
import matplotlib.pyplot as plt
import albumentations
from albumentations.pytorch import ToTensorV2

class alb_cat_dataset(Dataset):
    def __init__(self, file_paths, transform=None):
        self.file_paths = file_paths
        self.transform = transform

    def __getitem__(self, index):
        file_path = self.file_paths[index]

        # read an image with opencv
        image = cv2.imread(file_path)

        # BRG -> RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        self.st_time = time.time()
        if self.transform is not None:
            image = self.transform(image=image)["image"]
            total_time = (time.time() - self.st_time)

        return image, total_time

    def __len__(self):
        return len(self.file_paths)

        # 기존 torchvision Data pipeline
        # 1. dataset class -> image loader -> transform


class CataDataset(Dataset):
    def __init__(self, file_paths, trnasform = None):
        self.file_paths = file_paths
        self.transform = trnasform

    def __getitem__(self, index):
        # file_path = self.file_paths
        file_path = self.file_paths[index]

        image = Image.open(file_path)  # read image with PIL

        # transform time check
        start_time = time.time()
        if self.transform:
            image = self.transform(image)
        end_time = (time.time() - start_time)

        return image, end_time

    def __len__(self):
        return len(self.file_paths)

"""
### 나눌때는 random을 가지고 있는 요소는 다 삭제해야함 !!!
train_transform = transforms.Compose([
])

val_transform = transforms.Compose([
])
"""

### data aug transform
torchvision_transform = transforms.Compose([
    # transforms.Pad(padding= 10),            # 1. pad
    # transforms.Resize((256, 256)),          # 2. Resize (보통 정사각형 만들고 실행)
    # transforms.CenterCrop(size= (300)),     # 3. crop center (중앙 자르기, 거의 사용하지 않음)
    # transforms.Grayscale(),                 # 4. gray scale
    transforms.ColorJitter(                 # 5. 색상
        brightness= 0.2, 
        hue= 0.2,
        contrast= 0.3),  
    # transforms.GaussianBlur(                # 6. 가우시안 블러
    #     kernel_size= 3,
    #     sigma= (0.1, 2)),    
    # transforms.RandomPerspective(           # 7. 이미지 틀기
    #     distortion_scale= 0.7,
    #     p= 0.3),  # 확률 30%
    # transforms.RandomRotation(degrees= (0,100)),  # 8. 회전     
    #                 
    # transforms.RandomAffine(            # 9. Affine 
    #     degrees= (30, 60),
    #     translate= (0.1, 0.3),
    #     scale= (0.5, 0.7)),                         
    # transforms.RandomEqualize(p= 0.8),  # 10. 색상 비슷하게
    # transforms.RandAugment(),  # 11. 랜덤으로 하나줌
    # transforms.RandomHorizontalFlip(),  # 11. 좌우 반전
    # transforms.RandomVerticalFlip(),  # 12. 상하 반전
    # transforms.AutoAugment(),  # 13. 자동 Augment
    transforms.ToTensor()
])

albumentations_transform = albumentations.Compose([
    albumentations.Resize(256, 256),
    albumentations.RandomCrop(224, 224),
    albumentations.HorizontalFlip(),
    albumentations.VerticalFlip(),
    # albumentations.pytorch.transforms.ToTensor(),
    ToTensorV2()
])

albumentations_transform_oneof = albumentations.Compose([
    albumentations.Resize(256, 256),
    albumentations.RandomCrop(224, 224),
    albumentations.OneOf([
        albumentations.HorizontalFlip(p= 1),
        albumentations.RandomRotate90(p= 1),
        albumentations.VerticalFlip(p= 1),
    ], p= 1),
    albumentations.OneOf([
        albumentations.HorizontalFlip(p= .5),
        albumentations.MotionBlur(p= 1),
        albumentations.OpticalDistortion(p= 1),
        albumentations.GaussNoise(p= 1),
    ], p= 1),
    ToTensorV2()
])

cat_dataset = CataDataset(
    file_paths= ["./2022.12/12.15_d52_image/data/cat.png"], 
    trnasform= torchvision_transform
)

alb_dataset = alb_cat_dataset(
    file_paths= ["./2022.12/12.15_d52_image/data/cat.png"],
    transform= albumentations_transform)

alb_oneof = alb_cat_dataset(
    file_paths= ["./2022.12/12.15_d52_image/data/cat.png"],
    transform= albumentations_transform_oneof)

# from matplotlib import pyplot as plt
total_time = 0
for i in range(100):
    image, end_time = cat_dataset[0]
    total_time += end_time
print("torchvision tiem/image >> ", total_time*10)

alb_total_tiem = 0
for i in range(100):
    alb_image, alb_time = alb_dataset[0]
    alb_total_tiem += alb_time
print("alb time >> ", alb_total_tiem*10)

alb_oneof_tiem = 0
for i in range(100):
    alb_oneof_image, alb_oneof_time = alb_oneof[0]
    alb_oneof_tiem += alb_oneof_time
print("alb time >> ", alb_oneof_tiem*10)


# plt.figure(figsize=(10, 10))
# plt.imshow(transforms.ToPILImage()(image).convert("RGB"))
# plt.show()
