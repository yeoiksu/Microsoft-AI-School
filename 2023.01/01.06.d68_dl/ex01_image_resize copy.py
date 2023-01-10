from PIL import Image # pip install Pillow
import os
import glob

def expand2square(pil_img, background_color) :
    width, height = pil_img.size   
    if width == height :
        return pil_img
    elif width > height :
        result = Image.new(pil_img.mode, (width, width), background_color)
        # image add(추가할 이미지, 붙일 위치(가로, 세로))
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else :
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result

file_path = "./2023.01/01.06.d68_dl/raw_data"   # 위치 자신의 파일경로에 맞게 변경 필요 !!!
image_list = glob.glob(os.path.join(file_path, "*", "*"))

for item_path in image_list:
    newfile_path = item_path.replace("raw_data", "resize_data") # raw_data -> resize_data
    newfile_path = newfile_path.replace(".jpg", ".png")         # png로 변환

    image = Image.open(item_path).resize(224,224)  # 224로 리사이즈
    new_image = expand2square(image, (0,0,0))      # 정사각형화, 뒷배경 검은색
    new_image.save(newfile_path)



