import cv2

## 1. 동영상 속성 확인
video_path = "./2022.12/12.08_d47_image/data/video01.mp4"
cap = cv2.VideoCapture(video_path)
width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)

print("Width: ", width, ", Height: ", height) 
print("Frame Count: ", frame_count)
print("fps: ", fps)

## 2. 동영상 파일 읽기
if cap.isOpened():  # 캡처 객체 초기화 확인
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Video File Show", frame)
            cv2.waitKey(25)  # 25 fps 기준으로 프레임 나눠
        else:
            break
else:
    print("비디오 파일 읽기 실패")

cap.release()
cv2.destroyAllWindows()
