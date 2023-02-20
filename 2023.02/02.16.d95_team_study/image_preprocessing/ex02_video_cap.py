import cv2
video_path = "C:/Users/user/Documents/03.dataset/230206_dataset/heli_video/heli_video_10.mp4"

vidcap = cv2.VideoCapture(video_path) ## 다운받은 비디오 이름 
success,image = vidcap.read()
count = 875

while(vidcap.isOpened()):
    ret, image = vidcap.read()
    
    if count == 3000: # 종료 시점 
        break

    if(int(vidcap.get(1)) % 30 == 0): # XX 프레임당 저장
        print('Saved frame number : ' + str(int(vidcap.get(1))))
        cv2.imwrite("C:/Users/user/Documents/03.dataset/230206_dataset/test/frame%d.png" % count, image)
        print('Saved frame%d.jpg' % count)
        count += 1