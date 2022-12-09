# Day13. Data Preprocessing & Azure

## I. Data Preprocessing
<br>

### Data 분석을 용이하게 하기 위해 고치는 작업
    - 전체 프로젝트의 80~90% 소모 (>>알고리즘 구현)
    - 데이터 자체가 잘못된 경우 실험 결과가 개선 X

### 대표적인 Data Preprocessing 기법
    1. Scaling (스케일링)
    2. Sampling (샘플링)
    3. Dimensionality Reduction (차원의 축소)
    4. Categorical Variable to Numeric Variable ()
------
### 1. Scaling (스케일링)
    - 변수의 크기가 너무 크고나 작아 결과에 미치는 영향력이 작을 때 변수의 크기를 일정하게 맞춰주는 작업
    - sklearn의 MinMaxScaler() 내장함수 fit_transform() 사용
    - 대표적인 2가지 방법
        [1] Min-Max scaling
        [2] Standard Scaling : Z-score Normalization을 사용
#### 1.1. Min-Max Scaling    
    - 값의 범위가 0 ~ 1 사이로 변경 : 단위 크기와 상관없이 중요한 영향력을 가질 수 있게 함
    - 전체적인 수치를 '1'을 기준으로 비율이 조정 : 같은 조건에서 학습 될 수 있게 함
#### 1.2. Z-scaore Normalization을 이용한 standard scaling
    - 위의 Min-Max Scaling과 비슷
    - 평균 0, 표준편차 1
------
### 2. Sampling (샘플링)
    - 데이터의 불균형 문제를 해결하기 위함 (한쪽으로 치우치지 않게 해줌)
    - 데이터를 임의로 추가/삭제 하므로 risk(편향된 데이터 or 중요한 속성 삭제) 발생 가능
    - 대표적인 2가지 방법
        [1] Oversampling  : 적은 클래스의 수를 증가
        [2] UnderSampling : 많은 클래스의 수를 감소
        [3] SMOTHE
#### 2.1. Oversampling
    - Random으로 추가
    - Overfitting 이슈가 발생 가능 (과접합) : 편향된 데이터 생성 가능
#### 2.2. UnderSampling
    - Random으로 삭제
    - 중요한 속성을 가진 data를 삭제 가능
#### 2.3. SMOTHE
    - Oversampling 과 Undersampling의 단점을 극복한 sampling 방법
    - 데이터 손실 없이 과적합 문제를 해결할 수 있음
------
### 3. Dimensionality Reduction (차원의 축소)
    - 데이터의 차원이 불필요하게 큰 경우, 필요 ㅇ덦는 변수를 제거하고 과적합을 방지하기 위해 차원을 축소함
    - 차원이 크면 해석하는데 어려움이 있어 축소하는 경우도 있음
    - 대표적인 방법
        [1] PCA (Principal Component Analysis : 주성분 분석)
------
### 4. Categorical Variable to Numeric Variable
    - 범주형(Categorical) 데이터는 주로 문자열로 표시
    - 컴퓨터가 data를 활용하고 학습하기 위해서 data를 모두 수치화 필요

<br>


# II. Azure 교육
### 1. Azure Virtual Machine에서 Window 실행하기 ([link](https://learn.microsoft.com/ko-kr/azure/virtual-machines/windows/quick-create-portal))
    [1] 리소스그룹 선택 후 '+ 만들기'
    [2] '가상 머신' 만들기 선택
    [3] <기본 사항>
        가상머신이름 >> 사용자 임의로 설정
        이미지 >> "Windows Sever 2022" 선택
        관리자계정 >> "이름", "암호" 설정 후
        인바운드 포트 >> HTTP(80) 추가
        검토 + 만들기
    [4] Window에 "원격 데스크톱 연결"을 검색후 Azure의 "공용 IP 주소" 입력
    [5] 이전에 가상머신 생성 시 입력했던 "이름"과 "암호" 입력
    [6] 가상 머신에서 Window 연결 및 생성완료
    [7] 가상 머신의 Window에서 powershell 실행 후 "Install-WindowsFeature -name Web-Server -IncludeManagementTools" 입력
    [8] chrome열고 "공용ip주소" 입력 시 사이트가 뜨면 성공

### 2. Azure Virtual Machine에서 Ubuntu 실행하기 ([link](https://learn.microsoft.com/ko-kr/azure/virtual-machines/linux/quick-create-portal))
    [1] 리소스그룹 선택 후 '+ 만들기'
    [2] '가상 머신' 만들기 선택
    [3] 기본 사항 >> 인스턴스 detail
        가상머신이름 : 설정
        이미지 : "Ubuntu 18.04" 선택
        인증유형 : "SSH 공개 키" 설정
        관리자계정 : "이름", "암호" 설정 후
        인바운드 포트 >> HTTP(80) 추가
        검토 + 만들기
    [4] CMD를 실행시킨 후 ssh "가상머신이름"@"공용ip주소" >> yes >> 비밀번호 입력
    [6] 가상 머신에서 Ubuntu 연결 완료
    [7] cmd에서 "sudo apt-get -y update" 
                "sudo apt-get -y install nginx" 입력
    [8] chrome열고 "공용ip주소" 입력 시 사이트가 뜨면 성공
        

### 3. Azure에서 가상머신 확장 집합 만들기 ([link](https://learn.microsoft.com/ko-kr/azure/virtual-machine-scale-sets/quick-create-portal))