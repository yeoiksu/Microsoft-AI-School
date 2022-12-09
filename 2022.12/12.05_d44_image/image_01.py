import cv2

img_path = "./2022.12/12.05_d44_image/data/cat.jpg"
img = cv2.imread(img_path)

h, w , _ = img.shape

print("이미지 타입: ", type(img))
print(f"이미지 높이: {h}, 이미지 넓이: {w}")