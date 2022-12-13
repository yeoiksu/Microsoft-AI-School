import os
import json
import cv2

#### 1. json 파일 읽기
json_path_banana = './2022.12/12.13_d50_image/data/banana/annotations/instances_default.json'
lines = '\n' + ('='*80)

with open(json_path_banana, "r", encoding='UTF-8') as f:
    coco_info = json.load(f)
    # print(coco_info,lines)
assert len(coco_info) > 0, "파일 읽기 실패"  # 시도하고 실패면 뒤에 " " 출력

#### 2. 카테고리 정보 수집
categories = dict()
for category in coco_info['categories']:
    categories[category["id"]] = category["name"]

#### 3. annotation 정보 수집
ann_info = dict()
for annotation in coco_info['annotations']:
    image_id      = annotation['image_id']
    bbox          = annotation['bbox']
    category_id   = annotation['category_id']
    segmentation = annotation["segmentation"]
    # print(image_id, category_id, bbox, segmentation, lines)

    if image_id not in ann_info:
        ann_info[image_id] = {
            "boxes" : [bbox], "categories" : [category_id],
            "segmentation" : [segmentation]
        }
    else:
        ann_info[image_id]["boxes"].append(bbox)
        ann_info[image_id]["segmentation"].append(segmentation)
        ann_info[image_id]["categories"].append(categories[category_id])

#### 4. 이미지 정보 출력
for image_info in coco_info['images']:
    file_name = image_info['file_name']
    width     = image_info['width']
    height    = image_info['height']
    img_id    = image_info['id']

    file_path = os.path.join('./2022.12/12.13_d50_image/data/banana/images', file_name)
    img = cv2.imread(file_path)
    try : 
        annotation = ann_info[img_id]
    except KeyError:
        continue

    ## box category
    for bbox, category, segmentation in zip(annotation['boxes'], annotation['categories'], annotation['segmentation']):
        x, y, w, h = bbox
        import numpy as np
        for seg in segmentation:
            poly = np.array(seg, np.int32).reshape((int(len(seg)/2), 2))
            print(poly)
            poly_img = cv2.polylines(img, [poly], True, (255,0,0), 2)
            
    cv2.imshow("Seg", poly_img)
    cv2.waitKey(0)