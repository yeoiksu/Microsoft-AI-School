import numpy as np
import random
import cv2
import albumentations as A

keypoints = [
    (100, 100, 50, np.pi/4.0),
    (720, 410, 50, np.pi/4.0),
    (1100, 400, 50, np.pi/4.0),
    (1700, 30, 50, np.pi/4.0),
    (300, 650, 50, np.pi/4.0),
    (1570, 590, 50, np.pi/4.0),
    (560, 800, 50, np.pi/4.0),
    (1300, 750, 50, np.pi/4.0),
    (900, 1000, 50, np.pi/4.0),
    (910, 780, 50, np.pi/4.0),
    (670, 670, 50, np.pi/4.0),
    (830, 670, 50, np.pi/4.0),
    (1000, 670, 50, np.pi/4.0),
    (1150, 670, 50, np.pi/4.0),
    (820, 900, 50, np.pi/4.0),
    (1000, 900, 50, np.pi/4.0),
]  # 15개 

KEYPOINT_COLOR = (0, 255, 0)  # Green

def vis_keypoints(image, keypoints, color=KEYPOINT_COLOR, diameter=15):
    image = image.copy()
    for (x, y, s, a) in keypoints:
        print(x, y, s, a)
        cv2.circle(image, (int(x), int(y)), diameter, color, -1)

        x0 = int(x) + s * np.cos(a)
        y0 = int(y) - s * np.sin(a)
        cv2.arrowedLine(image, (int(x), int(y)), (int(x0), int(y0)), color, 2)

    cv2.imshow("test", image)
    cv2.waitKey(0)

image = cv2.imread("./2022.12/12.15_d52_image/data/fox.png")
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# vis_keypoints(image, keypoints)

transform = A.Compose([
    A.ShiftScaleRotate(p=1),
], keypoint_params=A.KeypointParams(format='xysa', angle_in_degrees=False))

transformed = transform(image=image, keypoints=keypoints)
vis_keypoints(transformed['image'], transformed['keypoints'])


