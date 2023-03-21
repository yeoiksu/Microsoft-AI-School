import cv2, threading, sys, numpy as np, torch, time, argparse, os, glob, requests, platform
from torch import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5 import uic
from important_data import *
# from qt_material import list_themes
# from qt_material import apply_stylesheet
from pathlib import Path
import torch.backends.cudnn as cudnn
from threading import Thread


"""limit the number of cpus used by high performance libraries"""
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

''' 멀티 프로세스 & EMAIL 보내기 & DB에 데이터 보내기위한 시간 라이브러리 ''' 
from multiprocessing import Process

from collections import deque

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # yolov5 strongsort root directory
WEIGHTS = ROOT / 'weights'

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
if str(ROOT / 'version') not in sys.path:
    sys.path.append(str(ROOT / 'version'))  # add yolov5 ROOT to PATH
if str(ROOT / 'trackers' / 'strongsort') not in sys.path:
    sys.path.append(str(ROOT / 'trackers' / 'strongsort'))  # add strong_sort ROOT to PATH

ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

import logging
from version.ultralytics.nn.autobackend import AutoBackend
from version.ultralytics.yolo.data.dataloaders.stream_loaders import LoadImages, LoadStreams
from version.ultralytics.yolo.data.utils import IMG_FORMATS, VID_FORMATS
from version.ultralytics.yolo.utils import DEFAULT_CFG, LOGGER, SETTINGS, callbacks, colorstr, ops
from version.ultralytics.yolo.utils.checks import check_file, check_imgsz, check_imshow, print_args, check_requirements
from version.ultralytics.yolo.utils.files import increment_path
from version.ultralytics.yolo.utils.torch_utils import select_device
from version.ultralytics.yolo.utils.ops import Profile, non_max_suppression, scale_boxes, process_mask, process_mask_native
from version.ultralytics.yolo.utils.plotting import Annotator, colors, save_one_box

from trackers.multi_tracker_zoo import create_tracker
from email_db import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

'''ui폼 받아오기'''
# Main
form = resource_path('ex01.ui')
form_class = uic.loadUiType(form)[0]

# Email
form_2 = resource_path('ex02_email.ui')
form_email = uic.loadUiType(form_2)[0]

