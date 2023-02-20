import os
import os.path as osp
import glob
import shutil

image_path = "C:/Users/user/Documents/DATASET/HELICOPTER"
new_img_path = osp.join(image_path, "images")
new_txt_path = osp.join(image_path, "labels")

os.makedirs(new_img_path, exist_ok= True)
os.makedirs(new_txt_path, exist_ok= True)

img_paths = glob.glob(osp.join(image_path, "*.png"))
txt_paths = glob.glob(osp.join(image_path, "*.txt"))


for index, img_path in enumerate(img_paths):
    img_name = osp.basename(img_path)
    txt_name = img_name.replace(".png", ".txt")
    
    shutil.move(img_path, osp.join(new_img_path, img_name))
    shutil.move(txt_paths[index], osp.join(new_txt_path, txt_name))
