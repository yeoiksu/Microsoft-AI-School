import os
import json
import cv2
import pandas as pd
import xml.etree.ElementTree as ET

#### 1. json 파일 읽기
json_path_banana = './2022.12/12.13_d50_image/data/banana/annotations/instances_default.json'
json_path_apple  = './2022.12/12.13_d50_image/data/apple/annotations/instances_default.json'
json_path_kiwi   = './2022.12/12.13_d50_image/data/kiwi/annotations/instances_default.json'
lines = '\n' + ('='*80)


with open(json_path_banana, "r", encoding='UTF-8') as f:
    coco_info = json.load(f)
# print(coco_info, lines)
assert len(coco_info) > 0, "파일 읽기 실패"  # 시도하고 실패면 뒤에 " " 출력

#### 2. 카테고리 정보 수집
categories = dict()
for category in coco_info['categories']:
    # print(category, lines)
    categories[category['id']] = category['name']
# print('categories info : ', categories)

#### 3. annotation 정보 수집
ann_info = dict()
for annotation in coco_info['annotations']:
    image_id    = annotation['image_id']
    bbox        = annotation['bbox']
    category_id = annotation['category_id']
    # print(f"image_id: {image_id}, category_id : {category_id}, bbox : {bbox}", lines)

    if image_id not in ann_info:
        ann_info[image_id] = {
            "boxes" : [bbox], "categories" : [category_id]
        }
    else:
        ann_info[image_id]["boxes"].append(bbox)
        ann_info[image_id]["categories"].append(categories[category_id])
# print("ann_info : " , ann_info)

#### 4. 이미지 정보 출력
file_list = []
x_list, y_list, w_list, h_list = [], [], [], []

for i, image_info in enumerate(coco_info['images']):
    file_name = image_info['file_name']
    width     = image_info['width']
    height    = image_info['height']
    img_id    = image_info['id']
    file_path = os.path.join('./2022.12/12.13_d50_image/data/banana/images', file_name)

    #### 이미지 가져오기 위한 처리
    img = cv2.imread(file_path)

    try : 
        annotation = ann_info[img_id]
    except KeyError:
        continue
    
    # box category
    label_list = {1: 'banana', 2: 'apple', 3:'kiwi'}

    ## box category
    for bbox, category in zip(annotation['boxes'], annotation['categories']):
        x, y, w, h = bbox
        rec_img = cv2.rectangle(img, 
                            (int(x), int(y)),
                            (int(x+w), int(y+h)), 
                            (225, 0, 255), 2)

        print(x, y, w, h)
    # cv2.imwrite()
    # cv2.imshow('Rectangle', rec_img)
    # cv2.waitKey(0)    

    file_list.append(file_name)
    x_list.append(x)
    y_list.append(y)
    w_list.append(w)
    h_list.append(h)
  
my_dict = {'file_name' : file_list,
    'x1': x_list,
    'y1': y_list,
    'w' : w_list,
    'h' : h_list
}
df = pd.DataFrame(my_dict)
df.to_csv('./2022.12/12.13_d50_image/bbox_data.csv', sep=',')
# print(df.head(10))



    