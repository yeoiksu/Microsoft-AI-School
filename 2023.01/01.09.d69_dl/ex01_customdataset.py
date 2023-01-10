from torch.utils.data import Dataset
import os
import glob
import cv2

class CustomDataset(Dataset) :
    def __init__(self, path , transform=None):
        self.all_path = glob.glob(os.path.join(path, "*", "*.jpg"))
        self.transform = transform

        self.label_dict = {}
        for index , (category) in enumerate(sorted(os.listdir(path))) :
            self.label_dict[category] = int(index)

    def __getitem__(self, item):
        # 1. image
        image_file_path = self.all_path[item]
        image = cv2.imread(image_file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 2. class label
        label_key = image_file_path.split("\\")[1]
        label = self.label_dict[label_key]

        # 3. Applying transforms on image
        if self.transform is not None :
            image = self.transform(image=image)["image"]

        # 4. return image, label
        return image, label

    def __len__(self):
        return len(self.all_path)


# test = CustomDataset("./2023.01/01.06.d68_dl/dataset/train" , transform=None)
# for i in test :
#     print(i)