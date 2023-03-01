import os
import os.path as osp
import glob
import shutil

path = "C:\\Users\\user\\Documents\\05.valid\\balloon_1\\images"
new_path = "C:\\Users\\user\\Documents\\05.valid\\balloon_1\\test"
NUM = 4583
label_name = 'balloon'

image_paths = glob.glob(osp.join(path, "*.png"))

for index, image_path in enumerate(image_paths):
    new_image_name = f'{label_name}_{str(index+NUM)}.png'
    shutil.copy(image_path, osp.join(new_path, new_image_name))