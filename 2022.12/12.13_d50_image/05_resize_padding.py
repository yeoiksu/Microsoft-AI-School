import os
import cv2
from PIL import Image

image_path = './2022.12/12.13_d50_image/data/'
image_name = 'flower.png'

def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        # image add (추가 이미지 , 붙일 위치 (가로 , 세로 ))
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result

img = Image.open(image_path + image_name)
img_new = expand2square(img, (0, 0, 0)).resize((224, 224))
img_new.save(image_path + 'flower_resized.png', quality=100)
