import os
import torch
from torchvision import models
from torch.utils.data import DataLoader
import albumentations as A
from albumentations.pytorch import ToTensorV2
from ex04_dataset_temp import CustomDataset
from glob import glob

def acc_function(correct, total):
    acc = correct / total * 100
    return acc

def test(model, test_loader, device):
    model.eval()

    correct = 0
    total = 0
    with torch.no_grad():
        for batch_index, (data, target) in enumerate(test_loader):
            data, target = data.to(device), target.to(device)
            output = model(data)
            _, argmax = torch.max(output, 1)
            
            total += target.size(0)
            correct += (target == argmax).sum().item()
        
        acc = acc_function(correct, total)
        print("\nacc for {} image : {:.2f}%".format(total, acc))

def main():
    test_transform = A.Compose([
        A.Resize(height=256, width=256),
        ToTensorV2()
    ])    

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net = models.__dict__["resnet18"](pretrained=False, num_classes = 5)  # resnet18 모델, num_classes 중요 !!!
    net = net.to(device)

    model_pt_paths = glob(os.path.join("./2022.12/12.22_d57_data/model_save", "*", "final.pt"))
    # ['./2022.12/12.22_d57_data/model_save\\transform0\\final.pt', 
    #                           ...
    # './2022.12/12.22_d57_data/model_save\\transform4\\final.pt']

    for pt_path in model_pt_paths:
        transform_name = pt_path.split("\\")[1]  # transform0
        
        net.load_state_dict(torch.load(pt_path, map_location= device))
        test_dataset = CustomDataset("./2022.12/12.19_d54_data/data/val", transform= test_transform)
        test_loader = DataLoader(test_dataset, batch_size= 1, shuffle= False)
        
        print(f"\n===== The Result of {transform_name} =====")
        test(net, test_loader, device)

if __name__ == '__main__':
    main()



    

    


            