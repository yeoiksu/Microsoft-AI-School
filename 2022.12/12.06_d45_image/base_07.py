### 엠보싱 효과
import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import image_show

image_path = "./2022.12/12.06_d45_image/data/car.jpg"
image = cv2.imread(image_path)

filter1 = np.array([[0, 1, 0], [0, 0, 0], [0, -1, 0]])
emboss_img1 = cv2.filter2D(image, -1, filter1)
emboss_img1 += 128
image_show(emboss_img1)

filter2 = np.array([[-1, -1, 0], [-1, 0, 1], [0, 1, 1]])
emboss_img2 = cv2.filter2D(image, -1, filter2)
emboss_img2 += 128
image_show(emboss_img2)

