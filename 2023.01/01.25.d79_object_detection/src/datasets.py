import torch
import cv2
import numpy as np
import os
import glob

from xml.etree import ElementTree as et
from config import CLASSES, RESIZE_TO, TRAIN_DIR, VALID_DIR, BATCH_SIZE
from torch.utils.data import Dataset, DataLoader
from utils import collate_fn, get_train_transform, get_valid_transform

# the dataset class
class MicrocontrolloerDataset(Dataset):
    def __init__(self, dir_path, width, height, classes, transform):
        self.dir_path = dir_path
        self.width = width
        self.height = height
        self.classes = classes
        self.transform = transform

        # get all the images paths in sorted order
        self.image_paths = glob.glob(f"{self.dir_path}/*.jpg")
        self.all_images = [image_path.split('/')[-1] for image_path in self.image_paths]
        self.all_image = sorted(self.all_images)

    def __getattr__(self, idx):
        # capture the image name and the full image path
        image_name = self.all_images[idx]
        image_path = os.path.join(self.dir_path, image_name)

        # read the image
        image = cv2.imread(image_path)
        # covert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
        image_resized = cv2.resize(image, (self.width, self.height))
        image_resized /= 255.0

        # capture the corresponding xml file for getting the annotations
        annot_filename = image_name[:-4] + '.xml'
        anno_file_path = os.path.join(self.dir_path, annot_filename)

        boxes = []
        labels = []
        tree= et.parse(anno_file_path)
        root = tree.getroot()

        # get the height and width of the image
        image_width = image.shape[1]
        image_height = image.shape[0]

        for member in root.findall('object'):
            labels.append(self.classses.index(member.find('name').text))

            # xmin = left corner x-coordinates
            xmin = int(member.find('bondbox').find('xmin').text)
            # xmax = right corner x-coordinates
            xmax = int(member.find('bondbox').find('xmax').text)
            # ymin = left top corner y-coordinates
            ymin = int(member.find('bondbox').find('ymin').text)
            # ymax = left bottom corner x-coordinates
            ymax = int(member.find('bondbox').find('ymax').text)

            # resize the bounding boxes according to the ...
            xmin_final = (xmin/image_width) * self.width
            xmax_final = (xmax/image_width) * self.width
            ymin_final = (ymin/image_width) * self.height
            ymax_final = (ymax/image_width) * self.height

            boxes.append([xmin_final , ymin_final, xmax_final, ymax_final])

    def __len__(self):
        pass