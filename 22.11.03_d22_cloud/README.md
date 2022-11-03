# Day22. DL. Cloud & Security 

## 1. VM에서 Linux (Ubuntu) 구현하기
### 1.1. "Azure Machine Learning" 만들기
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