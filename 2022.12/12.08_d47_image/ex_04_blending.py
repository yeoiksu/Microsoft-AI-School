import cv2
import numpy as np

large_img = cv2.imread("./2022.12/12.08_d47_image/data/1.png")
watermark = cv2.imread("./2022.12/12.08_d47_image/data/2.png")
small_img = cv2.resize(watermark, (300,300))

x_offset = 400
y_offset = 170

rows, columns, channels = small_img.shape
roi = large_img[y_offset:470, x_offset:700]

# logo image 빨간색 부분을 제외한 모든 것을 필토링 하도록 -> 회색조 이미지로 변경
small_img_gray = cv2.cvtColor(small_img, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(small_img_gray, 120, 255, cv2.THRESH_BINARY)
cv2.imshow("Mask", mask)
cv2.waitKey(0)

bg = cv2.bitwise_or(roi, roi, mask= mask)
mask_inv = cv2.bitwise_not(mask)
cv2.imshow("Mask Inversed", mask_inv)
cv2.waitKey(0)

fg = cv2.bitwise_and(small_img, small_img, mask= mask_inv)
cv2.imshow("Bitwise", fg)
cv2.waitKey(0)

final_roi = cv2.add(bg, fg)
cv2.imshow("ROI(Region Of Interest)", final_roi)
cv2.waitKey(0)