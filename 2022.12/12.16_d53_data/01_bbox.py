import random
import cv2
import albumentations as A

BOX_COLOR = (255,0,0)  # RED
TEXT_COLOR = (255, 255, 255)  # WHITE


def visualize_bbox(image, bboxes, category_ids, category_id_to_name,
                   color=BOX_COLOR, thickness=2):
    img = image.copy()
    for bbox, category_id in zip(bboxes, category_ids):
        class_name = category_id_to_name[category_id]
        print("class_name >> ", class_name)
        x_min, y_min, w, h = bbox
        x_min, x_max, y_min, y_max = int(x_min), int(
            x_min + w), int(y_min), int(y_min + h)

        cv2.rectangle(img, (x_min, y_min), (x_max, y_max),
                      color=color, thickness=thickness)
        cv2.putText(img, text=class_name, org=(x_min, y_min-15),
                    fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=color,
                    thickness=thickness)
    cv2.imshow("test", img)
    cv2.waitKey(0)

# custom = 

path= "./2022.12/12.16_d53_data/data/cat.png"
image = cv2.imread(path)
# dog -> [468.94, 92.01, 171.06, 248.45] 2
# cat -> [3.96, 183.38, 200.88, 214.03] 1

bboxes = [[3.96, 183.38, 200.88, 214.43], [468.94, 92.01, 171.06, 248.45]]
category_ids = [1, 2]
category_id_to_name = {1:' cat', 2: 'dog'}
# visualize_bbx(image, bboxes, category_ids, category_id_to_name, 
#         color= BOX_COLOR, thickness= 2)

# transforms
transfor = A.Compose([
    A.RandomSizedBBoxSafeCrop(width=448, height=336, erosion_rate=0.2),
    A.HorizontalFlip(p=1),
    A.RandomRotate90(p=1),
], bbox_params=A.BboxParams(format='coco', label_fields=['category_ids']))
# xml 사용시는 pascal, 
# coco, yolo, pascal 사용가능

transformed = transfor(image=image, bboxes=bboxes, category_ids=category_ids)

visualize_bbox(transformed['image'], transformed['bboxes'], transformed['category_ids'],
               category_id_to_name,
               color=BOX_COLOR, thickness=2)

