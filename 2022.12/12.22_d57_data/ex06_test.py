import os
import torch
from torchvision import models
from torch.utils.data import DataLoader
import albumentations as A
from albumentations.pytorch import ToTensorV2
from glob import glob

from ex04_dataset_temp import CustomDataset
from utils import save_model

def test(model, test_loader, device):
    model.eval()

    correct = 0
    total = 0
    with torch.no_grad():
        for batch_index, (data, target) in enumerate(test_loader):
            data, target = data.to(device), target.to(device)  # target은 정답(라벨)
            output = model(data)                               # output은 모델이 예측한 값 
            _, argmax = torch.max(output, 1)
            
            total += target.size(0)  # 전체 사이즈
            correct += (target == argmax).sum().item()  # target과 output 비교
        
        acc = correct / total * 100
        print("acc for {} image : {:.2f}%".format(total, acc))

        return acc  

def main():
    test_transform = A.Compose([
        A.Resize(height=256, width=256),
        ToTensorV2()
    ])    

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = models.__dict__["resnet18"](pretrained=False, num_classes = 5)  # resmodel18 모델, num_classes 중요 !!!
    model = model.to(device)

    model_pt_paths = glob(os.path.join("./2022.12/12.22_d57_data/model_save", "*", "final.pt"))
    # ['./2022.12/12.22_d57_data/model_save\\transform0\\final.pt', 
    #                           ...
    # './2022.12/12.22_d57_data/model_save\\transform4\\final.pt']

    best_acc = 0  # accuracy of the best model (제일 처음에는 0으로 초기화)
    best_trans_name = "None"  # 제일 처음 초기화

    for pt_path in model_pt_paths:
        transform_name = pt_path.split("\\")[1]  # transform0
        
        model.load_state_dict(torch.load(pt_path, map_location= device))
        test_dataset = CustomDataset("./2022.12/12.19_d54_data/data/val", transform= test_transform)
        test_loader = DataLoader(test_dataset, batch_size= 1, shuffle= False)
        
        print(f"===== The Result of {transform_name} =====\n")
        new_acc = test(model, test_loader, device)

        if new_acc > best_acc:
            print(f"{transform_name}이 {best_trans_name}보다 정확도가 높습니다\n")
            save_model(
                model= model,
                save_dir= "./2022.12/12.22_d57_data/model_save",
                file_name= f"best.pt"
            )
            best_acc = new_acc
            best_trans_name = transform_name
        elif new_acc == best_acc:
            print(f"{transform_name}이 {best_trans_name}보다 정확도가 같습니다\n")
        else:
            print(f"{best_trans_name}의 정확도가 더 높습니다\n")
        
if __name__ == '__main__':
    main()



    

    


            