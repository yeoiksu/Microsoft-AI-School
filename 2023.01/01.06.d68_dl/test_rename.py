from PIL import Image # pip install Pillow
import os
import cv2
import glob

image_list = glob.glob(os.path.join("./2023.01/01.06.d68_dl/testset", "*",'*.jpg'))

os.makedirs("./2023.01/01.06.d68_dl/test/r", exist_ok= True)
os.makedirs("./2023.01/01.06.d68_dl/test/s", exist_ok= True)
os.makedirs("./2023.01/01.06.d68_dl/test/p", exist_ok= True)

for image_path in image_list:
    image = cv2.imread(image_path)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    new_path = image_path.replace('testset', 'test')
    new_path = new_path.replace('.jpg', '.png')
    cv2.imwrite(new_path, image)
    