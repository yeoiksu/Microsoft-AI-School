from PIL import Image
import cv2

'''
opencv -> np array : bgr
Image -> pil : rgb
'''
image_path = "./2022.12/12.07_d46_image/data/billiards.jpg"
img = cv2.imread(image_path)
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
pil_img = Image.fromarray(rgb_img)
pil_img.show()