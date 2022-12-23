import torch
from torchvision import models
from torch.utils.data import DataLoader
import albumentations as A
from albumentations.pytorch import ToTensorV2

from dataset_temp import CustomDataset

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
        print("\n\nacc for {} image : {:.2f}%\n\n".format(total, acc))

def main():

    # test_transform = A.Compose([
    #     A.Resize(height=224, width=224),
    #     ToTensorV2()
    # ])

    test_transform = A.Compose([
        A.Resize(height=224, width=224),
        A.HorizontalFlip(p= 0.5),
        A.VerticalFlip(p= 0.5),
        A.RandomBrightnessContrast(p= 0.2),
        ToTensorV2()
    ])    

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net = models.__dict__["resnet18"](pretrained=False, num_classes = 5)
    net = net.to(device)
    net.load_state_dict(torch.load("./2022.12/12.22_d57_data/model_save/final.pt", map_location= device))

    test_dataset = CustomDataset("./2022.12/12.19_d54_data/data/val", transform= test_transform)
    test_loader = DataLoader(test_dataset, batch_size= 1, shuffle= False)
    test(net, test_loader, device)

if __name__ == '__main__':
    main()



    

    


            