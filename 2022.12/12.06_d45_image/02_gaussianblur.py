#### 이미지 blur처리
#### GaussianBlur 2d() 메소드 사용
import cv2
import numpy as np
from utils import image_show

# 이미지 경로
image_path = "./2022.12/12.06_d45_image/data/cat.jpg"

# 이미지 읽기 처리
image = cv2.imread(image_path)

# GaussianBlur(이미지, 커널, 표준편차)
image_g_blur = cv2.GaussianBlur(image, (9,9), 0)
image_show(image_g_blur)
