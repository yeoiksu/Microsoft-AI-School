#### 모서리 감지
import cv2
import numpy as np
from utils import image_show

# 이미지 경로
image_path = "./2022.12/12.06_d45_image/data/test1.jpg"
image_read = cv2.imread(image_path)

image_gray = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)
image_gray = np.float32(image_gray)

BLOCK_SIZE = 2  # 모서리 감지 매개 변수 설정
APERTURE = 29
FREE_PARAMETER = 0.04

detector_response = cv2.cornerHarris(image_gray,
                                    BLOCK_SIZE,
                                    APERTURE,
                                    FREE_PARAMETER)

print(detector_response)

THRESHOLD = 0.02
image_read[detector_response > THRESHOLD * 
            detector_response.max()] = [255,255,255]

image_gray = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)
image_show(image_gray)





