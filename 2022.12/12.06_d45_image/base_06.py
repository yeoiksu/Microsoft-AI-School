### 세피아 효과 필터
import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import image_show

image_path = "./2022.12/12.06_d45_image/data/car.jpg"
image = cv2.imread(image_path)

filter = np.array([[0.272, 0.534, 0.131],
                [0.349, 0.686, 0.168],
                [0.393, 0.769, 0.189]])

sepia_img = cv2.transform(image, filter)
image_show(sepia_img)
