import cv2
import numpy as np

face_xml_path = "./2022.12/12.07_d46_image/data/haarcascade_frontalface_default.xml"
eye_xml_path  = "./2022.12/12.07_d46_image/data/haarcascade_eye.xml"
image_path1    = "./2022.12/12.07_d46_image/data/face.png"
image_path2    = "./2022.12/12.07_d46_image/data/face01.png"

#### 1. face_casecase & eye_cascase objects 생성
face_cascade = cv2.CascadeClassifier(face_xml_path)
eye_cascade  = cv2.CascadeClassifier(eye_xml_path)

#### 2. 얼굴 데이터
image = cv2.imread(image_path2)
cv2.imshow("1. Original", image)
cv2.waitKey(0)

#### 3. 얼굴 감지 바운딩 박스
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # gray
faces = face_cascade.detectMultiScale(gray_image, 1.1, 4)  # face variable
# detectMultiScale(그레이 이미지, 축소할 이미지 배율 인수, 이웃의 최소 수)
for (x, y, w, h) in faces:  # 얼굴 주변 rectangle 정의
    cv2.rectangle(image, (x, y), (x+w, y+h) , (0,255,0), 3)
cv2.imshow("2. Face", image)
cv2.waitKey(0)

#### 4. 눈 감지 바운딩 박스
roi_gray  = gray_image[y:(y+h), x:(x+w)]
roi_image = image[y:(y+h), x:(x+w)]
eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 4) # eyes variable
index = 0
for (ex, ey, ew, eh) in eyes:  # 눈 두개 분리
    if index == 0:
        eye_1 = (ex, ey, ew, eh)
    elif index == 1:
        eye_2 = (ex, ey, ew, eh)
    # 눈 주변 rectangle 정의
    cv2.rectangle(roi_image, (ex,ey), (ex+ew, ey+eh), (0,0,255), 3) 
    index += 1
cv2.imshow("3. Eyes", image)
cv2.imwrite("./2022.12/22.12.07_d46_image/data/man_cascade.png", image)
cv2.waitKey(0)
