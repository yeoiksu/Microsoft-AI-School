#### 이미지 선명하게
import cv2
import numpy as np
import matplotlib.pyplot as plt
# from utils import image_show

# 이미지 경로
image_path = "./2022.12/12.06_d45_image/data/cat.jpg"

# 이미지 읽기 처리
image_bgr = cv2.imread(image_path, cv2.IMREAD_COLOR)

# RGB 타입으로 변환
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

# 커널 생성
kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])

# 커널 적용
image_sharp = cv2.filter2D(image_rgb, -1, kernel)

flg, ax = plt.subplots(1, 2, figsize= (10, 5))
ax[0].imshow(image_rgb)
ax[0].set_title("Original Image")
ax[1].imshow(image_sharp)
ax[1].set_title("Sharp Image")
plt.show()