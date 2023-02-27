import os
import os.path as osp
import glob
import shutil
import cv2
import xml.etree.ElementTree as ET

tree = ET.ElementTree()
root = ET.Element("annotations")

paths_old = "C:/Users/user/Documents/DATASET/HELICOPTER"
new_img_path = osp.join(paths_old, "images")
new_txt_path = osp.join(paths_old, "labels")

img_paths = glob.glob(osp.join(new_img_path, "*.png"))
txt_paths = glob.glob(osp.join(new_txt_path, "*.txt"))

paths_new = "C:/Users/user/Documents/DATASET"
path_img = osp.join(paths_new, "images")
# path_txt = osp.join(paths_new, "labels")

os.makedirs(path_img, exist_ok= True)
# os.makedirs(path_txt, exist_ok= True)

NUM = 8400
seen_count = 0

for index, img_path in enumerate(img_paths):
    # front_path = img_path.split('\\')[0]    # C:/Users/user/Documents/DATASET/HELICOPTER
    img_name   = img_path.split('\\')[-1]   # HELICOPTER_000002.png
    NEW_NUM = index + NUM
    image = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img_width = int(image.shape[0])
    img_height = int(image.shape[1])

    # image save
    new_image_name = f'helicopter_{NEW_NUM}.png'
    new_text_name  = f'helicopter_{NEW_NUM}.txt'
    shutil.copy(img_path, osp.join(path_img, new_image_name))
    
    # xml fix code
    xml_frame = ET.SubElement(root, "image", id="%d"%seen_count, name=new_image_name,
                            width="%d"%img_width, height="%d"%img_height)
    try:    
        bbox = []
        f = open(txt_paths[index], 'r')
        while True:
            line = f.readline()
            if not line: break
            # print(line)
            box = line.split(" ")
            bbox.append([float(x) for x in box])
        f.close()

        print(index,'\t',img_name)
        for box in bbox:
            # yolo 형식에 맞게 normalization을 해보자
            # yolo_x = round(((box[0] + box[2]) / 2) / img_width, 6)
            # yolo_y = round(((box[1] + box[3]) / 2) / img_height, 6)
            # yolo_w = round((box[2] - box[0]) / img_width, 6)
            # yolo_h = round((box[3] - box[1]) / img_height, 6)
            # print("yolo xywh >>>", yolo_x, yolo_y, yolo_w, yolo_h)
            # # 앞서 모은 정보들로 txt파일로 저장해보자
            # with open(osp.join(path_txt, new_text_name), 'a') as ff :
            #     ff.write(f"3 {yolo_x} {yolo_y} {yolo_w} {yolo_h}\n") # helicopter라 3

            x1 = box[0]
            y1 = box[1]
            x2 = box[2]
            y2 = box[3]
            xtl = str(round(x1,3))
            ytl = str(round(y1,3))
            xbr = str(round(x2,3))
            ybr = str(round(y2,3))

            image = cv2.putText(image, 'helicopter', (int(x1), int(y1-10)),
                            cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255))
            ret = cv2.rectangle(image,(int(x1),int(y1)),(int(x2),int(y2)), (0,255,0), 2)

            # bbox xml
            ET.SubElement(xml_frame, "box", label='helicopter', occluded="0", source="manual",
                        xtl=xtl, ytl=ytl, xbr=xbr, ybr=ybr, z_order="0")

        seen_count +=1

        cv2.imshow(new_image_name, image)
        cv2.waitKey(0)

    except Exception as e:
        print(e)

tree._setroot(root)
tree.write("C:/Users/user/Documents/DATASET/test.xml", encoding="utf-8")