import cv2
from utils import image_show

# 이미지 경로
image_path = "./2022.12/12.06_d45_image/data/cat.jpg"
image = cv2.imread(image_path)

# 10 x 10 변환
image_color_10_by_10 = cv2.resize(image, (10,10))
image_color_10_by_10.flatten()
image_show(image_color_10_by_10)

# 225 x 255 변환
image_color_225_by_255 = cv2.resize(image, (225,255))
image_color_225_by_255.flatten()
image_show(image_color_225_by_255)