#### Image Rotate
import cv2
image_path = "./2022.12/12.06_d45_image/data/cat.jpg"  # 이미지 경로

# 이미지 회전
image  = cv2.imread(image_path)
img90  = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE) # 시계방향 90도
img180 = cv2.rotate(image, cv2.ROTATE_180)  # 180 회전
img270 = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)  # 270 회전

# 이미지 크기
print(image.shape)
print(img90.shape)
print(img180.shape)
print(img270.shape)

# 이미지 출력
cv2.imshow("Original Image"  , image)
cv2.imshow("Rotate 90 Image" , img90)
cv2.imshow("Rotate 180 Image", img180)
cv2.imshow("Rotate 270 Image", img270)
cv2.waitKey(0)

# 이미지 좌우 및 상하 반전 (1 좌우 반전 0 상하 반전
dst_temp1 = cv2.flip(image, 1)
dst_temp2 = cv2.flip(image, 0)

cv2.imshow("dst_temp1", dst_temp1)
cv2.imshow("dst_temp2", dst_temp2)
cv2.waitKey(0)
