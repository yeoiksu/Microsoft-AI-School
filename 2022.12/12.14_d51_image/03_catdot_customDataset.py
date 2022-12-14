"""
    - train
        -cat
            -cat1.jpg ...
        -dog
    - val
        -cat
        -dog
    - test
        -cat
        -dog
"""
import os
import glob
from PIL import Image
from torch.utils.data.dataset import Dataset
label_dict = {"cat":0, "dog": 1}

class cat_dog_mycustomdataset(Dataset):
    def __init__(self, data_path):
        # data_path -> ./dataset/train      1
        # train     -> ./dataset/train
        # test      -> ./dataset/test
        # val       -> ./dataset/val

        # csv folder 읽기, 변환 할당, 데이터 필터링 등 과 같은 초기 논리가 발생
        self.all_data_path = glob.glob( os.path.join(data_path, '*', '*.jpg') )

    def __getitem__(self, index):
        # 데이터 레이블 반환 image, label
        image_path = self.all_data_path[index]
        # print(index, image_path)
        img = Image.open(image_path).convert("RGB")
        # label_temp = image_path.split('/') # -> ['.', '2022.12', '12.13_d50_image', 'data', 'image', 'dataset', 'train\\cat\\cat.1.jpg']
        label_temp = image_path.split("\\")  # -> ['./2022.12/12.13_d50_image/data/image/dataset/train', 'cat', 'cat.1.jpg']
        label = label_dict[label_temp[1]]
        return img, label

    def __len__(self):
        # 전체 데이터 길이 반환
        return len(self.all_data_path)

image_path = "./2022.12/12.13_d50_image/data/image/dataset/train/"
test = cat_dog_mycustomdataset(image_path)

for i in test:
    print(i)
    pass

