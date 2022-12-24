# Day58. DL. Introduction of ML & DL

### - ML과 DL의 개념과 차이점
1. ML : 사람이 정한 모델, 특징 추출 방법 -> 데이터 기반 추론
    - 데이터 > INPUT > 특징추출 (인간의 개입 O) > 분류 > OUTPUT
2. DL : 인공신경망을 사용 -> 빅데이터에 유용
    - 데이터 > INPUT + 특징추출 (인간의 개입 X) > 분류 > OUTPUT

### - ML의 학습 방식
1. 지도 학습 : 정답지(label)가 있는 학습방법 -> features, label
2. 비지도 학습 : 정답지가 없는 학습방법 -> features only 

#### - 지도학습 (Supervised Learning)
1. 회귀 (Regression) : 한 가지의 값을 예측, 연속적(Continuous)
2. 분류 (Classification) : 그룹을 예측, 이산적(Discrete)

#### - 비지도학습 (Unsupervised Learning)
1. 군집화 (Clustering) : 정답 없이 그룹을 만들어가는 과정

<hr>

## - 선형 분류 (Linear Classification)
1. 단순 선형 회귀 분석 : Weight이 1개, bias 1개
2. 다중 선형 회귀 분석 : Weight이 n개, bias 1개
- 단 XOR에서 선형 분류 불가 !!!

### 손실함수 (Loss function)
- Loss function이 최소화 하기 위한 최적화(optimization)가 진행된다.
- 대표적인 Loss function
    1. SVM Loss
    2. Cross-Entropy Loss -> <strong>softmax</strong> 함수

<hr>

### - 정규화, 정칙화 (Regulization)
- 모델이 학습 데이터(training data)에 의해 지나치게 훈련이 잘되는 overfiting 이슈를 해결하기 위해 사용

#### - Overfiting 잡는 방법
1. Traing Data 개체 수를 늘림
2. Regulization(규제, 정칙화, 정규화) : 
    ex. L1 (LASSO), L2 (Ridge), Elastic Net(Ridge와 LASSO를 합친 것) 
3. Dropout : 랜덤으로 뉴런을 중지시킴


