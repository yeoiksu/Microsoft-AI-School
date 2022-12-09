### 배경 제거
import cv2
import numpy as np
from utils import image_show

# 이미지 경로
image_path = "./2022.12/12.06_d45_image/data/test.jpg"

# 이미지 읽기
image = cv2.imread(image_path)
print(image.shape)

# 사각형 좌표 : 시작점 : x, y, 넓이, 높이
rectangle = (0,0,400,400)
# image = cv2.rectangle(image, (30,30), (150,150), (255,0,255), 2)
# image_show(image)

# 초기 마스크 생성
mask = np.zeros(image.shape[:2], np.uint8)

# grabCut에 사용할 임시 배열 생성
bgdModel = np.zeros((1,65), np.float64)
fgdModel = np.zeros((1,65), np.float64)

# grabCut 실행
# image -> 원본 이미지, bgdModel -> 배경을 위한 임시 배열 fgdModel -> 전경배경,
# 5-> 반복횟수 cv2.GC_INIT_WITH_RECT -> 사각형 초기화
cv2.grabCut(image, mask, rectangle, bgdModel,
            fgdModel, 5, cv2.GC_INIT_WITH_RECT)

# 배경인 곳은 0, 그 외에는 1로 설정한 마스크 생성
mask_2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# 이미지에 새로운 마스크 곱해서 -> 배경 제외
image_rgb_nobg = image * mask_2[:, :, np.newaxis]
image_show(image_rgb_nobg)


