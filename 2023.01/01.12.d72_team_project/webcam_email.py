import cv2
import torch
import torchvision.models as models
import torch.nn as nn
import albumentations as A
import torch.nn.functional as F
from albumentations.pytorch.transforms import ToTensorV2
from PIL import Image
import numpy as np
from torchvision import transforms
import time
import math
from ex07_email import *

#### 경고문, threshold ###
warning_text = '[[ Warning ]]'
THRESHOLD_VALUE = 98

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
labels = {0:"bird" , 1:"drone"}

data_transforms = transforms.Compose([ 
        transforms.Resize((224,224)),
        transforms.CenterCrop(200),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
######## 모델 수정#########
model = models.mobilenet_v2(pretrained=False)
model.classifier[1] = nn.Linear(in_features=1280, out_features=2)
model.load_state_dict(torch.load("./2023.01/01.12.d72_dl/12nd.pt",map_location=device)) 
# cuda에서 cpu로 넘겨주기 위해 map_location사용. cuda 대 cuda일 경우 생략.
model = model.to(device)
model.eval()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 850)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 850)

# fps값 추출
fps = cap.get(cv2.CAP_PROP_FPS)
print("현재 fps :", fps)

# 화면에 출력될 fps
fps_monitor = f'{int(fps)} FPS'

if cap.isOpened():
  while True:
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(frame)# fromarray : NumPy 배열을 Image 객체로 바꿀 때
    input_img = data_transforms(pil_img).reshape([1,3,200,200]).to(device)# reshaep([이미지수,채널수,height,width])
    out = model(input_img)
    softmax_result = F.softmax(out)
    top1_prob, top1_label = torch.topk(softmax_result, 1)

    # CCTV에 정확도(%) 표시 
    acc = str(round(top1_prob.item()*100, 3)) + "%"
    
    # thresholed를 위한 정확도
    acc_num = (round(top1_prob.item()*100, 3))
    
    # thresholed를 위한 레이블 이름
    object_label = labels.get(int(top1_label))

    # threshold를 넘는 경우에만 물체를 분류
    if acc_num > THRESHOLD_VALUE :

        # threshold를 넘으며 레이블이 '드론'일 경우
        if object_label == 'drone':
            # 화면에 경고문 출력
            cv2.putText(frame, warning_text, (150, 200), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0),3)
            print("Drone Appears!!!!")
            # 화면에 레이블 출력
            cv2.putText(frame, labels.get(int(top1_label)), (10, 400), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 1)
            # 화면에 예측 확률 출력
            cv2.putText(frame, acc, (10, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255 ,255 ), 1)
            print(acc, labels.get(int(top1_label)))
            time.sleep(5)
            send_alarm()

        # threshold를 넘으며 레이블이 드론이 아니고 '새'일 경우
        elif object_label =='bird' :
            # 화면에 레이블 출력
            cv2.putText(frame, labels.get(int(top1_label)), (10, 400), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 1)
            # 화면에 레이블 출력
            cv2.putText(frame, acc, (10, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255 ,255 ), 1)
            print(acc, labels.get(int(top1_label)))
    
    # threshold 넘지못하면 ...으로 분류
    else: # 아무일도 없었다.
        cv2.putText(frame, '...', (150, 200), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0),3)

    # 윈도우 창으로 출력하는 단
    cv2.putText(frame, fps_monitor, (500, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0), 1)
    cv2.imshow("Webcam CCTV", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    # BGR -> RGB로 변환
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    
    if cv2.waitKey(25) ==27 : 
        break
else:
    print('영상 읽기 실패...')

cap.release() # 자원 반납
cv2.destroyAllWindows() # 창 닫기.