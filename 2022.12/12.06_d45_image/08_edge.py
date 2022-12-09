import cv2
import numpy as np
from utils import image_show

# 이미지 경로
image_path = "./2022.12/12.06_d45_image/data/test1.jpg"
image_read = cv2.imread(image_path)
image_gray = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)

# 감지할 모서리 개수
CORNERS_TO_DETECT = 4
MINIMUM_QUALITY_SCORE = 0.05
MINIMUM_DISTANCE = 25

# 모서리 감지
corners = cv2.goodFeaturesToTrack(
    image_gray, CORNERS_TO_DETECT, MINIMUM_QUALITY_SCORE, MINIMUM_DISTANCE)
# print(corners)

for corner in corners:
    x, y = corner[0]
    cv2.circle(image_read, (int(x), int(y)), 10, (0,255,0), -1)

image_gray_temp = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)
image_show(image_gray_temp)
