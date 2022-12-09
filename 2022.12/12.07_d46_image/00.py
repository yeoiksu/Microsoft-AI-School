import numpy as np
import cv2
import matplotlib.pyplot as plt

image_path = "./2022.12/22.12.07_d46_image/data/billiards.jpg"
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
_, mask = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY_INV)