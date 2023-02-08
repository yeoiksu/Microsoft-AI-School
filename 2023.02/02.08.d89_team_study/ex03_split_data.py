from sklearn.model_selection import train_test_split
import os
import glob
import cv2
import shutil
import copy

# 데이터 나누기
# train 80 val 20 test 0


total_image_path = "./total_images"
total_label_path = "./total_labels"

train_image_list = []
train_label_list = []
valid_image_list = []
valid_label_list = []


# 이미지 경로 -> list
for path in os.listdir(total_image_path) :
    path_name = os.path.join(total_image_path, path)
    images = glob.glob(os.path.join(path_name, "*.png"))
# print(images)
for path in os.listdir(total_label_path) :
    path_name = os.path.join(total_label_path, path)
    texts = glob.glob(os.path.join(total_label_path, "*.txt"))
# print(texts)
    train_image, val_image = train_test_split(images, test_size= 0.2, random_state=777)
    train_image_list += train_image
    # print(train_image_list)

# val_image, test_image  = train_test_split(val_image, test_size= 0.5, random_state=777)
train_texts, val_texts = train_test_split(texts, test_size= 0.2, random_state=777)
# val_texts, test_texts  = train_test_split(val_texts, test_size= 0.5, random_state=777)
# print(train_image, val_image, train_texts, val_texts)


for i in train_image:
    file_name = os.path.basename(i)
    os.makedirs("./dataset/train/images", exist_ok=True)
    shutil.copy2(i, f"./dataset/train/images/{file_name}")

for i in val_image:
    file_name = os.path.basename(i)
    os.makedirs("./dataset/valid/images", exist_ok=True)
    shutil.copy2(i, f"./dataset/valid/images/{file_name}")

# for i in test_image:
#     file_name = os.path.basename(i)
#     os.makedirs("./dataset/test/images", exist_ok=True)
#     shutil.copy2(i, f"./dataset/test/images/{file_name}")

for i in train_texts:
    file_name = os.path.basename(i)
    os.makedirs("./dataset/train/labels", exist_ok=True)
    shutil.copy2(i, f"./dataset/train/labels/{file_name}")

for i in val_texts:
    file_name = os.path.basename(i)
    os.makedirs("./dataset/valid/labels", exist_ok=True)
    shutil.copy2(i, f"./dataset/valid/labels/{file_name}")

# for i in test_texts:
#     file_name = os.path.basename(i)
#     os.makedirs("./dataset/test/labels", exist_ok=True)
#     shutil.copy2(i, f"./dataset/test/labels/{file_name}")