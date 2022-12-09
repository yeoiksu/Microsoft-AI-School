#### 이미지 blur처리
#### filter 2d() 메소드 사용
import cv2
import numpy as np
from utils import image_show

# 이미지 경로
image_path = "./2022.12/12.06_d45_image/data/cat.jpg"

# 이미지 읽기 처리
image = cv2.imread(image_path)
# print(image)

# 커널 생성 처리
kernel = np.ones((10, 10)) / 25.0  # 정규화 (모두 더하면 1)
image_kernel = cv2.filter2D(image, -1, kernel)  # filter2D 
image_show(image_kernel)

