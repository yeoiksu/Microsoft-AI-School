import cv2
from utils import image_show

# 이미지 경로
image_path = "./2022.12/12.06_d45_image/data/cat.jpg"
image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # 그레이 이미지 변경

image_10_by_10 = cv2.resize(image_gray, (10,10))
image_10_by_10.flatten()  # 이미지 데이터를 1차원 벡터로 변환
image_show(image_10_by_10)