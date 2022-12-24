# Resize & Padding 
'''
data/image
    - banana
    - kiwi  
    - orange 
    - pineapple 
    - watermelon
'''

import os
import cv2
import argparse
import glob
from PIL import Image

# 폴더 구성 /dataset/image/각 폴더명 / 이미지 저장 (resize 400 x 400)
# 직사각형 -> 정사각형 리사이즈 비율 유지하는 함수 (padding)

folder_path = "./2022.12/12.19_d54_data/images"

#### image padding 함수
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

#### image padding 함수
def image_file_check(opt):
    image_path = opt.image_folder_path
    new_path = image_path.replace(f"images", "dataset/images") # '12.19_d54_data/images -> 12.19_d54_data/dataset/images
    os.makedirs(new_path, exist_ok= True) # './2022.12/12.19_d54_data/dataset 폴더 생성
    total_len = 0   # 이미지 총 개수

    for index, item in enumerate(os.listdir(image_path)):
        item_image_path = os.path.join(image_path, item)
        # [./2022.12/12.19_d54_data/images\banana, ./2022.12/12.19_d54_data/images\kiwi ... ]

        os.makedirs(os.path.join(new_path,item) , exist_ok= True)
        
        image_len = len(os.listdir(item_image_path))  # 파일 길이

        data = glob.glob(os.path.join(item_image_path, "*.jpg"))
        # ['./2022.12/12.19_d54_data/images\\banana\\banana_0.jpg', './2022.12/12.19_d54_data/images\\banana\\banana_1.jpg', ... ]

        #### 이미지 resize & png 파일로 저장 
        for idx, image in enumerate(data):
            img = Image.open(image)
            img_new = expand2square(img, (0, 0, 0)).resize((400, 400))
            try:
                img_new.save(f"{os.path.join(new_path,item)}/{item}_{str(idx)}.png", quality=100)
                # ./2022.12/12.19_d54_data/images\banana/banana_resized_0.jpg
            except:
                pass

    #### 각 폴더별 데이터 양 체크        
    # banana
        if index == 0:
            print("Banana\t\t:", image_len)            
    # kiwi
        elif index == 1:
            print("Kiwi\t\t:", image_len)            
    # orange
        elif index == 2:
            print("Orange\t\t:", image_len)            
    # pineapple
        elif index == 3:
            print("Pineapple\t:", image_len)            
    # watermelon
        elif index == 4:
            print("Watermelon\t:", image_len)            
        total_len += image_len  # 이미지 총 개수
    print("Total\t\t:", total_len)

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-folder-path", type=str, default= folder_path)
    opt = parser.parse_args()

    return opt

if __name__ == "__main__":
    opt = parse_opt()
    image_file_check(opt)