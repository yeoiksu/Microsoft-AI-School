# 같은 크기의 이미지 블렌딩 실험
import cv2
import matplotlib.pyplot as plt
import numpy as np

large_img = cv2.imread("./2022.12/12.08_d47_image/data/1.png")
watermark = cv2.imread("./2022.12/12.08_d47_image/data/2.png")

# print("Large Image Size: ", large_img.shape)
# print("Watermark Image Size: ", watermark.shape)
"""
Large Image Size:  (683, 1024, 3)
Watermark Image Size:  (480, 640, 3)
"""

img1 = cv2.resize(large_img, (800,600) ) 
img2 = cv2.resize(watermark, (800,600) )

# print("Image 1 Resize: ", img1.shape)
# print("Image 2 Resize: ", img2.shape)
"""
Image 1 Resize:  (600, 800, 3)
Image 2 Resize:  (600, 800, 3)
"""

## 혼합 진행
blended = cv2.addWeighted(img1, 0.8, img2, 0.2, 0)  
# img1은 0.9만큼, img2 0.1만큼 진하게

# 1로 설정 
# blended = cv2.addWeighted(img1, 1, img2, 1, 0)

cv2.imshow("Image Large", blended)
cv2.waitKey(0)
