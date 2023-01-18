import torch    
import torch.nn as nn
import matplotlib.pyplot as plt
import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2
from torch.utils.data import DataLoader
from ex03_customdataset import CustomDataset
import pandas as pd
from torchvision import models
from ex04_main import FIX
import numpy as np
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def test_main():
    test_aug = A.Compose([
        A.SmallestMaxSize(max_size= 224),
        A.CenterCrop(width= 200, height= 200),
        A.Normalize(mean=(0.485, 0.456, 0.406), std= (0.229, 0.224, 0.225)),
        ToTensorV2()
    ])

    test_dataset = CustomDataset("./0111/dataset/test" , transform= test_aug)
    test_loader  = DataLoader(test_dataset, batch_size= 1, shuffle= False, num_workers= 2, pin_memory= True)

    ###### 수정해야 할 부분 !!!!!!!!!!!!!!!!!!!
    model = models.mobilenet_v2(pretrained= False)
    model.classifier[1] = nn.Linear(in_features=1280, out_features= 2)
    model.load_state_dict(torch.load(f"./0111/12nd.pt", map_location=device))
    model.to(device)

    # model = models.__dict__["resnet50"](pretrained= False)
    # model.fc = nn.Linear(in_features= 2048, out_features= 2)
    # model.load_state_dict(torch.load(f"./0111/best{str(FIX)}.pt", map_location=device))
    # model.to(device)

    test(model, test_loader, device)

def acc_function(correct, total) :
    acc = correct / total * 100
    return acc

def test(model, data_loader, device) :
    model.eval()
    correct = 0
    total = 0
    y_pred, y_true = [], []
    with torch.no_grad():
        for i, (image, label) in enumerate(data_loader) :
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
        print(f"acc >> {acc}%" )

    # Build confusion matrix
    classes = ('bird', 'drone')
    cf_matrix = confusion_matrix(y_true, y_pred)
    df_cm = pd.DataFrame(cf_matrix, index = [i for i in classes],    
                        columns = [i for i in classes])
    plt.figure(figsize = (12,7))
    sn.heatmap(df_cm, annot=True)
    plt.savefig('./0111/confunsion_matrix.png')    

if __name__ == '__main__':
    test_main()