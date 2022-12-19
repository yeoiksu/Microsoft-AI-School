import cv2
import os
import glob
from torch.utils.data import Dataset

fruit_dict = {
    'banana'    : 0, 
    'kiwi'      : 1,
    'orange'    : 2,
    'pineapple' : 3,
    'watermelon': 4,
    }

class custom_dataset(Dataset):
    def __init__(self, path, transform=None):
        """
        data
            train
                라벨 폴더명 
                    이미지

        "./data/train"
        """
        self.paths = glob.glob(os.path.join(path, "*", "*.png"))
        self.transform = transform

    def __getitem__(self, index):
        # image loader
        image_path = self.paths[index]
        image = cv2.imread(image_path)
        
        # cv2 -> BGR -> RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # label
        label_list = image_path.split("\\")  # ['./2022.12/12.19_d54_data/data/train', 'banana', 'banana_0.png']
        label_temp = label_list[-2]
        label = fruit_dict[label_temp]

        if self.transform is not None:
            image = self.transform(image= image)["image"]
        image = image.float()
        return image, label
        
    def __len__(self):
        return len(self.paths)

if __name__ == '__main__':
    file_path = "./2022.12/12.19_d54_data/data/train"
    test = custom_dataset(file_path, transform= None)
    for i in test:
        pass