import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = "./2022.12/12.06_d45_image/data/billiards.jpg"
image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # gray
_ , mask = cv2.threshold(image_gray, 230, 255, cv2.THRESH_BINARY_INV)

# 3x3 Kernel
kernel = np.ones((3,3), np.uint8)
print(kernel)

dilation = cv2.dilate(mask, kernel)

titles = ["image", "mask", "dilation"]
images = [image_gray, mask, dilation]

for i in range(3):
    plt.subplot(1, 3, i+1),
    plt.imshow(images[i], "gray"),
    plt.title(titles[i]),
    plt.xticks([]),
    plt.yticks([]),
plt.show()
