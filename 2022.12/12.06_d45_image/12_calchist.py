### calcHist
import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import image_show

# 이미지 경로
image_path = "./2022.12/12.06_d45_image/data/cat.jpg"
image_bgr = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
features = []  # 특성 값을 담을 리스트
colors = ("r", "g", "b")  # 각 컬러 체널에 대해 히스토그램을 계산
for i, channel in enumerate(colors):
    # calcHist([이미지], [체널 인덱스], [마스크 없으므로 None], [히스토그램 크기])
    histogram = cv2.calcHist([image_rgb], [i], None, [256], [0,256])
    plt.plot(histogram, color= channel)
    plt.xlim([0, 256])
plt.show()






