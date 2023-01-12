import os
import sys
import torch    
import torch.nn as nn
import copy
import matplotlib.pyplot as plt
import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2
from torch.utils.data import DataLoader
from ex03_customdataset import CustomDataset
import pandas as pd
from tqdm import tqdm
from torchvision import models
from timm.loss import LabelSmoothingCrossEntropy
from ex04_main import FIX

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.mobilenet_v2(pretrained= False)
model.classifier[1] = nn.Linear(in_features=1280, out_features= 2)
model.load_state_dict(torch.load("./2023.01/01.12.d72_dl/12nd.pt", map_location= device))
model.to(device)