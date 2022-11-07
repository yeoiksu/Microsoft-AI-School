# Day22. Azure. Cloud & Docker & Kubernetes  
## Index.
1. [VM에서 Linux (Ubuntu)와 Docker 구현하기](#1-vm에서-linux-ubuntu와-docker-구현하기) <br>
    1.1. [Ubuntu Server 생성](#11-ubuntu-server-생성) <br>
    1.2. [Docker 설치 & 기본 setting](#12-docker-설치--기본-setting)<br>
    1.3. [Docker 기본 명령어](#13-docker-기본-명령어)<br>
    1.4. [Docker에 push 하기 ](#14-docker에-push-하기)<br>
    
2. [Kubernetes 사용하기](#2-kubernetes-사용하기)<br>
    2.1. [Minikube 다운받고 웹 통신하기](#21-Minikube-다운받고-웹-통신하기)<br>
    2.2. [yaml 파일 생성](#22-yaml-파일-생성-pod-deployment-service-pvc)<br>
<hr>

## 1. VM에서 Linux (Ubuntu)와 Docker 구현하기
### 1.1. Ubuntu Server 생성
    [1]  + 리소스 만들기
    [2] 'Ubuntu Server 22.04 LTS' 만들기 선택
    [3] <기본> 이름, 지역 설정
    [4] 검토 + 만들기
    [5] 입력
### 1.2. Docker 설치 & 기본 setting
    [1] 가상환경 연결하기 
        > cmd >> ssh 이름@주소 >> 비밀번호  
    [2] 리눅스 업데이트 (한줄씩 입력할 것) 
        sudo apt-get update          
        sudo apt-get upgrade
    [3] sudo apt-get install \>
        > apt-transport-https \
        > ca-certificates \
        > curl \
        > gnupg \
        > lsb-release
    [4] Docker 가져오고 Key 값 설치
        > curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg    
    [5] Docker 기본 설치
        > echo \
        "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    [6] 업데이트
        > sudo apt-get update
        sudo apt-get install docker-ce docker-ce-cli containerd.io
    [7] 아래 명렁어 사용 시  "Hello from Docker!" 나오면 설치 완료
        > sudo docker run hello-world
    [8] 연결된 docker list
        > sudo docker ps
    [9] 관리자 권환 바꾸기
        > sudo usermod -a -G docker $USER
    [10] 권환 바꾼 이후 docker restart 필요
        > sudo service docker restart
        > exit
    [11] 다시 VM 재연결
        > ssh 이름@주소 >> 비밀번호  
    [12] Docker 확인 (아래 명령어 작성 시 list뜨면 성공!!)
        > docker ps
### 1.3. Docker 기본 명령어
    [1] Ubuntu help
        > docker pull --help
    [2] Ubuntu 18.XX version의 image 가져오기
        > docker pull ubuntu:18.04
    [3] 실행되고있는 docker container 확인
        > docker ps
    [4] Docker 실행시키기 (18.04버전의 'demo1' docker를 /bin/bash 파일에서 실행)
        > docker run -it --name demo1 ubuntu:18.04 /bin/bash 
        > docker run -it --name demo2 ubuntu:18.04 /bin/bash 
        BUT!! 실행은 되지면 exit하면 나와버림 !! 
    [5] Service 형태로 계속 띄어진 프로그램(데몬)을 위해서는 '-d' 명령어 추가
        > docker run -it -d --name demo3 ubuntu:18.04 /bin/bash 
    [6] Docker 실행시키기 (exc)
        > docker exec -it demo3 /bin/bash
        > docker run --name demo4 -d busybox sh -c "while true;do $(echo date);sleep 1;done"
    [7] Docker의 log 확인 (stop)
        > docker logs demo4 -f
    [8] 실행 중단 (stop)
        > docker stop demo4
        BUT!! 실행만 중단한 것 일뿐 Container는 살아있음
    [10] Container까지 삭제 (rm)
        > docker rm demo4
        BUT!! local에 image는 계속 남아있음
    [11] local에서 images 삭제
        1) docker image 리스트 확인
            > docker images 
        2) image 삭제
            > docker rmi ubuntu:18.04
        3) 삭제된 docker image 확인
            > docker iamges 
            ('ubuntu:18.04' 리스트에서 사라졌나 확인)
### 1.4 Docker에 push 하기 
- 깃허브와 원리 비슷
#### 1) 텍스트 파일 생성 & 편집
    [1] 텍스트 파일 생성 (vi) : vi hello.txt
    [2] 편집 (i)             : i >> 편집할 내용 작성
    [3] 저장 (:w)            : esc >> :w
    [4] 파일 Exit (:q        : :q (강제로 나가고 싶을 때 '!' 추가 ":q!")
    [5] 파일 확인 (cat)      : cat hello.txt
    [6] 빈 파일 생성 (touch) : touch world.txt
    [7] 파일 삭제 (rm)       : rm hello.txt 
#### 2) Docker 폴더 생성
    [1] Home으로 이동
        > cd $HOME
    [2] 폴더 생성
        > mkdir docker-practice
    [3] 폴더 이동
        > cd docker-practice/
    [4] 빈 Dockerfile 생성
        > touch Dockerfile
    [5] 폴더 리스트 확인
        > ls
    [6] Dockerfile파일 수정
        > vi Dockerfile >> i
            FROM ubuntu:18.04
            RUN apt-get update
            CMD ["echo", "Welcome to Microsoft AI School"]
    [7] 파일 확인
        > cat Dockerfile
    [8] Docker image 생성
        > docker build -t my-image:v1.0.0 .
    [9] 필요한 파일만 학인 
        > docker images | grep my-image
#### 3) local에 docker registry 생성 & 푸시
    [1] Registry 생성 (-p: 허가할 Port, --name: 이름 ) 
        > docker run -d -p 5000:5000 --name registry registry
    [2] Registry 확인
        > docker ps 
    [3] 태그 변경
        > docker tag my-image:v1.0.0 localhost:5000/my-image:v1.0.0
    [4] Local Registry에 push
        > docker push localhost:5000/my-image:v1.0.0 
    [5] Web통신 요청
        > curl -X GET http://localhost:5000/v2/_catalog
        > curl -X GET http://localhost:5000/v2/my-image/tags/list
    [6] Docker에 로그인
        > docker login
        >> 아이디, 비밀번호 입력 ('Login Succeeded' 뜨면 성공!! )
    [7] 태그 변경
        > docker tag my-image:v1.0.0 아이디/my-image:v1.0.0
    [8] docker의 내 계정에 push
        > docker push 아이디/my-image:v1.0.0
    [9] docker의 내 계정에서 pull
        > docker pull 아이디/my-image:v1.0.0
    [10] docker에서 바로 실행
        > docker run -d 아이디/my-image:v1.0.0

<hr>

## 2. Kubernetes 사용하기
- 컨테이너화된 workload와 service를 관리하기 위한 이식성이 있고, 확장가능한 오픈소스 플랫폼이다. 
- 수많은 workload와 효율적으로 관리
- 쿠버네티스는 컴퓨터들을 연결하여 단일 형상으로 동작하도록 컴퓨팅 클러스터를 구성하고 높은 가용성을 제공하도록 조율

<center><img src="https://losskatsu.github.io/assets/images/infra/kubernetes/kubernetes01.jpg" style='width: 70%'><br>
(출처: https://losskatsu.github.io/it-infra/kubernetes01/#)</center>

### 2.1. Minikube 다운받고 웹 통신하기 
#### 1) Minikube 다운로드
    [1] Minikube 다운로드
        > curl -LO http://storage.googleapis.com/minikube/releases/v1.22.0/minikube-linux-amd64
    [2] Minikube를 뒤에 파일 location에 설치
        > sudo install minikube-linux-amd64 /usr/local/bin/minikube
    [3] 설치 확인
        > minikube --help
    [4] 버전 확인
        > minikube version
#### 2) 큐브CTL 다운로드
    [1] 큐브CTL 다운르도
        > curl -LO https://dl.k8s.io/release/v1.22.1/bin/linux/amd64/kubectl
    [2] 설치
        > sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    [3] 설치 확인
        > kubectl --help
    [4] 버전 확인
        > kubectl version
 #### 3) Minikube 실행
    [1] Minikube 실행
        > minikube start --driver=docker
    [2] 상태 확인
        > minikube status
    [3] 시스탬용 pod 확인하기
        > kubectl get pod -n kube-system
    [4] Minikube 삭제하기
        > minikube delete
### 2.2. yaml 파일 생성 (pod, deployment, service, pvc)
#### 1) Pod 생성
    [1] Minikube 다시 생성
        > minikube start --driver=docker
    [2]  yaml 파일 생성 (Pod)
        > vi pod.yaml        
        > 파일 내용
            apiVersion: v1
            kind: Pod           ## type 설정 Pod !!
            metadata:
                name: 이름(counter)
            spec:
                containers: 
                - name: count
                  image: busybox
                  args: [/bin/sh, -c, 'i= 0;while true;do echo "$i: $(date)"; sleep 1;done']
    [2] yaml 파일 실행
        > kubectl apply -f pod.yaml
    [3] pod를 가져오기
        > kubect1 get pod 
        (아래 결과 뜨면 성공!!!) 
            NAME      READY   STATUS    RESTARTS   AGE
            이름(counter)   1/1     Running   0          4m58s
    [4] pod 정보 가져오기
        > kubectl get pod -A
        > kubectl get pod -o wide
    [5] pod 정보를 계속 monitor할 경우 (명령어가 끝나질 않음)
        > kubectl get pod -w
    [6] pod의 log 확인
        > kubectl logs 이름(counter)
        > kubectl logs 이름(counter) -f (게속 보고 싶을 때)
    [7] 돌고 있는 pod에 접속하기
        > kubectl exec -it 이름(counter) sh >> ps >> 내용확인 >> exit
    [8] i) pod 삭제하기 
        > kubectl delete pod 이름(counter)
         ii) yaml 삭제하기
        > kubectl pod -f pod.yaml
#### 2) Deployment 생성
    - pod의 상위 개념
    - replicas를 통해 pod의 개수 control 가능

    [1] yaml 파일 생성 (Deployment)
        > vi Deployment.yaml
        > 파일 내용
            apiVersion: apps/v1
            kind: Deployment        ## type 설정 Deployment !!
            metadata:
            name: nginx-deployment
            labels:
                app: nginx
            spec:
            replicas: 3
            selector:
                matchLabels:
                app: nginx
            template:
                metadata:
                labels:
                    app: nginx
                spec:
                containers:
                - name: nginx
                    image: nginx:1.14.2
                    ports:
                    - containerPort: 80
    [2] yaml 파일 실행
        > kubectl apply -f Deployment.yaml
    [3] Deployment 가져오기
        > kubectl get Deployment 
        (성공 시 3개가 통합적으로 나옴)
    [4] pod를 가져오기
        > kubectl get pod
        (성공 시 3개의 pod가 개별적으로 나옴)
    [5] 만약 pod 하나가 죽었을 시 (실험을 위해 강제로 하나 죽임)
        > kubectl delete pod nginx-deployment-66b6c48dd5-46xwd
        > kubectl get pod
        (다시 새로운 Pod 1개가 생긴 것을 확인할 수 있음 : Auto-healing)
    [6] pod의 개수를 조절
        > kubectl scale deployment/nginx-deployment --replicas=5
    [7] pod 확인
        > kubectl get pod
        (성공 시 5개의 pod 확인)
    [8] deployment 삭제
        > kubectl delete deployment nginx-deployment
    [9] deployment 재생성
        > kubectl apply -f Deployment.yaml
    [10] 접속 시도 
        > curl -X GET 172.17.0.4 -vvv
#### 3) Service 생성
    - 내부에 있는 pod를 외부에 있는 pod로 뚫어줌
    - 내부 <-> 외부 pod들과 연결을 시켜줌

    [1] yaml 파일 생성 (Service)
        > vi Service.yaml
        > 파일 내용
            apiVersion: v1
            kind: Service       ## type 설정 Service !!
            metadata:
            name: my-nginx
            labels:
                run: my-nginx
            spec:
            type: NodePort
            ports:
            - port: 80
                protocol: TCP
            selector:
                app: nginx
    [2] yaml 파일 실행
        > kubectl apply -f Service.yaml
    [3] Service 가져오기
        > kubectl get service 
    [4] 외부 pod 연결하기
        > curl -X GET IP주소:80   # PORT 숫자: 80 

#### 4) PVC 생성




