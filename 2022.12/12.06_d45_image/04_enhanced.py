#### 이미지 대비
import cv2
import matplotlib.pyplot as plt

# 이미지 경로
image_path = "./2022.12/12.06_d45_image/data/cat.jpg"

### 흑백 이미지 대비 높이기
# 이미지 대비 높이기
image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
image_enhanced = cv2.equalizeHist(image_gray)

flg, ax = plt.subplots(1, 2, figsize= (10, 5))
ax[0].imshow(image_gray, cmap= 'gray')
ax[0].set_title("Original Image")
ax[1].imshow(image_enhanced, cmap= 'gray')
ax[1].set_title("Enhanced Image")
plt.show()

### 컬러 이미지 대비 높이기
### 방법 : RGB -> YUV -> equalizeHist() -> RGB
# 1. BGR
image_bgr = cv2.imread(image_path)
# 2. RGB
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
# 3. YUV
image_yuv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2YUV)
# 4. 히스토그램 평활화 적용
image_yuv[:,:,0] = cv2.equalizeHist(image_yuv[:,:,0])
# 5. RGB 변경
image_rgb_temp = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2RGB)

flg, ax = plt.subplots(1, 2, figsize= (12, 8))
ax[0].imshow(image_rgb)
ax[0].set_title("Original Image")
ax[1].imshow(image_rgb_temp)
ax[1].set_title("Enhanced Color Image")
plt.show()