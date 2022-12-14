import os
import pandas as pd
import glob
from torch.utils.data.dataset import Dataset

class MyCustomDataset(Dataset):
    def __init__(self, path):
        self.all_data_path = glob.glob(os.path.join(path, '*.csv') )  
        # ['./2022.12/12.13_d50_image\\bbox_data.csv']
        csv_path = self.all_data_path[0]  
        # ./2022.12/12.13_d50_image\bbox_data.csv
        df = pd.read_csv(csv_path)
        # print(df)
        # exit()
        self.file_name = df.iloc[: , 1].values # ['banana_0.jpg' 'banana_1.jpg' ...]
        self.x_list = df.iloc[: , 2].values  # [ 18.89  74.51 ...]
        self.y_list = df.iloc[: , 3].values  # [ 16.8   24.87 ...]
        self.w_list = df.iloc[: , 4].values  # [236.2  612.25 ...]
        self.h_list = df.iloc[: , 5].values  # [135.87 793.09 ...]

    def __getitem__(self, index):
        image_name = self.file_name[index]
        x = self.x_list[index]
        y = self.y_list[index]
        w = self.w_list[index]
        h = self.h_list[index]
        return image_name, x, y, w, h

    def __len__(self):
        return len(self.all_data_path)

data = MyCustomDataset("./2022.12/12.13_d50_image/")
for item in data:
    print(item)