"""Main Window"""
class Ui_MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        '''Ui 디자인'''
        back_Image = QImage("pics/background.png")
        size_Image = back_Image.scaled(QSize(1138, 677))
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap(size_Image))) # <= 원하시는 사진
        self.setPalette(palette)
        self.date = QDate.currentDate()
        self.setupUi(self)
        self.isCamOn = False

        ''' 웹캠 동작(종료)시키는 클릭 이벤트 처리 연결'''
        self.pushButton_cctv_on.clicked.connect(self.live_webcam_click_on)  # 동작
        self.pushButton_cctv_off.clicked.connect(self.live_webcam_click_off) # 종료 

        # # '''Live Webcam 공간 부분''' --> 무쓸모로 판명
        # self.box_webcam = QtWidgets.QGroupBox(self.centralwidget)
        # self.box_webcam.setGeometry(QtCore.QRect(320, 50, 770, 500)) # 좌측 상단 X좌표, 좌측 상단 Y좌표, X로부터 우측으로의 거리, Y로부터 아래쪽으로의 거리
        # font = QtGui.QFont()
        # font.setFamily("Yu Gothic UI Semibold")
        # font.setPointSize(10)
        # font.setBold(True)
        # font.setWeight(75)
        # self.box_webcam.setFont(font)
        # self.box_webcam.setObjectName("box_webcam")

        ''' 실제 카메라 화면 출력 부분'''
        self.frame = QLabel(self.box_webcam)
        self.frame.setGeometry(QtCore.QRect(10, 20, 1000, 511))
        self.frame.setObjectName("box_webcam")

    '''on 버튼 눌렀을 시 웹캠 시작'''
    def live_webcam_click_on(self) :
        self.isCamOn =True
        opt = myWindow.parse_opt()
        self.run(**vars(opt))

    '''off 버튼 눌렀을 시 웹캠 종료'''
    def live_webcam_click_off(self) :
        self.frame.clear() 
        QMessageBox.about(self, 'App Alert', '연결된 카메라를 끕니다.')
        self.frame.hide() # 정확히는 숨김 처리 --> 노트
        self.isCamOn = False
        print('\n--------------------------------------------------------------------')
        print('live_webcam_click_off 함수에서 isCamOn : ', self.isCamOn)
        print('--------------------------------------------------------------------\n')

    '''X버튼 누를 시 종료 재확인 메세지'''
    def closeEvent(self, QCloseEvent): # 오버라이딩 메소드
        self.isCamOn = False
        ans = QMessageBox.question(self, "종료 확인","종료하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    # 2번 버튼
    ''' email버튼 클릭 시 이메일 창 활성화'''    
    def email_clicked(self):
        # self.hide() # 메인윈도우 숨김
        self.second = email_form()
        self.second.exec() # 두번째 창을 닫을 때 까지 기다림
        self.show() 

    '''3번 버튼 클릭 시 연결'''
    def connect_powerbi(self):
        import webbrowser
        webbrowser.open(POWER_BI_LINK)

    # 3번 버튼
    '''Data Analysis 버튼 클릭 시 DB창으로 이동'''
    def bi_clicked(self):
        # self.hide() # 메인윈도우 숨김
        self.second = self.connect_powerbi() 
        # self.second.exec() # 두번째 창을 닫을 때 까지 기다림
        # self.show() 

    @torch.no_grad()
    def run(
            self,
            source='0',
            yolo_weights=WEIGHTS / 'yolov5m.pt',  # model.pt path(s),
            reid_weights=WEIGHTS / 'osnet_x0_25_msmt17.pt',  # model.pt path,
            tracking_method='strongsort',
            tracking_config=None,
            imgsz=(1000, 640),  # inference size (height, width)
            conf_thres=0.25,  # confidence threshold
            iou_thres=0.45,  # NMS IOU threshold
            max_det=1000,  # maximum detections per image
            device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
            show_vid=True,  # show results
            save_txt=False,  # save results to *.txt
            save_conf=False,  # save confidences in --save-txt labels
            save_crop=False,  # save cropped prediction boxes
            save_trajectories=False,  # save trajectories for each track
            save_vid=True,  # save confidences in --save-txt labels
            nosave=False,  # do not save images/videos
            classes=None,  # filter by class: --class 0, or --class 0 2 3
            agnostic_nms=False,  # class-agnostic NMS
            augment=False,  # augmented inference
            visualize=False,  # visualize features
            update=False,  # update all models
            project=ROOT / 'runs' / 'track',  # save results to project/name
            name='exp',  # save results to project/name
            exist_ok=False,  # existing project/name ok, do not increment
            line_thickness=2,  # bounding box thickness (pixels)
            hide_labels=False,  # hide labels
            hide_conf=False,  # hide confidences
            hide_class=False,  # hide IDs
            half=False,  # use FP16 half-precision inference
            dnn=False,  # use OpenCV DNN for ONNX inference
            vid_stride=1,  # video frame-rate stride
            retina_masks=False,
            
            send_DB = False, # 데이터 베이스로 데이터를 보낼지 말지 
            send_DB_term = 60, # DB로 보내는 시간(초) 단위
            send_EMAIL = False,
            send_EMAIL_term = 3,
            target_object = 'military drone'
    ):
    
 
    
            source = str(source)
            save_img = not nosave and not source.endswith('.txt')  # save inference images
            is_file = Path(source).suffix[1:] in (VID_FORMATS)
            is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
            webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)
            if is_url and is_file:
                source = check_file(source)  # download

            # Directories
            if not isinstance(yolo_weights, list):  # single yolo model
                exp_name = yolo_weights.stem
            elif type(yolo_weights) is list and len(yolo_weights) == 1:  # single models after --yolo_weights
                exp_name = Path(yolo_weights[0]).stem
            else:  # multiple models after --yolo_weights
                exp_name = 'ensemble'
            exp_name = name if name else exp_name + "_" + reid_weights.stem
            save_dir = increment_path(Path(project) / exp_name, exist_ok=exist_ok)  # increment run
            (save_dir / 'tracks' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

            # Load model
            device = select_device(device)
            is_seg = '-seg' in str(yolo_weights)
            model = AutoBackend(yolo_weights, device=device, dnn=dnn, fp16=half)
            stride, names, pt = model.stride, model.names, model.pt
            imgsz = check_imgsz(imgsz, stride=stride)  # check image size

            '''DB 관련 '''
            is_data_sent = False 
            is_db_first = True  # db 첫번째로 보내는 데이터 추가 
            '''EMAIL 관련'''
            is_email_first = True
            address = get_customer()
        
            
            '''바로 아래 for-loop부터 각 프레임(0.3초?)별로 데이터를 저장 & 업데이터 하기 위한 딕셔너리 타입 '''
            frame_List=dict()
            target_List=dict()
            
            '''TARGET_OBJECT  '''
            t_email_before = ''
            t_db_before = '' # <- db 시간 데이터 추가 
            
            

            # Dataloader
            bs = 1
            if webcam:
                show_vid = check_imshow(warn=True)
                dataset = LoadStreams(
                    source,
                    imgsz=imgsz,
                    stride=stride,
                    auto=pt,
                    transforms=getattr(model.model, 'transforms', None),
                    vid_stride=vid_stride
                )
                bs = len(dataset)
            else:
                dataset = LoadImages(
                    source,
                    imgsz=imgsz,
                    stride=stride,
                    auto=pt,
                    transforms=getattr(model.model, 'transforms', None),
                    vid_stride=vid_stride
                )
            vid_path, vid_writer, txt_path = [None] * bs, [None] * bs, [None] * bs
            model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup

            # Create as many strong sort instances as there are video sources
            tracker_list = []
            
            for i in arange(bs): 
                tracker = create_tracker(tracking_method, tracking_config, reid_weights, device, half)
                tracker_list.append(tracker, )
                if hasattr(tracker_list[i], 'model'):
                    if hasattr(tracker_list[i].model, 'warmup'):
                        tracker_list[i].model.warmup()
            outputs = [None] * bs

            # Run tracking
            #model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
            seen, windows, dt = 0, [], (Profile(), Profile(), Profile(), Profile())
            curr_frames, prev_frames = [None] * bs, [None] * bs
            
            for frame_idx, batch in enumerate(dataset):
            
                    path, im, im0s, vid_cap, s = batch
                    visualize = increment_path(save_dir / Path(path[0]).stem, mkdir=True) if visualize else False
                    with dt[0]:
                        im = torch.from_numpy(im).to(device)
                        im = im.half() if half else im.float()  # uint8 to fp16/32
                        im /= 255.0  # 0 - 255 to 0.0 - 1.0
                        if len(im.shape) == 3:
                            im = im[None]  # expand for batch dim

                    # Inference
                    with dt[1]:
                        preds = model(im, augment=augment, visualize=visualize)

                    # Apply NMS
                    with dt[2]:
                        if is_seg:
                            masks = []
                            p = non_max_suppression(preds[0], conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det, nm=32)
                            proto = preds[1][-1]
                        else:
                            p = non_max_suppression(preds, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
                    
                    # Process detections
                    for i, det in enumerate(p):  # detections per image
                        
                        '''
                        이 for-loop은 한 프레임 안의 각각 개체를 관리하는데 
                        아래 리스트에서는 [4, 'military drone', '2023-03-09 18:36:11.50'] 
                        <- 이런식으로 트래킹번호, 라벨이름, 디텍팅된 시간을 저장
                        ''' 
                        
                        individual_List=[]
                        
                        seen += 1
                        if webcam:  # bs >= 1
                            p, im0, _ = path[i], im0s[i].copy(), dataset.count
                            p = Path(p)  # to Path
                            s += f'{i}: '
                            txt_file_name = p.name
                            save_path = str(save_dir / p.name)  # im.jpg, vid.mp4, ...
                        else:
                            p, im0, _ = path, im0s.copy(), getattr(dataset, 'frame', 0)
                            p = Path(p)  # to Path
                            # video file
                            if source.endswith(VID_FORMATS):
                                txt_file_name = p.stem
                                save_path = str(save_dir / p.name)  # im.jpg, vid.mp4, ...
                            # folder with imgs
                            else:
                                txt_file_name = p.parent.name  # get folder name containing current img
                                save_path = str(save_dir / p.parent.name)  # im.jpg, vid.mp4, ...
                        curr_frames[i] = im0

                        txt_path = str(save_dir / 'tracks' / txt_file_name)  # im.txt
                        s += '%gx%g ' % im.shape[2:]  # print string
                        imc = im0.copy() if save_crop else im0  # for save_crop

                        annotator = Annotator(im0, line_width=line_thickness, example=str(names))
                        
                        if hasattr(tracker_list[i], 'tracker') and hasattr(tracker_list[i].tracker, 'camera_update'):
                            if prev_frames[i] is not None and curr_frames[i] is not None:  # camera motion compensation
                                tracker_list[i].tracker.camera_update(prev_frames[i], curr_frames[i])

                        if det is not None and len(det):
                            if is_seg:
                                shape = im0.shape
                                # scale bbox first the crop masks
                                if retina_masks:
                                    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], shape).round()  # rescale boxes to im0 size
                                    masks.append(process_mask_native(proto[i], det[:, 6:], det[:, :4], im0.shape[:2]))  # HWC
                                else:
                                    masks.append(process_mask(proto[i], det[:, 6:], det[:, :4], im.shape[2:], upsample=True))  # HWC
                                    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], shape).round()  # rescale boxes to im0 size
                            else:
                                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()  # rescale boxes to im0 size

                            # Print results
                            for c in det[:, 5].unique():
                                n = (det[:, 5] == c).sum()  # detections per class
                                s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                            # pass detections to strongsort
                            with dt[3]:
                                outputs[i] = tracker_list[i].update(det.cpu(), im0)
                            
                            # draw boxes for visualization
                            if len(outputs[i]) > 0:
                                
                                if is_seg:
                                    # Mask plotting
                                    annotator.masks(
                                        masks[i],
                                        colors=[colors(x, True) for x in det[:, 5]],
                                        im_gpu=torch.as_tensor(im0, dtype=torch.float16).to(device).permute(2, 0, 1).flip(0).contiguous() /
                                        255 if retina_masks else im[i]
                                    )
                                
                                for j, (output) in enumerate(outputs[i]):
                                    # partial_List=[]
                                    bbox = output[0:4]
                                    id = output[4]
                                    cls = output[5]
                                    conf = output[6]
                                    
                                    '''
                                    Step 1. 각각 라벨의 정보(라벨명, detecting된 시간)을 individual_list에 넣어서 보냄
                                    
                                    ex) 현재 이런 식으로 저장됨
                                    [[4, 'bird', '2023-03-09 18:36:11.50'], [3, 'military drone', '2023-03-09 18:36:11.50'], [2, 'military drone', '2023-03-09 18:36:11.50'], [1, 'military drone', '2023-03-09 18:36:11.50']]
                                    '''
                                    
                                    tracking_index = int(id)                 
                                    tracking_object = names[int(cls)] 
                                    
                                    # send_database에서 현재 시간 정보를 얻어옴
                                    current_time = get_current_time()
                                    individual_List.append([tracking_index, tracking_object, current_time])
                                    
                                    if save_txt:
                                        # to MOT format
                                        bbox_left = output[0]
                                        bbox_top = output[1]
                                        bbox_w = output[2] - output[0]
                                        bbox_h = output[3] - output[1]
                                        # Write MOT compliant results to file
                                        with open(txt_path + '.txt', 'a') as f:
                                            f.write(('%g ' * 10 + '\n') % (frame_idx + 1, id, bbox_left,  # MOT format
                                                                        bbox_top, bbox_w, bbox_h, -1, -1, -1, i))

                                    if save_vid or save_crop or show_vid:  # Add bbox/seg to image
                                        c = int(cls)  # integer class
                                        id = int(id)  # integer id
                                        label = None if hide_labels else (f'{id} {names[c]}' if hide_conf else \
                                            (f'{id} {conf:.2f}' if hide_class else f'{id} {names[c]} {conf:.2f}'))
                                        color = colors(c, True)
                                        annotator.box_label(bbox, label, color=color)
                                        
                                        if save_trajectories and tracking_method == 'strongsort':
                                            q = output[7]
                                            tracker_list[i].trajectory(im0, q, color=color)
                                        if save_crop:
                                            txt_file_name = txt_file_name if (isinstance(path, list) and len(path) > 1) else ''
                                            save_one_box(np.array(bbox, dtype=np.int16), imc, file=save_dir / 'crops' / txt_file_name / names[c] / f'{id}' / f'{p.stem}.jpg', BGR=True)
                            
                            '''
                            이제 각 라벨별 데이터를 frame_List에 최종적으로 입력 및 
                            individaul_List에 저장된 데이터를 clear함
                            '''
                            
                            
                            for numb_track, name_track, tracked_time in individual_List:
                                if numb_track not in list(frame_List.keys()):
                                    frame_List[numb_track] = [name_track, tracked_time, tracked_time]  
                                    
                                    if target_object == name_track:          
                                        target_List[numb_track] = [name_track, tracked_time, tracked_time]        
                                                              
                                elif numb_track in list(frame_List.keys()):
                                    tmp_val = frame_List[numb_track]
                                    if len(tmp_val) == 4:
                                        frame_List[numb_track] = [name_track, tmp_val[2], tracked_time]
                                    else:
                                        frame_List[numb_track][2] = tracked_time
                                        
                                    if numb_track in list(target_List.keys()):
                                        tmp_target_val = target_List[numb_track]
                                        if len(tmp_target_val) == 4:
                                            target_List[numb_track] =  [name_track, tmp_target_val[2], tracked_time]
                                        else:
                                            target_List[numb_track][2] = tracked_time
                            
                            individual_List.clear()
                            
                        else:
                            pass
                            #tracker_list[i].tracker.pred_n_update_all_tracks()
                    
                        # Stream results
                        im0 = annotator.result()
                        img = cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (761, 511))

                        if show_vid:
                            h, w, ch = img.shape
                            bytesPerLine = ch * w
                            qImg = QImage(img.data, w, h, bytesPerLine, QImage.Format_RGB888)
                            pixmap = QPixmap.fromImage(qImg)
                            self.frame.setPixmap(pixmap)    
                            self.frame.setContentsMargins(5,5,0,0)
                            self.frame.resize(pixmap.width(), pixmap.height())
                            QtWidgets.QApplication.processEvents()
                        
                        

                        # Save results (image with detections)
                        if save_vid:
                            if vid_path[i] != save_path:  # new video
                                vid_path[i] = save_path
                                if isinstance(vid_writer[i], cv2.VideoWriter):
                                    vid_writer[i].release()  # release previous video writer
                                if vid_cap:  # video
                                    fps = vid_cap.get(cv2.CAP_PROP_FPS)
                                    w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                    h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                                else:  # stream
                                    fps, w, h = 30, im0.shape[1], im0.shape[0]
                                save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                                vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                            vid_writer[i].write(im0)
                        
                        if send_DB and is_db_first == True:
                            if len(frame_List)>=1:      
                                is_db_first = False 
                                t_db_before =  datetime.now()       
                                # 이때 DB로 데이터 보내기! 
                                frame_List = update_Format(frame_List)
                                th2 = Process(target = DB_process(frame_List))
                                th2.start()
                                th2.terminate()                        
                        
                        if send_DB and is_db_first == False:                            
                            if len(frame_List)>=1:
                                now_DB = datetime.now()     
                                result = now_DB.second - t_db_before.second
                                result = cal_abs(result)
                                
                                if result >= send_DB_term: 
                                    frame_List = remove_error(frame_List, current_time) # 중복 제거 
                                    frame_List = update_Format(frame_List)
                                    th3 = Process(target = DB_process(frame_List))
                                    th3.start()
                                    th3.terminate()
                                    t_db_before =  datetime.now()      
                                    frame_List = update_List(frame_List, current_time)
                            else:
                                pass 
                                
                        if send_EMAIL and is_email_first == True: 
                            if len(target_List)>=1:
                                t_email_before = current_time 
                                # cpu_count = multiprocessing.cpu_count()
                                # print('---cpu_count: ', cpu_count)
                                th4 = Process(target = send_alarm(target_object,is_email_first,len(target_List), t_email_before, current_time, address))
                                th4.start()
                                th4.terminate()
                                is_email_first = False 
                            else:
                                pass 
                            
                        if send_EMAIL and is_email_first == False:                             
                            if len(target_List) >= 1:                                
                                t_cal = calculate_time_min(t_email_before, current_time)                                
                                if t_cal >= send_EMAIL_term:
                                    target_List = remove_error(target_List, current_time)
                                    # cpu_count = multiprocessing.cpu_count()
                                    # print('---cpu_count: ', cpu_count)
                                    th5 = Process(target = send_alarm(target_object,is_email_first,len(target_List), t_email_before, current_time, address))
                                    th5.start()
                                    th5.terminate() 
                                    target_List= update_List(target_List, current_time)
                                    t_email_before = current_time
                                      
                                else:
                                    pass 
                            else:
                                pass 
                            
                        if self.isCamOn == False:
                            
                            return 
                            
                        else: pass
                    
                        print(frame_List)
                        prev_frames[i] = curr_frames[i]
                        

                            
                        
                    # # Print total time (preprocessing + inference + NMS + tracking)
                    # LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}{sum([dt.dt for dt in dt if hasattr(dt, 'dt')]) * 1E3:.1f}ms")

           
    def parse_opt(self):
            parser = argparse.ArgumentParser()
            parser.add_argument('--yolo-weights', nargs='+', type=Path, default=WEIGHTS / 'best.pt', help='model.pt path(s)')
            parser.add_argument('--reid-weights', type=Path, default=WEIGHTS / 'osnet_x0_25_msmt17.pt')
            parser.add_argument('--tracking-method', type=str, default='ocsort', help='strongsort, ocsort, bytetrack, botsort')
            parser.add_argument('--tracking-config', type=Path, default=None)
            parser.add_argument('--source', type=str, default='0', help='file/dir/URL/glob, 0 for webcam')  
            parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
            parser.add_argument('--conf-thres', type=float, default=0.7, help='confidence threshold')
            parser.add_argument('--iou-thres', type=float, default=0.2, help='NMS IoU threshold')
            parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
            parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
            parser.add_argument('--show-vid', action='store_true',default=True, help='display tracking video results')
            parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
            parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
            parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
            parser.add_argument('--save-trajectories', action='store_true', help='save trajectories for each track')
            parser.add_argument('--save-vid', action='store_true',default=False, help='save video tracking results')
            parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
            # class 0 is person, 1 is bycicle, 2 is car... 79 is oven
            parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
            parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
            parser.add_argument('--augment', action='store_true', help='augmented inference')
            parser.add_argument('--visualize', action='store_true', help='visualize features')
            parser.add_argument('--update', action='store_true', help='update all models')
            parser.add_argument('--project', default=ROOT / 'runs' / 'track', help='save results to project/name')
            parser.add_argument('--name', default='exp', help='save results to project/name')
            parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
            parser.add_argument('--line-thickness', default=2, type=int, help='bounding box thickness (pixels)')
            parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
            parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
            parser.add_argument('--hide-class', default=False, action='store_true', help='hide IDs')
            parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
            parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
            parser.add_argument('--vid-stride', type=int, default=1, help='video frame-rate stride')
            parser.add_argument('--retina-masks', action='store_true', help='whether to plot masks in native resolution')
            parser.add_argument('--send_DB', action='store_true', default=True, help=' T/F send date to DB')
            parser.add_argument('--send_DB_term', action='store_true', default=5, help='term to send data to DB')
            parser.add_argument('--send_EMAIL', action='store_true', default=True, help='T /F send date to EMAIL')
            parser.add_argument('--send_EMAIL_term', action='store_true', default=5, help='term to send EMAIL')
            parser.add_argument('--target_object', action='store_true', default='military drone', help='Target object to count')
            opt = parser.parse_args()
            opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
            opt.tracking_config = ROOT / 'trackers' / opt.tracking_method / 'configs' / (opt.tracking_method + '.yaml')
            print_args(vars(opt))
            return opt

