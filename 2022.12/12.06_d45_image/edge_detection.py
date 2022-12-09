import cv2
import numpy as np
from utils import image_show

# 이미지 경로
image_path = "./2022.12/12.06_d45_image/data/test.jpg"

# 경계선 찾기
image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# 픽셀 가옫의 중간값을 계산
median_intensity = np.median(image_gray)
print(median_intensity)

# 중간 픽셀 강도에서 위아래 1 표준편차 떨어진 값을 임계값으로 설정
lower_threshold = int(max(0, (1.0 - 0.33) * median_intensity))
upper_threshold = int(min(255, (1.0 + 0.33) * median_intensity))

# Canny Edge Detection 적용
image_canny = cv2.Canny(image_gray, lower_threshold, upper_threshold)
image_show(image_canny)