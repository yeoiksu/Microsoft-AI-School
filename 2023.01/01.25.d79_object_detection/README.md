# Day79. Object Detection

### 1. data.yaml 생성 
    1. 폴더 root : data >> data.yaml
    2. train, vallid path 설정 
    2. names로 label명과 label number 설정(num_class 삭제됨)
#### ex ) data.yaml 
```
train: ./dataset/train/images
val: ./dataset/valid/images

# Classes
names:
  0: big bus
  1: big truck
  2: bus-l-
  3: bus-s-
  4: car
  5: mid truck
  6: small bus
  7: small truck
  8: truck-l-
  9: truck-m-
  10: truck-s-
  11: truck-xl-
```

### 2. 


### 3. inf.py 생성
    1. 폴더 root : utils >> inf.py 파일 생성
    2. model명 먼저 설정 (model path는 runs >> train에서 확인 가능)
    3. inference 설정
    4. result(bbox, label_num) 설정
    5. 
#### ex ) inf.py
```

``` 

