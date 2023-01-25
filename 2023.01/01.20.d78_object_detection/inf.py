import torch
import cv2

# model 
model = torch.hub.load('ultralytics/yolov5',
                        'custom', path = './runs/train/exp3/weights/best.pt')

# Inference setting
model.conf = 0.5  # NMS confidence threshold
model.iou = 0.45  # NMS IoU threshold (실무에서도 거의 고정)

# device setting
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.cpu()   # cpu  version
# model.cuda()  # cuda version
model.to(device)

# one image
image_path = "./dataset/test/images/siang_15112021_1_mp4-226_jpg.rf.156e6b099373ee009c52d96d7aa69d40.jpg"
img1 = cv2.imread(image_path) #opencv image BGR to RGB
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
# img2 = cv2.imread(image_path)[..., ::-1]

# label dict
label_dict = { 
  0 : "big bus",
  1 : "big truck",
  2 : "bus-l-",
  3 : "bus-s-",
  4 : "car",
  5 : "mid truck",
  6 : "small bus",
  7 : "small truck",
  8 : "truck-l-",
  9 : "truck-m-",
  10 : "truck-s-",
  11 : "truck-xl-",
}

# Inference
results = model(img1, size=640)
bbox = results.xyxy[0]
for bbox_info in bbox :
    x1 = bbox_info[0].item()
    y1 = bbox_info[1].item()
    x2 = bbox_info[2].item()
    y2 = bbox_info[3].item()
    sc = bbox_info[4].item()
    label_number = bbox_info[5].item()
    label = label_dict[int(label_number)]

    # image size h w c
    h, w, c = img1.shape

    # xyxy to yolo center_x, center_y, w, h
    center_x = round(((x1 + x2)/2)/w,6)
    center_y = round(((y1 + y2)/2)/h,6)
    yolo_w = round((x2 - x1)/w,6)
    yolo_h = round((y2 - y1)/h,6)
    print(int(label_number), center_x, center_y, yolo_w, yolo_h)

    # yolo center_x , center_y , w ,h -> txt save
    with open(f"./siang_15112021_1_mp4-226_jpg.rf."
              f"156e6b099373ee009c52d96d7aa69d40.txt" ,'a') as f:
        f.write(f"{int(label_number)} {center_x} {center_y} {yolo_w} {yolo_h}\n")

#     img1 = cv2.putText(img1, label, (int(x1), int(y1-10)),
#                        cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255))
#     ret = cv2.rectangle(img1,(int(x1),int(y1)),(int(x2),int(y2)), (0,255,0), 2)
#
# cv2.imshow("test" ,ret)
# cv2.waitKey(0)
