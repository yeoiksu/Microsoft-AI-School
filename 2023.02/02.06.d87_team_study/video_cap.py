import cv2
video_path = "./2023.02/02.04.d87_team_study/4.mp4"

vidcap = cv2.VideoCapture(video_path) ## 다운받은 비디오 이름 
success,image = vidcap.read()
count = 434

while(vidcap.isOpened()):
    ret, image = vidcap.read()
    
    if count == 800: # 종료 시점 
        break

    if(int(vidcap.get(1)) % 30 == 0): # XX 프레임당 저장
        print('Saved frame number : ' + str(int(vidcap.get(1))))
        cv2.imwrite("./2023.02/02.04.d87_team_study/helicopter/8.video/frame%d.jpg" % count, image)
        print('Saved frame%d.jpg' % count)
        count += 1