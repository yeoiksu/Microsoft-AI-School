'''
./2022.12/12.19_d54_data/data
    - train
        - banana
        - kiwi  
        - orange 
        - pineapple 
        - watermelon
    - val
        - banana
        - kiwi  
        - orange 
        - pineapple 
        - watermelon
'''
import os
import cv2
import glob
import shutil
from sklearn.model_selection import train_test_split

image_path = "./2022.12/12.19_d54_data/dataset/images"
RANDOM_SEED = 7777

# 데이터셋 크기가 크지 않으므로 testdata는 생성 X
for item in os.listdir(image_path): # [banana, kiwi, orange, pineapple, watermelon]
    data = glob.glob(os.path.join(image_path, item, '*.png'))
    train_data, val_data = train_test_split(data, test_size= 0.1, random_state= RANDOM_SEED)  # train val 9:1
    
    new_train_path = f"{image_path.replace('dataset/images', 'data/train')}/{item}" # ./dataset/images -> ./data/train/banana
    new_val_path   = f"{image_path.replace('dataset/images', 'data/val')}/{item}"   # ./dataset/images -> ./data/val/banana

    os.makedirs(new_train_path, exist_ok= True)  # create train folder
    os.makedirs(new_val_path, exist_ok= True)  # create val folder

    # train
    for i in train_data:
        file_name = os.path.basename(i)
        img = cv2.imread(i)  # ./2022.12/12.19_d54_data/data/train/banana/banana_xx.png
        cv2.imwrite(f"{new_train_path}/{file_name}", img)
    # validation
    for i in val_data:
        file_name = os.path.basename(i)
        img = cv2.imread(i)  # ./2022.12/12.19_d54_data/data/train/banana/banana_xx.png
        cv2.imwrite(f"{new_val_path}/{file_name}", img)