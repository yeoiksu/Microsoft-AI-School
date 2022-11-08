# Day25. Azure. Storage (Queue) & Event Hubs & IoT Hub
## 1. Queue
- 메세지를 저장할 수 있는 Simple Queue
- FIFO 지원
- Base64 인코딩 지원
- 최대 64kb message 저장
- message를 주로 주고받는데 사용됨

<hr>

## 2. Storage 탐색기 시작하기
    [1] windows 11 가상환경 만들기
    [2] 연결 후 Edge에서 'storage explorer download' 검색
    [3] Windows 버전으로 다운르도하고 파일 설치
    [4] 'Microsoft Azure Storage Explorer' 실행 >> 'Sign in with Azure' >> 기본 'Azure' >> 아이디, 비밀번호 입력
    [5] 왼쪽 tab의 연결된 것을 확인 가능 >> 'Open with Browser'

<hr>

## 3. Event Hubs ([관련링크](https://learn.microsoft.com/ko-kr/azure/event-hubs/event-hubs-about)) 
<br>

![Event Hubs](https://learn.microsoft.com/ko-kr/azure/event-hubs/media/event-hubs-about/event_hubs_architecture.png)

1) HTTP / AMQP (MQTT/IBM)
2) Partition: 하나 하나의 저장공간
3) Azure Event Hubs:
    - 빅데이터 스트리밍 플랫폼, 이벤트 수집 서비스
    - Event Hubs아래 Event hub들을 다룰 수 있음 (scaleout 가능)
    
### 3.1 Event Hubs 만들기
    [1] 리소스 만들기 > 
    [2] 'Event Hubs' 검색 >> Create
    [3] <기본 설정> 이름, 위치 설정, Enable Auto-Inflate(auto scaleout할 건지 여부)
    [4] 기타 기본으로 설정하여 Create
    [5] 생성 후 리소스로 이동
    [6] '+ Event Hub'를 눌로 event hub 생성하기
    [7] <기본 사항> 이름, Partition Count(전체 개수), Message retention(기간) 설정 >> Create
    [8] overview 아래에 event가 생성된 것을 확인 가능

### 3.2. Event Hubs 사용하기
    [1] 왼쪽 tab의 Scale
        - Throughput Units: 기본 1 TU (traffic 사용량이 많아지면 TU를 늘려야한다)
        - Auto-Inflate: Auto scaleout 수치 설정 가능
    [2] overview 아래에서 생성된 event를 확인 가능

<hr>

## 4. IoT Device 
![IoT Hub 구조](https://docs.devicewise.com/Content/Resources/Images/deviceWISE_Azure.png)

### 기본 Setting    
    [1] Widwows 11 가상환경을 만들고 Edge에서 'Visual Studio 2022 Community Edition Download >> Download
    [2] New Project 생성 >> C##, Windows, Console >> Console App (.NET Framework) 생성

### 4.1. IoT Hub 생성
    [1] 리소스 만들기
    [2] 'IoT Hub' 선택 >> create
    [3] <기본 사항> 이름, 지역 설정
    [4] 다른 설정은 기본으로 >> create
    [5] 리소스로 이동 >> 왼쪽 tab의 'Device' >> '+ Add Device' >> 이름 설정 >> create

### 4.2. CS 파일로 IoT Hub 연결하기 ([관련링크](https://github.com/KoreaEva/IoT/blob/master/Labs/IoT_Hub/3.Device_Programming.md))
    [1] 오른쪽의 'Solution Explorer'의 프로젝트 이름 오른쪽 마우스 >> 'Manage Nuget Packages..' 
        >> Browse >> 'Microsoft Azure Device Client' 검색 >> Install
    [2] 오른쪽의 'Solution Explorer'의 프로젝트 이름 오른쪽 마우스 >> Add >> Class >> Weather data (Humidity, Temperature, Dust)를 불러오기 위한 class 작성 >> "WeatherModel.cs" 작성
    [3] random dummy값을 부여해줄 class "DummySensor.cs" 작성
    [4] main code >> "Program.cs" 작성 & 실행




