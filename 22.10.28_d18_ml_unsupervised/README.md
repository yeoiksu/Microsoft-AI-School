# Day18. ML. Scikit Learn (Supervised Learning - Classification)

## 1. Classification
    1. Logistic Regression
    2. Support Vector Machine
    3. Decision Tree
    4. Random Forest

## II. Unsupervised Learning
### 1. Clustering
    1) k-Means
    2) PCA
    3) Hierarchical Clustering

## III. Microsoft Azure 실습
### 1. Azure에서 가상머신 확장 집합 만들기 ([관련 링크](https://learn.microsoft.com/ko-kr/azure/virtual-machine-scale-sets/quick-create-portal))
#### 1) "Load Balance" (부하 분산 장치) 만들기
    [1]  + 리소스 만들기
    [2] 'Load Balance (부하 분산 장치)' 만들기 선택
    [3] <프런트 엔드 IP 구성> 
        - 이름 설정, 공용 IP주소 "새로 만들기" >> 이름 설정
    [4] 검토 + 만들기
#### 2) "Virtual Machine Scale Set (가상 머신 확장 집합)" 만들기
    [1]  + 리소스 만들기
    [2] '가상 머신 확장 집합' 만들기 선택
    [3] <기본사항>
        - 이미지 >> 'Ubuntu' 설정
        <네트워킹>
        - '부하 분산 장치 사용' 체크 (위에서 만든 load balance 사용을 위해)
        - '부하 분산 장치 선택'에서 1)에서 만든 load balance 선택
        - '백 엔드 풀 선택'에서 새로 만들기 하여 이름 설정
    [4] 검토 + 만들기
#### 3) Instance 수 늘리기
    [1] 만들어진 "가상 머신 확장 집합" 리소스로 이동
    [2] '설정' >> '확장 중' >> '인스턴스 수' 조절 후 "저장" 클릭 
    [3] '설정' >> '인스턴스'에 가서 

## 2. Virtual Network (가상 네트워크)
#### 1) "Virtual Network" 만들기
    [1]  + 리소스 만들기
    [2] '가상 네트워크' 만들기 선택
    [3] <IP 주소>
        - IPv4 주소공간 >> ip 수정
        - 서브넷 추가 + >> 이름, 서브넷 주소 범위 설정 
    [4] <보안>
        - BastionHost >> 사용
        - 이름, 주소 공간, 공용IP주소 설정
        - Bastion이란 ? Virtual Network에 연결된 VM들과 연결을 보안/통제하기 위한 네트워크 
    [5] 검토 + 만들기
#### 2) "Virtual Machine" 만들고 "Virtual Network"와 연결하기
    [1]  + 리소스 만들기
    [2] '가상 네트워크' 만들기 선택
    [3] <기본사항>
        - Bastion을 만들었으면 '인바운드 포트 선택'을 설정해야함
        <네트워킹>
        - '가상 네트워크' : 1)에서 만들었던 Virtual Network와 연결
    [4] 검토 + 만들기
    [5] 위의 step을 한번 더 반복하여 VM2 만들면 Virtual Network안에 VM 1과 VM 2가 연결됨    
#### 3) "원격 데스크톱 연결"을 사용하여 "Virtual Machine" 연결 확인하기
    [1] "원격 데스크톱 연결"을 사용하여 VM 1, VM 2 연결
    [2] VM 1, VM 2의 Powershell을 실행시킨 후 아래의 명령어 입력
        " New-NetFirewallRule –DisplayName "Allow ICMPv4-In" –Protocol ICMPv4 "
    [3] VM1의 powershell에서 " ping VM2 ", VM2의 powershell에서 " ping VM1 "을 입력했을 때 잘되면 연결 성공  
    