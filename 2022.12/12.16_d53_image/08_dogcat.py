import torch
import cv2
import os
import copy
import glob
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
import albumentations as A
from albumentations.pytorch import ToTensorV2

# m1제품 해당하는것
# device = torch.device('mps:0' if torch.backends.mps.is_available() else 'cpu')
# print('device', device)

# print(f"PyTorch version:{torch.__version__}")  # 1.12.1 이상 True 여야 합니다.
# print(f"MPS 장치를 지원하도록 build 되었는지: {torch.backends.mps.is_built()}")
# print(f"MPS 장치가 사용 가능한지: {torch.backends.mps.is_available()}")  # True 여야 합니다.

# 엔비디아 GPU 사용하시는분은 요고 주석 풀고 device 사용
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# print(device)


class catvsdogDataset(Dataset):
    def __init__(self, image_file_path, transform=None):
        self.image_file_paths = glob.glob(
            os.path.join(image_file_path, "*", "*.jpg"))
        self.transform = transform

    def __getitem__(self, index):
        # image loader
        image_path = self.image_file_paths[index]
        image = cv2.imread(image_path)
        # converter BGR -> RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # label
        label_temp = image_path.split("\\")
        label_temp = label_temp[1]
        label = 0
        if "cat" == label_temp:
            label = 0
        elif "dog" == label_temp:
            label = 1
        print(image_path, label)

        if self.transform is not None:
            image = self.transform(image=image)["image"]

        return image, label

    def __len__(self):
        return len(self.image_file_paths)


# aug
train_transform = A.Compose([
    A.Resize(height=224, width=224),
    A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=1.0),
    ToTensorV2()
])

val_transform = A.Compose([
    A.Resize(height=224, width=224),
    ToTensorV2()
])

# dataset
train_dataset = catvsdogDataset("./2022.12/12.16_d53_image/data/dataset/train/", transform=None)
val_dataset = catvsdogDataset("./2022.12/12.16_d53_image/data/dataset/val/", transform=None)


# visualize augmentation
def visualize_augmentation(dataset, idx=0, samples=10, cols=5):
    dataset = copy.deepcopy(dataset)
    dataset.transform = A.Compose([
        t for t in dataset.transform if not isinstance(t, (ToTensorV2))])
    rows = samples // cols
    figure, ax = plt.subplots(nrows=rows, ncols=cols, figsize=(12, 6))
    for i in range(samples):
        image, _ = dataset[idx]
        ax.ravel()[i].imshow(image)
        ax.ravel()[i].set_axis_off()
    plt.tight_layout()
    plt.show()

visualize_augmentation(train_dataset)
