import cv2
import numpy as np

large_img = cv2.imread("./2022.12/12.08_d47_image/data/1.png")
watermark = cv2.imread("./2022.12/12.08_d47_image/data/2.png")

small_img = cv2.resize(watermark, (300,300))

x_offset = 30
y_offset = 170

x_end = x_offset + small_img.shape[0]
y_end = y_offset + small_img.shape[1]

large_img[y_offset:y_end, x_offset:x_end] = small_img
cv2.imshow("test", large_img)
cv2.waitKey(0)