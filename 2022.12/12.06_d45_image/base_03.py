import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import image_show

image_path = "./2022.12/12.06_d45_image/data/car.jpg"
image = cv2.imread(image_path)

# creating out sharpening filter
filter = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])

sharpen_img = cv2.filter2D(image, -1, filter)
cv2.imshow("Original Image", image)
cv2.waitKey(0)

image_show(sharpen_img)