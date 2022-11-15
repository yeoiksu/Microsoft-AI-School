# Day30. Microsoft Certification: DP 900 & Azure CLI
## 내용은 SECRET !!!
### 나만의 One Note에 작성

## 1. Azure Cosmos DB 
### 1.1. Azure Cosmos DB 만들기
    [1] "Azure Cosmos DB" 만들기 >> 코어(SQL) 권장
    [2] 기본 설정 이후 만들기
    [3] 리소스로 이동
    [4] "+ 컨테이너 추가" 선택 >> 정보 입력 후 생성
    [5] 왼쪽 tab의 "전역으로 데이터 복제" >> 읽기 지역 추가 >> "사용" 클릭하며 데이터 복제 가능

## 2. Azure CLI 생성
### 2.1. Azure CLI 생성
    [1] 먼저 "Windows 11" 가상환경을 생성
    [2] https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli 에서 "Azure CLI" Window 버전 다운로드
    [3] CMD에서 'az' 검색 후 결과가 나오면 설치 성공

### 2.2. Azure CLI 사용하여 AKS 배포하기 ([관련 링크](https://learn.microsoft.com/ko-kr/azure/aks/learn/quick-kubernetes-deploy-cli))
    1) 기본 명령어 & Setting
        [1] Login하고 정보 확인하기
            'az login'
        [2] 리소스 생성
            az group create --name RGTest37 --location eastus
            (이름, 지역)
        [3] 가상 네트워크 생성 
            az network vnet create --name labuser37vnet --resource-group RGTest37 --subnet-name labuser37subnet --address-prefixes 10.0.0.0/16 --subnet-prefixes 10.0.0.0/24        
            (가상네트워크, Vnet prefix, Subnet Prefix)
        [4] 가상 머신 생성
            az vm create --resource-group RGTest37 --name labuser37testvm --image UbuntuLTS --vnet-name labuser37vnet --subnet labuser37subnet --generate-ssh-keys
            (generate-ssh-keys: key를 만들면서 접속)
        [5] 리소스 그룹 삭제
            az group delete --name RGTest37 --yes
            (yes: 묻지도 말고 지워 !!) 

    2) Azure Container Registry & Azure Kubernetes Service 생성 후 배포하기
        [1] ACR 만들기
            az acr create --resource-group RG37 --name labuser37acr --sku Basic

        [2] AKS 만들기
            az aks create --resource-group RG37 --name labuser37aks --location eastus --attach-acr labuser37acr --generate-ssh-keys

        [3] AKS에 CLI 설치하기
            az aks install-cli

        [4] 접속에 필요한 인증
            az aks get-credentials --resource-group RG37 --name labuser37aks

        [5] 인증을 이용하여 작업, git 설치 이후 sample github clone
            git clone https://github.com/Azure-Samples/azure-voting-app-redis.git

        [6] 해당 파일로 이동
            cd azure-voting-app-redis
            cd azure-vote

        [7] Docker 이미지 파일 다운로드
            az acr build --image azure-vote-front:v1 --registry labuser37acr --file Dockerfile .

        [8] 파일 다운로드
            https://github.com/helm/helm/releases 에서 Windows로 다운 후
            압출 해제 후,
            helm파일을 C:\Users\winkey\azure-voting-app-redis\azure-vote 경로에 복붙

        [9] yaml파일 생성 (azure-vote-front.yml), 위의 경로에 저장 

            ``` yaml파일
            apiVersion: v2
            name: azure-vote-front
            description: A Helm chart for Kubernetes

            dependencies:
            - name: redis
                version: 14.7.1
                repository: https://charts.bitnami.com/bitnami

            ...
            # This is the version number of the application being deployed. This version number should be
            # incremented each time you make changes to the application.
            appVersion: v1
            
            ```
            copy azure-vote-front.yaml.txt azure-vote-front.yml

        [10] helm 생성 후 이동
            helm create azure-vote-front
            cd azure-vote-front
        
        [11] yaml파일 후 수정
            values.yaml

            - yaml파일 내용중에 수정할 부분
                repository: 1. nginx     -> labuser37acr/azure-vote-front
                            2. tag: ""   -> tag: "v1"
            service:
                type:       3. ClusterIP -> LoadBalancer
        
        [12] 파일 디렉토리 변경 후 helm 설치
            cd ..
            helm install azure-vote-front azure-vote-front/

        => Azure Portal >> 리소스그룹 >> aks파일 >> 왼쪽 tab의 "서비스 및 수신"에서 azure-vote-front가 생성되어 배포된 것을 확인 가능

### 2.3. WSL을 사용하여 Windows에 Linux 설치하기 ([관련 링크](https://learn.microsoft.com/ko-kr/windows/wsl/install))

<hr>