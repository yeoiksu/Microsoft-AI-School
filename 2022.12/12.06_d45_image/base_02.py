### 가우시안 필터
import cv2
import numpy as np
from utils import image_show

image_path = "./2022.12/12.06_d45_image/data/car.jpg"
img = cv2.imread(image_path, 0)

image_resize = cv2.resize(img, (320,240))

Gaussian_bluured_1 = np.hstack([
    cv2.GaussianBlur(image_resize, (3,3), 0),
    cv2.GaussianBlur(image_resize, (7,7), 0),
    cv2.GaussianBlur(image_resize, (11,11), 0),
])
image_show(Gaussian_bluured_1)

image_name = "./2022.12/12.06_d45_image/data/gaussian_blur.png"
cv2.imwrite(image_name, Gaussian_bluured_1)


