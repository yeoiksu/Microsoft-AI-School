import numpy as np
import cv2
import matplotlib.pyplot as plt

image_path = "./2022.12/12.07_d46_image/data/billiards.jpg"
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

_, mask = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY_INV)
kernel = []
for i in [cv2.MORPH_RECT, cv2.MORPH_CROSS, cv2.MORPH_ELLIPSE]:
    kernel.append(cv2.getStructuringElement(i, (11, 11)))

## Erosion example
title = ['Rectangle', 'Cross', 'Ellipse']

plt.figure(figsize = (11, 11))
plt.subplot(2, 2, 1)
plt.imshow(mask, 'gray')
plt.title('Original')
for i in range(3):
    erosion = cv2.erode(mask, kernel[i])
    plt.subplot(2, 2, i + 2)
    plt.imshow(erosion, 'gray')
    plt.title(title[i])
    plt.axis('off')

# plt.tight_layout()
plt.show()
