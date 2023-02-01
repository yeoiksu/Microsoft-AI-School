import mmcv
import torch

from mmdet.apis import init_detector, inference_detector
from mmdet.datasets.builder import DATASETS
from mmdet.datasets.coco import CocoDataset
from mmdet.datasets import build_dataset
from mmdet.models import build_detector
from mmdet.apis import set_random_seed
from mmdet.apis import train_detector
# from mmdet.utils import collect_env, get_root_logger, setup_multi_processes
# from mmcv.runner import get_dist_info, init_dist
from mmcv import Config

# Dataset register : 등록해야 강제로 바꿀 수 있음
@DATASETS.register_module(force=True)
class WineLabelsDataset(CocoDataset) :  # Coco Dataset을 상속받음
    # Class 이름 변경 필요
    CLASSES = ('wine-labels', 'AlcoholPercentage',
               "Appellation AOC DOC AVARegion",
               "Appellation QualityLevel",
               "CountryCountry",
               "Distinct Logo",
               "Established YearYear",
               "Maker-Name",
               "Organic",
               "Sustainable",
               "Sweetness-Brut-SecSweetness-Brut-Sec",
               "TypeWine Type",
               "VintageYear",
               )

### 경로 configs >> dynamic_rcnn >> py script
config_file = "./configs/dynamic_rcnn/dynamic_rcnn_r50_fpn_1x_coco.py"
cfg = Config.fromfile(config_file)
# print(cfg.text) 하여 마지막 output을 수정해줘야함
# 가장 대중적으로 사용하는 모델:
# cascade_rcnn (엄청 무거움), dynamic rcnn, faster rcnn : detection 용도
# mask-rcnn : segementation 용도

# Optimizer learning rate setting
# sing GPU -> 0.0025
# cfg.optimizer.lr = 0.02/8  # 8개 gpu
cfg.optimizer.lr = 0.0025  # 1개 값

# dataset setting
cfg.dataset_type = "WineLabelsDataset"  # 위의 Dataset과 이름이 같아야함
cfg.data_root = "./dataset"

# train, val test dataset >> type data root ann file img_prefix setting
# configs >> base >> datasets >> coco_detection.py
# train
cfg.data.train.type = "WineLabelsDataset"
cfg.data.train.ann_file = "./dataset/train/_annotations.coco.json"
cfg.data.train.img_prefix = "./dataset/train/"

# val
cfg.data.val.type = "WineLabelsDataset"
cfg.data.val.ann_file = "./dataset/valid/_annotations.coco.json"
cfg.data.val.img_prefix = "./dataset/valid/"

# test
cfg.data.test.type = "WineLabelsDataset"
cfg.data.test.ann_file = "./dataset/test/_annotations.coco.json"
cfg.data.test.img_prefix = "./dataset/test/"

# class number
# 위에 작성한 
# config_file = "./configs/dynamic_rcnn/dynamic_rcnn_r50_fpn_1x_coco.py"
# 타고 들어가서 확인 가능
cfg.model.roi_head.bbox_head.num_classes = 13

# small obj -> change anchor -> df : size 8 -> size 4
cfg.model.rpn_head.anchor_generator.scales = [4]

# pretrained call
cfg.load_from = "./dynamic_rcnn_r50_fpn_1x-62a3f276.pth"

# train model save dir 모델저장 경로
cfg.work_dir = "./work_dirs/0130"

# lr hyp setting
cfg.lr_config.warmup = None
cfg.log_config.interval = 10

# cocodataset evaluation type = bbox 
# mAP iou threshold 0.5 ~ 0.95

# 주로 bbox 타입, or mAP 타입
# 보통 10 epoch 해서 train 상태 확인
cfg.evaluation.metric = 'bbox'
cfg.evaluation.interval = 10
cfg.checkpoint_config.interval = 10

# parameter setting
# 8 x 12 -> 96  >> 12는 scheduler에서 gpu 개수 8개 !!
cfg.runner.max_epochs = 88  # 보통 88 최대 96
cfg.seed = 777
cfg.data.samples_per_gpu = 6  # 고정 batch size
cfg.data.workers_per_gpu = 2  # 고정 num_work
print("cfg.data >>" , cfg.data)
cfg.gpu_ids = range(1)
cfg.device = "cuda"
set_random_seed(777, deterministic=False)
print("cfg info show ", cfg.pretty_text)

datasets = [build_dataset(cfg.data.train)]
print("dataset[0]", datasets[0])

# datasets[0].__dict__ variables key val
datasets[0].__dict__.keys()

model = build_detector(cfg.model, train_cfg=cfg.get("train_cfg"),
                       test_cfg=cfg.get('test_cfg'))
model.CLASEES = datasets[0].CLASSES  # class 개수 확인
print(model.CLASEES)

if __name__ == '__main__' :
    train_detector(model, datasets,cfg,distributed=False, validate=True)

'''
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.293
 Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=1000 ] = 0.434
 Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=1000 ] = 0.339
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=1000 ] = 0.177
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=1000 ] = 0.282
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=1000 ] = 0.230
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.473
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=300 ] = 0.473
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=1000 ] = 0.473
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=1000 ] = 0.297
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=1000 ] = 0.480
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=1000 ] = 0.423
'''