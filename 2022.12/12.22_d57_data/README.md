# Day57. Data. Custom Dataset & Image Augmentation & Train/Test

#### ex01. 데이터 수집 (Web Crawling)
- kewords.txt 파일에서 키워드를 읽고 구글 이미지에 키워드를 자동 검색 후 이미지 저장 (대략 각 키워드 100장)
- keyword.txt (banana, kiwi, orange, pineapple, watermelon 5가지)

#### ex02. Data Split
- ex01에서 저장한 이미지 데이터를 읽고 train과 validation 데이터를 9:1 비율로 분리
- 분리 후 train폴더와 val 폴더에 이미지 저장

#### ex03. Image Pretreatment
- expand2square() 함수를 사용해 기존 이미지를 정사각형화 후, padding하여 400 x 400 사이즈로 Resize -> dataset/images 폴더에 저장
- 각 카테고리 별 데이터의 수를 출력 (총 460장)

#### ex04. CustomDataset 생성
-	data/train에 있는 5개 카테고리의 모든 이미지 데이터를 불러와 리스트 한 후, 이미지에 해당하는 label 값을 읽어와 image, label 데이터 반환

#### ex05. Main
- 서로 다른 augmentation transform 모델을 불러오고 훈련이 진행
- hy_parameter.py에서 parameter 값을 가져옴
- transform_list.py 에서 image augmentation 리스트를 불러와 훈련 모두 실행
- utils.py의 train() 함수를 사용하여 모델 훈련 후 model save 폴더에 pt 파일 저장


