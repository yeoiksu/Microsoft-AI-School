#### adaptiveThreshold
import cv2
from utils import image_show

# 이미지 경로
image_path = "./2022.12/12.06_d45_image/data/cat.jpg"

# 이미지 이진화
image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
MAX_OUTPUT_VALUE   = 255
NEIGHBORHOOD_SIZE  = 99
SUBTRACT_FROM_MEAN = 10

image_binary = cv2.adaptiveThreshold(image_gray, 
                                    MAX_OUTPUT_VALUE,
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                    cv2.THRESH_BINARY,
                                    # cv2.THRESH_BINARY_INV, # 검정색(반전)
                                    NEIGHBORHOOD_SIZE,
                                    SUBTRACT_FROM_MEAN)
image_show(image_binary)

