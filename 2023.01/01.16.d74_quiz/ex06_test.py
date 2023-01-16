import os
import cv2
import glob
import torch    
import torch.nn as nn
import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2
from torch.utils.data import DataLoader
from ex04_customdataset import CustomDataset
from torchvision import models
# from ex05_main import model_try
from sklearn.metrics import confusion_matrix
import numpy as np
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

model_num = 1
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def test_main():
    test_aug = A.Compose([
        A.CenterCrop(width= 200, height= 200),
        A.Normalize(mean=(0.485, 0.456, 0.406), std= (0.229, 0.224, 0.225)),
        ToTensorV2()
    ])
    test_data_path = "./0116/dataset/test"
    test_dataset = CustomDataset(test_data_path, transform= test_aug)
    test_loader  = DataLoader(test_dataset, batch_size= 1, shuffle= False, num_workers= 2, pin_memory= True)

    ###### 모델에 따라 수정 필요 !!!!
    model = models.__dict__["resnet50"](pretrained= True)
    model.fc = nn.Linear(in_features = 2048, out_features = 6)
    model.load_state_dict(torch.load(f'./0116/best_{str(model_num)}.pt', map_location=device))
    model.to(device)

    test(model, test_loader, device)  # 테스트 진행할때 실행 : 정확도 출력
    # test_show(test_loader, device)    # 틀린 label 이미지 확인하고 싶을 때 진행 : 사진 비교

def acc_function(correct, total) :
    acc = correct / total * 100
    return acc

def test(model, data_loader, device) :
    model.eval()
    correct = 0
    total = 0
    y_pred, y_true = [], []
    test_data_path = "./0116/dataset/test"
    with torch.no_grad():
        for i, (image, label, path) in enumerate(data_loader) :
            images, labels = image.to(device), label.to(device)
            output = model(images)
            _, argmax = torch.max(output, 1)
            total += images.size(0)
            correct += (labels == argmax).sum().item()

            argmax = argmax.data.cpu().numpy()  # gpu에 할당된 tensor를 cpu 텐서로 변환
            labels = labels.data.cpu().numpy()  # gpu에 할당된 tensor를 cpu 텐서로 변환

            y_pred.extend(argmax) # Save Prediction
            y_true.extend(labels) # Save True

        acc = acc_function(correct, total)
        print(f"Model Accuracy: {acc}%" )      

    # Build confusion matrix
    classes = ('20F', '20M', '30F', '30M', '40F', '40M')
    cf_matrix = confusion_matrix(y_true, y_pred)
    df_cm = pd.DataFrame(cf_matrix/np.sum(cf_matrix) * len(os.listdir(test_data_path)), 
                    index = [i for i in classes], columns = [i for i in classes])
    plt.figure(figsize = (12,7))
    sn.heatmap(df_cm, annot=True)
    plt.savefig('./0116/confunsion_matrix.png')    

def test_show(test_loader, device) :
    model = models.__dict__["resnet50"](pretrained= True)
    model.fc = nn.Linear(in_features = 2048, out_features = 6)
    model.load_state_dict(torch.load(f'./0116/best_{model_num}.pt', map_location=device)) # 경로 수정 필요
    model.to(device)

    test_data_path = "./0116/dataset/test"
    label_dict = folder_name_det(test_data_path)

    print('\n============================ Test Show ============================')
    model.eval()
    with torch.no_grad():
        for i, (imgs, labels, path) in enumerate(test_loader) :
            inputs, outputs, paths = imgs.to(device), labels.to(device), path     

            predicted_outputs = model(inputs)            
            _, predicted = torch.max(predicted_outputs, 1) # 제일 확률 높은 답안지 내놔라

            labels_temp = labels.item()
            labels_pr_temp = predicted.item()

            predicted_label = label_dict[str(labels_pr_temp)]
            answer_label = label_dict[str(labels_temp)]

            if(answer_label != predicted_label):  # label과 predicted output이 다를 경우멘 사진출력
                print("Answer Label\t:" , answer_label)
                print("Predicted Label\t:", predicted_label)
                print('Name of Image\t:', paths[0].split('\\')[2], '\n')

                img = cv2.imread(paths[0])
                cv2.putText(img, predicted_label, (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 2) # 예상 답안 : 초록색
                cv2.putText(img, answer_label, (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)    # 실제 답안 : 빨간색
                cv2.imshow("test", img)
                cv2.waitKey(0)

def folder_name_det(folder_path) :
    folder_name = glob.glob(os.path.join(folder_path,"*"))
    det = {}
    for index, (path) in enumerate(folder_name) :
        temp_name = path.split("\\")
        temp_name = temp_name[1]
        det[str(index)] = temp_name
    return det     

def draw_confunsion(test_loader, model):
    print("Drawing Confusion Matrix...")
    y_pred, y_true = [], []

    for imgs, labels, path in test_loader:
        inputs, outputs, paths = imgs.to(device), labels.to(device), path  

        predicted_outputs = model(inputs)            
        _, predicted = torch.max(predicted_outputs, 1) # 제일 확률 높은 답안지 내놔라
        y_pred.extend(predicted) # Save Prediction
        labels = labels.data.cpu().numpy()
        y_true.extend(labels) # Save True

    classes = ('20F', '20M', '30F', '30M', '40F', '40M')

    # Build confusion matrix
    cf_matrix = confusion_matrix(y_true, y_pred)
    df_cm = pd.DataFrame(cf_matrix/np.sum(cf_matrix) *10, index = [i for i in classes],
                        columns = [i for i in classes])
    plt.figure(figsize = (12,7))
    sn.heatmap(df_cm, annot=True)
    plt.savefig('./0116/output.png')
                    
if __name__ == '__main__':
    test_main()