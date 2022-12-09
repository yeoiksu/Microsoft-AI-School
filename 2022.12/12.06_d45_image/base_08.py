import cv2
import matplotlib.pyplot as plt

image_path = "./2022.12/12.06_d45_image/data/billiards.jpg"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # gray

# 임계값 연산자의 출력을 마스크 라는 변수에 저장
# 230 이하: 흰색 처리 // 230 이상: 검은색 처리
_ , mask = cv2.threshold(image, 230, 255, cv2.THRESH_BINARY_INV)

titles =["image", "mask"]
images = [image, mask]

for i in range(2):
    plt.subplot(1, 2, i+1),
    plt.imshow(images[i], "gray"),
    plt.title(titles[i]),
    plt.xticks([]),
    plt.yticks([]),
plt.show()

