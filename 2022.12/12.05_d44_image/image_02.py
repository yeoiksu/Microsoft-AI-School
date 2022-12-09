import cv2
import matplotlib.pyplot as plt
image_path = "./2022.12/12.05_d44_image/data/cat.jpg"  # 경로

# 이미지 읽기
image = cv2.imread(image_path)

# RGB 변환
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 사이즈 변환
image_50_by_50 = cv2.resize(image, (50,50))

# 이미지 저장
cv2.imwrite("./2022.12/12.05_d44_image/data/cat_resized.jpg", image_50_by_50)
image_50_by_50 = cv2.resize(image_rgb, (50,50))

flg, ax = plt.subplots(1, 2, figsize= (10, 5))
ax[0].imshow(image_rgb)
ax[0].set_title("Original Image")
ax[1].imshow(image_50_by_50)
ax[1].set_title("Resize Image")
plt.show()