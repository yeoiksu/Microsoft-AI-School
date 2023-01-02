import os
import torch
import argparse
import torch.optim
import torch.nn as nn
import torchvision.models as models
from torch.utils.data import DataLoader
import torch.optim as optim

import albumentations as A
from albumentations.pytorch import ToTensorV2

from timm.loss import LabelSmoothingCrossEntropy
from adamp import AdamP
from ex01_custom_dataset import CustomDataset
from ex03_utils import train, test_species, test_show


def main(opt):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # augmentation
    train_transform = A.Compose([
        A.SmallestMaxSize(max_size=160),
        A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.05, rotate_limit=15, p=0.8),
        A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=0.7),
        A.RandomBrightnessContrast(p=0.5),
        A.RandomShadow(p=0.5),
        A.RandomFog(p=0.4),
        A.RandomShadow(p=0.3),
        A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ToTensorV2()
    ])
    val_transform = A.Compose([
        A.SmallestMaxSize(max_size=160),
        A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ToTensorV2()
    ])
    # dataset
    train_dataset = CustomDataset(file_path= opt.train_path, transform= train_transform)
    valid_dataset = CustomDataset(file_path= opt.val_path  , transform= val_transform)
    test_dataset  = CustomDataset(file_path= opt.test_path , transform= val_transform)

    # dataloader
    train_loader = DataLoader(train_dataset, batch_size= opt.batch_size, shuffle= True)
    valid_loader = DataLoader(valid_dataset, batch_size= opt.batch_size, shuffle= False)
    test_loader  = DataLoader(test_dataset, batch_size= 1, shuffle= False)

    # model call
    # train -> label -> 53
    net = models.__dict__["resnet50"](pretrained= True)
    num_ftrs = net.fc.in_features 
    net.fc = nn.Linear(num_ftrs, 53)  # output 수정
    net.to(device)

    # loss
    criterion= LabelSmoothingCrossEntropy().to(device)

    # optimizer
    optimizer = AdamP(net.parameters(), lr= opt.lr, weight_decay= 1e-2)

    # scheduler
    scheduler = optim.lr_scheduler.MultiStepLR(optimizer, 
                                            milestones=[60, 90], gamma=0.1)
    # scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.1)

    # model .pt save dir
    save_dir = opt.save_path
    os.makedirs(save_dir, exist_ok=True)

    # train
    train_flg = opt.train_flag
    if train_flg == True:
        train(opt.epoch, net, train_loader, valid_loader, criterion, optimizer, scheduler, save_dir, device)
    else:
        # test_species(test_loader, device)
        test_show(test_loader, device)

def parse_opt() :
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-path", type=str, default= "C:\\dataset\\train", 
                        help="train data path")
    parser.add_argument("--val-path" ,type=str, default= "C:\\dataset\\valid", 
                        help="val data path")
    parser.add_argument("--test-path" ,type=str, default= "C:\\dataset\\test", 
                        help="test data path")
    parser.add_argument("--save-path", type=str, default="C:\\dataset\\weights",
                        help="save mode path")
    parser.add_argument("--batch-size", type=int, default=32,
                        help="batch size")                    
    parser.add_argument("--train-flag", type=bool, default=False,
                        help="train or test mode flag")
    parser.add_argument("--epoch", type=int, default=100,
                        help="epoch number")
    parser.add_argument("--lr" , type=float, default=0.001,
                        help="lr number")
    opt = parser.parse_args()
    return opt

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
