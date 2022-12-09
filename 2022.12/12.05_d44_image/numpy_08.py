import numpy as np
import cv2

# 이미지 경로 
x = cv2.imread("./2022.12/12.05_d44_image/data/cat.jpg", 0)  # 흑백
y = cv2.imread("./2022.12/12.05_d44_image/data/cat.jpg", 1)  # 컬러

# 여러개 파일 저장 .npz
np.savez("./2022.12/12.05_d44_image/data/image.npz", array1= x, array2= y)

# 압축 방법
np.savez_compressed("./2022.12/12.05_d44_image/data/image_compressed.npz", array1= x, array2= y)

# npz 데이터 불러오기
data = np.load("./2022.12/12.05_d44_image/data/image_compressed.npz")

result1 = data["array1"]
result2 = data["array2"]

cv2.imshow("result1", result1)
cv2.waitKey(0)