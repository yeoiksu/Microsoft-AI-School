import cv2
import numpy as np

face_xml_path = "./2022.12/12.08_d47_image/data/haarcascade_frontalface_default.xml"
eye_xml_path  = "./2022.12/12.08_d47_image/data/haarcascade_eye.xml"
image_path1    = "./2022.12/12.08_d47_image/data/face.png"
image_path2    = "./2022.12/12.08_d47_image/data/iksu.jpg"

#### 1. face_casecase & eye_cascase objects 생성
face_cascade = cv2.CascadeClassifier(face_xml_path)
eye_cascade  = cv2.CascadeClassifier(eye_xml_path)

#### 2. 얼굴 데이터
image = cv2.imread(image_path1)
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
# cv2.imwrite("./22.12.07_d46_image/data/man_cascade.png", image)
cv2.waitKey(0)

#### 5. 좌우 눈 설정
if eye_1[0] < eye_2[0]:
    left_eye  = eye_1
    right_eye = eye_2
else:
    left_eye  = eye_2
    right_eye = eye_1   

#### 6. 직사각형 중심점의 좌표 계산
left_eye_center = (int(left_eye[0] + (left_eye[2]/2)), int(left_eye[1] + (left_eye[3]/2)))
left_eye_x = left_eye_center[0]
left_eye_y = left_eye_center[1]

right_eye_center = (int(right_eye[0] + (right_eye[2]/2)), int(right_eye[1] + (right_eye[3]/2)))
right_eye_x = right_eye_center[0]
right_eye_y = right_eye_center[1]

cv2.line(roi_image, right_eye_center, left_eye_center, (0,200,200), 3)
cv2.circle(roi_image, left_eye_center,  5, (255,0,0), -1)
cv2.circle(roi_image, right_eye_center, 5, (255,0,0), -1)

cv2.imshow("4. Center Eyes", image)
cv2.waitKey(0)

#### 7.  두 눈의 중심점을 연결하는 선 사이의 각도 계산
if left_eye_y > right_eye_y:
    A = (right_eye_x, left_eye_y)
    direction = -1  # clockwise로 회전
else:
    A = (left_eye_y, right_eye_x)
    direction = 1   # coutner clockwise로 회전

cv2.line(roi_image, right_eye_center, left_eye_center, (0,200,200), 3)
cv2.line(roi_image, left_eye_center, A, (0,200,200), 3)
cv2.line(roi_image, right_eye_center, A, (0,200,200), 3)
cv2.circle(roi_image, A, 5, (255,0,0), -1)

cv2.imshow("5. Center Eyes Triangle", image)
cv2.waitKey(0)

#### 8. 각도 구하기
# np.arctan = 함수 단위는 라디안
# 라디안 -> 각도 : (theta * 100) / np.pi
delta_x = right_eye_x - left_eye_x
delta_y = right_eye_y - left_eye_y
angle = np.arctan(delta_y/delta_x)
angle = (angle*180) / np.pi # 각도 (약 -21도)

#### 9. 회전 하기
h, w = image.shape[:2]
center = (w//2, h//2)
M = cv2.getRotationMatrix2D(center, (angle), 1.0)  # 회전
rotated = cv2.warpAffine(image, M, (w, h))

cv2.imshow("6. Rotated", rotated)
cv2.waitKey(0)