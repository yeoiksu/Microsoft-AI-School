# import cv2
import os
import os.path as osp
from glob import glob
from sklearn.model_selection import train_test_split
import shutil

root_path = "C:/Users/user/Documents/03.dataset/230206_dataset/10_kaggle"
select_new_path = "C:/Users/user/Documents/03.dataset/230206_dataset/selected"
remove_new_path = "C:/Users/user/Documents/03.dataset/230206_dataset/removed"

os.makedirs(select_new_path, exist_ok= True)
os.makedirs(remove_new_path, exist_ok= True)

image_paths = glob(osp.join(root_path, "*.jpg"))
selected_paths, remove_paths = train_test_split(image_paths, test_size= 0.2, random_state= 777)

for selected_path in selected_paths:
    image_name = selected_path.split('\\')[-1]
    shutil.copy(selected_path, osp.join(select_new_path, image_name))

for remove_path in remove_paths:
    image_name = remove_path.split('\\')[-1]
    shutil.copy(remove_path, osp.join(remove_new_path, image_name))
    

