### Mexican hat filter
import cv2
import numpy as np
from utils import image_show

image_path = "./2022.12/12.06_d45_image/data/car.jpg"
image = cv2.imread(image_path)

# Mexican hat filter (3x3)
filter = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
mexican_hat_image_3_by_3 = cv2.filter2D(image, -1, filter)
image_show(mexican_hat_image_3_by_3)
cv2.imwrite("./2022.12/12.06_d45_image/data/mexican_hot_3x3.jpg", 
            mexican_hat_image_3_by_3)

# Mexican hat filter (5x5)
filter = np.array([[0,0,-1,0,0],[0,-1,-2,-1,0],
                [-1,-2,16,-2,-1],[0,-1,-2,-1,0],
                [0,0,-1,0,0]])
mexican_hat_image_5_by_5 = cv2.filter2D(image, -1, filter)
image_show(mexican_hat_image_5_by_5)
cv2.imwrite("./2022.12/12.06_d45_image/data/mexican_hot_5x5.jpg", 
            mexican_hat_image_5_by_5)

