### 기본적인 이미지 처리 기술을 이용한 이미지 선명화 
import cv2
import numpy as np

image_path = "./2022.12/12.06_d45_image/data/car.jpg"
img = cv2.imread(image_path, 0)
img_resize = cv2.resize(img, (320,240))

print(img.shape)

blurred_1 = np.hstack([
    cv2.blur(img_resize, (3,3)),
    cv2.blur(img_resize, (7,7)),
    cv2.blur(img_resize, (11,11))
])

cv2.imshow("show", blurred_1)
cv2.waitKey(0)

