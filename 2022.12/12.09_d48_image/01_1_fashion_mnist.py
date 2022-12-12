import os
import cv2
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor

file_path = './2022.12/12.09_d48_image/data'

#### 1. 파일 다운로드
training_data = datasets.FashionMNIST(
    root= file_path,
    train= True,
    download= True,
    transform= ToTensor()
)

test_data = datasets.FashionMNIST(
    root= file_path,
    train= False,
    download= True,
    transform= ToTensor()
)

img_size = 28
num_images = 5

#### 2. 배열 형태를 이미지로 만들고 시각화
with open( file_path + '/FashionMNIST/raw/t10k-images-idx3-ubyte', 'rb') as f:
    a = f.read(16)  # 헤더 17byte부터 이미지 데이터
    buf = f.read(img_size*img_size*num_images)
    data = np.frombuffer(buf, dtype= np.uint8).astype(float)  # frombuffer : Binary 읽기
    data = data.reshape(num_images, img_size, img_size, 1)
    import matplotlib.pyplot as plt
    image = np.asarray(data[1]).squeeze()
    plt.imshow(image, cmap= 'gray')

#### 3. 라벨 파일 들고와서 이미지 인덱스에 해당하는 라벨 출력(0)
with open( file_path + '/FashionMNIST/raw/train-labels-idx1-ubyte', 'rb') as f:    
    buf = f.read(num_images)
    labels = np.frombuffer(buf, dtype= np.uint8).astype(np.uint64)
    print("Label 출력: ",labels[1])  # 라벨 0 출력

plt.title(f'{labels[1]}')
plt.show()

labels_map = {    
    0: "T-Shirt",
    1: "Trouser",
    2: "Pullover",
    3: "Dress",
    4: "Coat",
    5: "Sandal",
    6: "Shirt",
    7: "Sneaker",
    8: "Bag",
    9: "Ankle Boot",
}

#### 4. 데이터 확인 ( 3 x 3 )
figure =plt.figure(figsize= (8,8)) 
cols, rows = 3, 3
for i in range(1, cols*rows +1):
    sample_idx = torch.randint(len(training_data), size= (1,)).item()
    img, label = training_data[sample_idx]
    figure.add_subplot(rows,cols, i)
    plt.title(labels_map[label])
    plt.axis('off')
    plt.imshow(img.squeeze(), cmap= 'gray')
plt.show()

#### 5. 바이너리 파일 img와 label인 csv파일로 저장
## train csv 생성
imgf = open(file_path + '/FashionMNIST/raw/train-images-idx3-ubyte', 'rb')
imgd = imgf.read(16)
lblf = open(file_path + '/FashionMNIST/raw/train-labels-idx1-ubyte', 'rb')
lbuf = lblf.read(8)
df_dict_train = {
    'file_name' : [],
    'label' : []
}
idx = 0
# os.makedirs(file_path+'/FashionMNIST/images', exist_ok=True)  # 디렉토리 생성 
while True:
    imgd = imgf.read(img_size*img_size)
    if not imgd:
        break
    data = np.frombuffer(imgd, dtype = np.uint8).astype(float)
    data = data.reshape(1, img_size, img_size, 1)
    image = np.asarray(data).squeeze()
    lbld = lblf.read(1)
    labels = np.frombuffer(lbld, dtype= np.uint8).astype(np.int64)
    file_name = f'{idx}.png'
    cv2.imwrite(file_path +'/FashionMNIST/train/'+ file_name, image)
    
    idx+=1

    df_dict_train['label'].append(labels[0])
    df_dict_train['file_name'].append(file_name)

df_train = pd.DataFrame(df_dict_train)
print('Train dataframe 생성\n', df_train.head())
df_train.to_csv(file_path +'/FashionMNIST/annotation_train.csv')

## test csv 생성
imgf = open(file_path + '/FashionMNIST/raw/t10k-images-idx3-ubyte', 'rb')
imgd = imgf.read(16)
lblf = open(file_path + '/FashionMNIST/raw/t10k-labels-idx1-ubyte', 'rb')
lbuf = lblf.read(8)

df_dict_test = {
    'file_name' : [],
    'label' : []
}
idx = 0
# os.makedirs(file_path+'/FashionMNIST/images', exist_ok=True)  # 디렉토리 생성 
while True:
    imgd = imgf.read(img_size*img_size)
    if not imgd:
        break
    data = np.frombuffer(imgd, dtype = np.uint8).astype(float)
    data = data.reshape(1, img_size, img_size, 1)
    image = np.asarray(data).squeeze()
    lbld = lblf.read(1)
    labels = np.frombuffer(lbld, dtype= np.uint8).astype(np.int64)
    file_name = f'{idx}.png'
    cv2.imwrite(file_path +'/FashionMNIST/test/'+ file_name, image)
    idx+=1

    df_dict_test['label'].append(labels[0])
    df_dict_test['file_name'].append(file_name)

df_test = pd.DataFrame(df_dict_test)
df_test.to_csv(file_path +'/FashionMNIST/annotation_test.csv')
print('Test dataframe 생성\n', df_test.head())