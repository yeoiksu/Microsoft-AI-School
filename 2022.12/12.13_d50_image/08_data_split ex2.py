## image data get -> train 80, val 10, test 10
import os
import natsort
import glob
import cv2
from sklearn.model_selection import train_test_split

cat_image_path = "./2022.12/12.13_d50_image/data/image/cats"
dog_image_path = "./2022.12/12.13_d50_image/data/image/dogs"

#### 1. 정렬
cat_image_full_path = natsort.natsorted(
    glob.glob(os.path.join(f"{cat_image_path}/*.jpg")))
print("cat image size : " , len(cat_image_full_path))

dog_image_full_path = natsort.natsorted(
    glob.glob(os.path.join(f"{dog_image_path}/*.jpg")))
print("dog image size : " , len(dog_image_full_path))

#### 2. cat train 80, val 20 -> val 10 , test 10
random_seed = 7777
cat_train_data, cat_val_data = train_test_split(
    cat_image_full_path, test_size = 0.2, random_state = 7777)
cat_val, cat_test = train_test_split(
    cat_val_data, test_size=0.5, random_state = 7777)

print(f"cat train data : {len(cat_train_data)}, cat val data : {len(cat_val)}, cat test data : {len(cat_test)}")

#### 3. dog train 80, val 20 -> val 10 , test 10
dog_train_data, dog_val_data = train_test_split(
    dog_image_full_path, test_size = 0.2, random_state = 7777)
dog_val, dog_test = train_test_split(
    dog_val_data, test_size = 0.5, random_state = 7777)

print(f"dog train data : {len(dog_train_data)}, dog val data : {len(dog_val)}, dog test data : {len(dog_test)}")

#### 4. image cv2 imard -> 저장하는 방법
#### mv copy

#### 4.1. cat train
for cat_train_data_path in cat_train_data:
    # print(cat_train_data_path)
    img = cv2.imread(cat_train_data_path)
    os.makedirs("./2022.12/12.13_d50_image/data/image/dataset/train/cat/", exist_ok= True)
    file_name = os.path.basename(cat_train_data_path)
    cv2.imwrite(f"./2022.12/12.13_d50_image/data/image/dataset/train/cat/{file_name}", img)

#### 4.2. cat val, test
for cat_val_path, cat_test_path in zip(cat_val, cat_test):
    img_val  = cv2.imread(cat_val_path)
    img_test = cv2.imread(cat_test_path)    
    os.makedirs("./2022.12/12.13_d50_image/data/image/dataset/val/cat/", exist_ok= True)
    os.makedirs("./2022.12/12.13_d50_image/data/image/dataset/test/cat/", exist_ok= True)
    file_name_val  = os.path.basename(cat_val_path)
    file_name_test = os.path.basename(cat_test_path)    
    cv2.imwrite(f"./2022.12/12.13_d50_image/data/image/dataset/val/cat/{file_name_val}", img_val)
    cv2.imwrite(f"./2022.12/12.13_d50_image/data/image/dataset/test/cat/{file_name_test}", img_test)
    
#### 4.3. dog_train
for dog_train_data_path in dog_train_data:
    # print(cat_train_data_path)
    img = cv2.imread(dog_train_data_path)
    os.makedirs("./2022.12/12.13_d50_image/data/image/dataset/train/dog/", exist_ok= True)
    file_name = os.path.basename(dog_train_data_path)
    cv2.imwrite(f"./2022.12/12.13_d50_image/data/image/dataset/train/dog/{file_name}", img)

#### 4.4. dog val, test
for dog_val_path, dog_test_path in zip(dog_val, dog_test):
    img_val  = cv2.imread(dog_val_path)
    img_test = cv2.imread(dog_test_path)    
    os.makedirs("./2022.12/12.13_d50_image/data/image/dataset/val/dog/", exist_ok= True)
    os.makedirs("./2022.12/12.13_d50_image/data/image/dataset/test/dog/", exist_ok= True)
    file_name_val  = os.path.basename(dog_val_path)
    file_name_test = os.path.basename(dog_test_path)  
    cv2.imwrite(f"./2022.12/12.13_d50_image/data/image/dataset/val/dog/{file_name_val}", img_val)
    cv2.imwrite(f"./2022.12/12.13_d50_image/data/image/dataset/test/dog/{file_name_test}", img_test)  