import cv2
import os

## 1. 동영상 속성 확인
video_path = "./2022.12/12.08_d47_image/data/video01.mp4"
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
count = 0

## 2. 동영상 파일 읽기
if cap.isOpened():
    while True:
        ret, frame = cap.read()
        if ret:
            if (int(cap.get(1)) % fps == 0):  # fps 값을 사용하여 1초마다 추출
                os.makedirs("./2022.12/12.08_d47_image/data/frame_image_save", exist_ok=True)
                cv2.imwrite("./2022.12/12.08_d47_image/data/frame_image_save/" + "frame%d.jpg" %
                            count, frame)
                print("save frame number >> ", str(int(cap.get(1))))
                count += 1
        else:
            break
else:
    print("비디오 열기 실패")

cap.release()
cv2.destroyAllWindows()
