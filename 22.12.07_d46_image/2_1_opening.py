'''
opening : erosion -> dilation (to delete dot noise)
'''
import numpy as np
import cv2
import matplotlib.pyplot as plt

image_path = "./22.12.07_d46_image/data/billiards.jpg"
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
_, mask = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY_INV)

# datatype : int, float
kernel = np.ones((3, 3), np.uint8)

N = 5
idx = 1
plt.figure(figsize=(15, 15))
for i in range(1, N + 1):
    erosion = cv2.erode(mask, kernel, iterations=i)
    opening = cv2.dilate(erosion, kernel, iterations=i)
    f_opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=i)

    plt.subplot(N, 2, idx)
    idx += 1
    plt.imshow(opening, 'gray')
    plt.title(f'{i} manual opening')

    plt.subplot(N, 2, idx)
    plt.imshow(f_opening, 'gray')
    plt.title(f'{i} function opening')
    idx += 1
# plt.tight_layout()
plt.show()