################################################################################################################

'''2번 기능 페이지'''
class email_form(QDialog,QWidget,form_email):
    def __init__(self):
        super(email_form,self).__init__()
        back_Image = QImage("./pics/background.png")
        size_Image = back_Image.scaled(QSize(1028, 560))
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap(size_Image))) # <= 원하시는 사진
        self.setPalette(palette)        
        
        self.initUi()
        self.show()

        print(self.info_comboBox.currentText(), '모드 입니다.')
        self.info_comboBox.currentIndexChanged.connect(self.printShtname)

    def initUi(self):
        self.setupUi(self)
        '''버튼 아이콘'''
        # enter
        capture_pixmap = QStyle.StandardPixmap.SP_DialogApplyButton
        capture_icon = myWindow.style().standardIcon(capture_pixmap)
        self.enter_pushButton.setIcon(capture_icon)

        # exit
        exit_pixmap = QStyle.StandardPixmap.SP_MessageBoxCritical
        exit_icon = myWindow.style().standardIcon(exit_pixmap)
        self.exit_pushButton.setIcon(exit_icon)
        
    '''CUSTOMER_TABLE 연결'''
    def connect_table(self):
        from mysql.connector import connection
        conn = connection.MySQLConnection(
            user     = USER,
            password = PASSWORD,
            host     = HOST,
            database = DATABASE
            )
        return conn

    '''info 입력/검색/삭제 부분 업데이트 중'''
    def reset(self):
        self.id_text.clear()
        self.name_text.clear()
        self.email_text.clear()  

    def printShtname(self): # 콤보박스 상태 변경 시 터미널에 출력하는 기능 함수.
        print(self.info_comboBox.currentText(),'모드 입니다.')

    def add_info(self): 
        self.id      = self.id_text.text()    # 아이디
        self.name    = self.name_text.text()  # 이름
        self.email   = self.email_text.text() # 이메일
        self.fn_type = self.info_comboBox.currentText()  # 콤보 박스: 입력, 검색, 삭제    
        set_flag = False

        ## 1. 검색
        if self.fn_type == ' SELECT':
            if self.id or self.name or self.email:
                select_count = self.countData()
                if select_count > 0 :
                    set_flag = True
                    id_list, name_list, email_list = self.SelectData()
                    QMessageBox.information(self, "Select 결과", f"{select_count}개의 데이터를 출력합니다.")
                else:
                    QMessageBox.critical(self, "입력 오류", "입력하신 정보의 데이터가 없습니다")
            else:
                QMessageBox.critical(self, "입력 오류", "정보를 입력해주세요!")
        
        ## 2. 입력
        elif self.fn_type == ' INSERT':
            if self.id and self.name and self.email:
                set_flag = True
                self.InsertData()
            # close event 처럼 하나 필요 !!!
            else:
                QMessageBox.critical(self, "입력 오류", "모든 정보를 입력해주세요!")
                print("모든 정보를 입력해주세요!")

        ## 3. 삭제
        elif self.fn_type == ' DELETE':
            msg = '정말 삭제하시겠습니까?'
            buttonReply = QMessageBox.question(self, '삭제', msg, QMessageBox.Yes | QMessageBox.No)

            # 삭제 메세지에서 YES선택 시
            if buttonReply == QMessageBox.Yes:
                # 3개의 데이터 중 하나만이라도 존재하면
                if self.id and self.name and self.email:
                    delete_count = self.countData()
                    # delete할 행이 있다면
                    if delete_count > 0 :
                        set_flag = self.DeleteData()
                        QMessageBox.information(self, "Delete 결과", f"{delete_count}개의 데이터를 삭제합니다.")
                    # delete할 행이 없다면
                    else:
                        QMessageBox.critical(self, "입력 오류", "입력하신 정보의 데이터가 없습니다.\n데이터를 다시 확인 후 입력해주세요")
                else:
                    QMessageBox.critical(self, "입력 오류", "정보를 다시 입력해주세요!")     
            else: 
                buttonReply == QMessageBox.No
                QMessageBox.critical(self, "취소", "취소되었습니다!")
        ## info table에 입력할 데이터
        if set_flag:
            if self.fn_type == ' DELETE' or self.fn_type == ' INSERT':
                row = self.info_table.rowCount()
                self.info_table.insertRow(row)
                self.info_table.setItem(row, 0, QTableWidgetItem(self.fn_type + f" 완료"))
                self.info_table.setItem(row, 1, QTableWidgetItem(self.id))
                self.info_table.setItem(row, 2, QTableWidgetItem(self.name))
                self.info_table.setItem(row, 3, QTableWidgetItem(self.email))
            elif self.fn_type == ' SELECT':
                for index, item in enumerate(id_list):
                    row = self.info_table.rowCount()
                    self.info_table.insertRow(row)
                    self.info_table.setItem(row, 0, QTableWidgetItem(self.fn_type + f" {index+1} 완료"))
                    self.info_table.setItem(row, 1, QTableWidgetItem(id_list[index]))
                    self.info_table.setItem(row, 2, QTableWidgetItem(name_list[index]))
                    self.info_table.setItem(row, 3, QTableWidgetItem(email_list[index]))
        self.reset()

    '''CUSTOMER_TABLE 연결'''
    def countData(self):
        conn = self.connect_table()
        cur = conn.cursor()    
        # COUNT 문
        if self.fn_type == " SELECT":
            # 1 0 0
            if (len(self.id) != 0) and (len(self.name) == 0) and (len(self.email) == 0):
                SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}` WHERE `id` = '{str(self.id)}';'''
            # 0 1 0
            elif (len(self.id) == 0) and (len(self.name) != 0 ) and (len(self.email) == 0):
                SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}` WHERE `name` = '{str(self.name)}';'''
            # 0 0 1
            elif (len(self.id) == 0) and (len(self.name) == 0) and (len(self.email) != 0):
                SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}` WHERE `email` = '{str(self.email)}';'''
            # 1 1 0
            elif (len(self.id) != 0) and (len(self.name) != 0) and (len(self.email) == 0):
                SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}` WHERE `id` = '{str(self.id)}' AND `name`='{str(self.name)}';'''
            # 1 0 1
            elif (len(self.id) != 0) and (len(self.name) == 0) and (len(self.email) != 0):
                SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}` WHERE `id` = '{str(self.id)}' AND `email`='{str(self.email)}';'''
            # 0 1 1
            elif (len(self.id) == 0) and (len(self.name) != 0) and (len(self.email) != 0):
                SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}` WHERE `name` = '{str(self.name)}' AND `email`='{str(self.email)}';'''
            # 1 1 1
            elif (len(self.id) != 0) and (len(self.name) != 0) and (len(self.email) != 0):
                SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}` 
                WHERE `id` = '{str(self.id)}' AND `name`='{str(self.name)}' AND `email`='{str(self.email)}';'''

        elif self.fn_type == " DELETE":
            SQL_COUNT = f'''SELECT COUNT(*) FROM `{TABLE_CUSTOMER}`
            WHERE `id` = '{str(self.id)}' AND `name`='{str(self.name)}' AND `email`='{str(self.email)}';'''

        cur.execute(SQL_COUNT)
        count = cur.fetchone()[0]
        conn.commit()
        conn.close()

        return count

    ''' Select Data'''
    def SelectData(self):
        id_list, name_list, email_list = [], [], []
        conn = self.connect_table()
        cur = conn.cursor()
        # SELECT 문
        # 1 0 0
        if (len(self.id) != 0) and (len(self.name) == 0) and (len(self.email) == 0):
            SQL_SELECT = f'''SELECT * FROM `{TABLE_CUSTOMER}` WHERE `id` = '{str(self.id)}';'''
        # 0 1 0
        elif (len(self.id) == 0) and (len(self.name) != 0 ) and (len(self.email) == 0):
            SQL_SELECT = f'''SELECT * FROM `{TABLE_CUSTOMER}` WHERE `name` = '{str(self.name)}';'''
        # 0 0 1
        elif (len(self.id) == 0) and (len(self.name) == 0) and (len(self.email) != 0):
            SQL_SELECT = f'''SELECT * FROM `{TABLE_CUSTOMER}` WHERE `email` = '{str(self.email)}';'''
        # 1 1 0
        elif (len(self.id) != 0) and (len(self.name) != 0) and (len(self.email) == 0):
            SQL_SELECT = f'''SELECT * FROM `{TABLE_CUSTOMER}` WHERE `id` = '{str(self.id)}' AND `name`='{str(self.name)}';'''
        # 1 0 1
        elif (len(self.id) != 0) and (len(self.name) == 0) and (len(self.email) != 0):
            SQL_SELECT = f'''SELECT * FROM `{TABLE_CUSTOMER}` WHERE `id` = '{str(self.id)}' AND `email`='{str(self.email)}';'''
        # 0 1 1
        elif (len(self.id) == 0) and (len(self.name) != 0) and (len(self.email) != 0):
            SQL_SELECT = f'''SELECT * FROM `{TABLE_CUSTOMER}` WHERE `name` = '{str(self.name)}' AND `email`='{str(self.email)}';'''
        # 1 1 1
        elif (len(self.id) != 0) and (len(self.name) != 0) and (len(self.email) != 0):
            SQL_SELECT = f'''SELECT * FROM `{TABLE_CUSTOMER}` 
            WHERE `id` = '{str(self.id)}' AND `name`='{str(self.name)}' AND `email`='{str(self.email)}';'''

        cur.execute(SQL_SELECT)
        result = cur.fetchall()
        for i in result:
            id_list.append(i[1])
            name_list.append(i[2])
            email_list.append(i[3])

        conn.commit()
        conn.close()

        return id_list, name_list, email_list

    ''' Insert Data'''
    def InsertData(self):
        conn = self.connect_table()
        cur = conn.cursor()
        SQL_INSERT = f'''INSERT INTO `{TABLE_CUSTOMER}`(id, name, email) 
    VALUES ('{str(self.id)}', '{str(self.name)}', '{str(self.email)}');'''
        cur.execute(SQL_INSERT)
        conn.commit()
        conn.close()
        
    ''' Delete Data'''
    def DeleteData(self):
        conn = self.connect_table()
        cur = conn.cursor()

        SQL_DELETE = f'''DELETE FROM `{TABLE_CUSTOMER}` 
        WHERE `id` = '{str(self.id)}' AND `name`='{str(self.name)}' AND `email`='{str(self.email)}';'''
        cur.execute(SQL_DELETE)
        conn.commit()
        if cur.rowcount >= 1:
            conn.close()
            return True
        else:
            conn.close()
            return False

    '''X 버튼 누를 시 종료 재확인 메세지'''
    def closeEvent(self, QCloseEvent): # 오버라이딩 메소드
        ans = QMessageBox.question(self, "종료 확인","종료하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore() 
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myWindow = Ui_MainWindow()
    myWindow.show()
    
    '''상태표시줄'''
    # myWindow.statusBar()
    DATE = myWindow.date.toString(Qt.DefaultLocaleLongDate) + " "
    TIME = QTime.currentTime().toString()
    MESSAGE = " 위험비행물 감지시스템 동작 중...   "
    myWindow.statusBar().showMessage(MESSAGE + DATE + TIME)

    app.exec_()