from ex02_utilis import *
from PIL import Image,  ImageOps
from ex02_utilis import expand2square

train_path = "C://Users//user//Documents//datasets//train_image"
test_path  = "C://Users//user//Documents//datasets//test_image"
            
train_data = image_file(train_path)
test_data  = image_file(test_path)

print("train 길이\t:", len(train_data))
print("test 길이\t:", len(test_data))
"""
train 길이      : 569
test 길이       : 310
"""
# resize flag
train_image_resize = True
if train_image_resize == True:
    for idx in range(10):
        os.makedirs(f"./2022.12/12.28.d61_cnn/data/dataset/train/{idx}/", exist_ok= True)
    for i in train_data:
        # ['./2022.12/12.28.d61_cnn/data/dataset/train_image', '0', 'zero_00100.png']
        f_name = i.split("\\")[1]       # '0'
        f_name_temp = i.split("\\")[-1] # 'zero_00100.png'
        file_name = f_name_temp.split('.')[0]

        img = Image.open(i)
        img = ImageOps.exif_transpose(img)
        img_new = expand2square(img, (0,0,0)).resize((400,400))
        for num in range(10):
            if f_name == str(num):
                img_new.save(f"./2022.12/12.28.d61_cnn/data/dataset/train/{str(num)}/{file_name}.png")    

# resize flag
test_image_resize = True
if test_image_resize == True:
    for idx in range(10):
        os.makedirs(f"./2022.12/12.28.d61_cnn/data/dataset/test/{idx}/", exist_ok= True)
    for i in test_data:
        # ['./2022.12/12.28.d61_cnn/data/dataset/test_image', '0', 'zero_00100.png']
        f_name = i.split("\\")[1]       # '0'
        f_name_temp = i.split("\\")[-1] # 'zero_00100.png'
        file_name = f_name_temp.split('.')[0]

        img = Image.open(i)
        img = ImageOps.exif_transpose(img)
        img_new = expand2square(img, (0,0,0)).resize((400,400))
        for num in range(10):
            if f_name == str(num):
                img_new.save(f"./2022.12/12.28.d61_cnn/data/dataset/test/{str(num)}/{file_name}.png")    

