### Custom Filter
import cv2
import numpy as np
from utils import image_show

image_path = "./2022.12/12.06_d45_image/data/car.jpg"
image = cv2.imread(image_path)

filter = np.array(([3, -2, -3],[-4, 8, -6], [5, -1, -0]))
custom_image_filter = cv2.filter2D(image, -1, filter)

image_show(custom_image_filter)
