import torch
import os
import glob
import cv2
import xml.etree.ElementTree as ET
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# model call
weight_path = "runs/train/exp4/weights/best.pt"
model = torch.hub.load('ultralytics/yolov5', 'custom', path= weight_path) ### 본인 경로에 맞게 수정

# inference Settings
model.conf = 0.5
model.iou = 0.45
model.to(device)

# image loader
image_dir = "./dataset/valid/images" ### 본인 경로에 맞게 수정
image_path = glob.glob(os.path.join(image_dir, "*.png"))
label_dict = {   
  0: 'drone',
  1: 'bird',
  2: 'birds',
  3: 'airplane',
  4: 'helicopter',
  5: 'balloon'}

tree = ET.ElementTree()
root = ET.Element("annotations")

seen_count = 0

for img_path in image_path :
    # Image
    img = cv2.imread(img_path)

    # Inference
    results = model(img, size=640)

    # Results
    bbox = results.xyxy[0]

    # image name
    image_name = os.path.basename(img_path)

    # image w h
    h, w, c = img.shape

    # xml fix code
    xml_frame = ET.SubElement(root, "image" , id="%d"%seen_count, name=image_name,
                              width="%d"%w, height="%d"%h)


    for box in bbox :
        x1 = box[0].item()
        y1 = box[1].item()
        x2 = box[2].item()
        y2 = box[3].item()
        xtl = str(round(x1,3))
        ytl = str(round(y1,3))
        xbr = str(round(x2,3))
        ybr = str(round(y2,3))

        # clss
        clss_number = box[5].item()
        clss_number_int = int(clss_number)
        labels = label_dict[clss_number_int]

        # sc number
        sc = box[4].item()

        # bbox xml
        ET.SubElement(xml_frame, "box", label=labels, occluded="0", source="manual",
                      xtl=xtl, ytl=ytl, xbr=xbr, ybr=ybr, z_order="0")

    seen_count +=1

tree._setroot(root)
tree.write("test_birds_o.xml", encoding="utf-8")

