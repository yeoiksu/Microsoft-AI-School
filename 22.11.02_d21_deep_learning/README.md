# Day21. DL. Deep Learning & Convolutional Neural Network

## 1. Azure Machine Learning (기계 학습)
### 1.1. "Azure Machine Learning" 만들기
    [1]  + 리소스 만들기
    [2] 'Azure Machine Learning' 만들기 선택
    [3] <기본> 이름, 지역 설정
    [4] 검토 + 만들기
    [5] 생성 이후 리소스로 이동
    [6] 아래의 'Launch Studio' 클릭
### 1.2. "Azure Machine Learning" 사용하기
    1) "Notebooks" 사용하기
        [1] ipynb 노트북 파일 생성
        [2] 상단의 'Computer instance:'의 햄버거에서 'Create compute instance' 선택 후 생성

## 2. DSVM, Data Science Virtual Machine - Windows 2019
### 2.1. DSVM 가상머신 만들기 
    [1]  + 리소스 만들기
    [2] 'DSVM' 만들기 선택
    [3] <기본> 이름, 지역 설정
    [4] 검토 + 만들기
    [5] 생성 이후 리소스로 이동
    [6] 왼쪽 상단에 '연결' (3가지 옵션) 선택
    [7] 'RDP' 선택 >> 'RDP 다운로드'
    
### 2.2. DSVM 환경 setting하기
    [1] Kaggle에서 'cats and dogs' dataset 다운로드하기
    [2] 가상머신에서 jupyter 실행하기
    [3] Document안에 폴더 생성 이후 'cats and dogs' dataset과 ipynb파일 추가

## 3. Convolutional Neneural Network (합성곱)
- 이미지를 인식하기 위해 패턴을 찾는데 유용
- 자율주행, 얼굴 인식과 같은 객체인식에 자주 샤용
### 3.1. DVSM에서 Dog와 Cat 구분하는 CNN 모델 구현하기