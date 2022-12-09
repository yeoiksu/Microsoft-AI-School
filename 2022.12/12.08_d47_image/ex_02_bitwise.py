import cv2
import numpy as np
import matplotlib.pyplot as plt

# ex-01
image_rectangle = np.ones((400,400), dtype= 'uint8')
cv2.rectangle(image_rectangle, (50,50), (300,300), (255,255,255), -1)
plt.figure(figsize=(15,15))
plt.subplot(2,3,1)
plt.title("Rectangle")
plt.imshow(image_rectangle, cmap= 'gray')

## ex-02
img_circle = np.ones((400,400), dtype= 'uint8')
cv2.circle(img_circle, (300, 300), 70, (255,255,255), -1)
plt.subplot(2,3,2)
plt.title("Circle")
plt.imshow(img_circle, cmap= 'gray')

## ex-03
bitwiseAnd = cv2.bitwise_and(image_rectangle, img_circle)
plt.subplot(2,3,3)
plt.title("Bitewise And")
plt.imshow(bitwiseAnd, cmap= 'gray')

bitwiseOr  = cv2.bitwise_or(image_rectangle, img_circle)
plt.subplot(2,3,4)
plt.title("Bitewise Or")
plt.imshow(bitwiseOr, cmap= 'gray')

bitwiseXor  = cv2.bitwise_xor(image_rectangle, img_circle)
plt.subplot(2,3,5)
plt.title("Bitewise Xor")
plt.imshow(bitwiseXor, cmap= 'gray')

rec_not = cv2.bitwise_not(image_rectangle, img_circle)
plt.subplot(2,3,6)
plt.title("Bitewise Not")
plt.imshow(rec_not, cmap= 'gray')
plt.show()

# ex-04 마스킹 과제는 흰색대신 이미지를 넣어주시면 됩니다. (원하는 이미지 혹은 얼굴이미지)
face_xml_path = "./2022.12/12.08_d47_image/data/haarcascade_frontalface_default.xml"
image = cv2.imread("./2022.12/12.08_d47_image/data/faces.jpg")
cv2.imshow("Original Image", image)
cv2.waitKey(0)

face_cascade = cv2.CascadeClassifier(face_xml_path)  # face_casecase objects 생성
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # gray
faces = face_cascade.detectMultiScale(gray_image, 1.1, 4)  # face variable

crop_faces = []
for (x, y, w, h) in faces:  # 얼굴 주변 rectangle 정의
    crop_faces.append(image[y:(y+h), x:(x+w)])

mask = np.zeros((683, 1024, 3), dtype='uint8')
cv2.rectangle(mask, (60, 50), (280, 280), (255, 255, 255), -1)
cv2.rectangle(mask, (420, 50), (550, 230), (255, 255, 255), -1)
cv2.rectangle(mask, (750, 50), (920, 280), (255, 255, 255), -1)
cv2.imshow("test", mask)
cv2.waitKey(0)
 
# pt1, pt2 : 사각형의 두 꼭지점 좌표. (x, y) 튜플
# (x, y, w, h)

x_offset = [60, 420, 750]
y_offset = [50, 50, 50]

x_end = [280, 550, 920]
y_end = [280, 230, 280]
resize_crop_faces = []

for i in range(len(crop_faces)):
    # resize
    resize_crop_faces.append(cv2.resize(crop_faces[i], 
                                    (x_end[i]-x_offset[i], y_end[i]-y_offset[i])))
    # add resized crop faces in mask                                    
    mask[y_offset[i]: y_offset[i] + resize_crop_faces[i].shape[0],
        x_offset[i] : x_offset[i] + resize_crop_faces[i].shape[1]] = resize_crop_faces[i]
    print(mask[y_offset[i]: y_offset[i] + resize_crop_faces[i].shape[0],
        x_offset[i] : x_offset[i] + resize_crop_faces[i].shape[1]].shape, resize_crop_faces[i].shape)
cv2.imshow("faces in mask", mask)
cv2.waitKey(0)
