import cv2
# from image_03 import image_show

def imshow(image):  
    cv2.imshow("show", image)
    cv2.waitKey(0)

image_path = "./2022.12/12.05_d44_image/data/cat.jpg"

# 이미지 읽기
image = cv2.imread(image_path)

# 이미지 Blur
image_blury = cv2.blur(image, (5,5))
imshow(image_blury)

