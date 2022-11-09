# Day26. Azure. IoT Hub & Stream Analytics Job & MS SQL Database
## 1. IoT Hub
### 1.1 Azure IoT Explorer 사용하기 
    1) IoT Hub 연결 하기
        [1] https://github.com/Azure/azure-iot-explorer/releases 
        >> Version 0.15.1 >> Azure.IoT.Explorer.Preview.0.15.1.msi 설치
        [2] Azure Portal >> IoT Hub >> "공유 엑세스 정책" >> iothubowner >> "기본 연결 문자열" 복사
        [3] Azure IoT Explorer 실행 >> Connection String 선택 >> + Add Connection >> [2] 에서 복사한 "기본연결 문자열" 붙여넣기 >> 성공

    2) IoT Hub와 message send & receive 하기
        [1] Send message ( SendEvent() ) : 
        DeviceID 선택 >> Device에 대한 정보 확인 가능 >> 왼쪽 tab의 'Telemetry' >> 'Start' >> 들어오는 message 확인 !!
        [2] Receive message ( ReceiveCommands() ) : 
        IoT Explorer >> 왼쪽 tab의 'Cloud-to-device message' >> 보낼 Message body 작성 >> 'Send message to device' >> 실행된 CMD 에서 message 확인 가능

<hr>

## 2. Data Flow (Stream) 만들기 
- Stream Analytics Job >> Blob Storage >> Azure SQL Databse

### 2.1 Stream Analytics Job 만들기
    [1] 리소스 만들기
    [2] 'Stream Analytics Job' 검색 >> create
    [3] 기본 설정 >> create >> 리소스로 이동

### 2.2 Stream Analytics Job 연결하기
    [1] Input 만들기:
    왼쪽 tab의 Job topology(작업 토폴로지) >> input(입력) >> + Add stream input (스트림 입력 추가) >> "IoT hub" 선택 >> Alias(별칭), 해당 IoT Hub 설정 >> Save (저장) 
    [2] Output 만들기:
    왼쪽 tab의 Job topology >> output(출력) >> + 추가 >> "Blob Storage/ADLS Gen2" 선택 >> Alias(별칭), 해당 Storage Account, container, 인증 모드(Connection String) 설정
    [3] Input <-> Output 연결하기
    왼쪽 tab의 Job topology(작업 토폴로지) >> Query >> Input, Ouput 설정 >> Query 실행 >> Query 저장
    [4] Azure Portal >> Stream >> Overview(개요) >> Start(시작) >> 설정 >> Start
    [5] Flow 확인하기
    Azure Portal >> Storage >> Blob service >> weatherdata >> 일정시간 후 파일이 생성한 것을 확인 가능
    
 <hr>

## 3. Database
### 3.1. Data
- Data 종류:
1) 구조화: csv, yaml, 
2) 반구조화: 
3) 비구조화: 이미지 동영상
- Data 처리방법: 
1) OLTP (온라인 Transaction 거래 처리) : 데이터는 한번의 transaction으로 저장 (한번에 묶어서 처리함 -> Locking -> BUT "Dead Lock" 초래 가능 !!)
2) OLAP (온라인 Analytics 분석 처리)   : 데이터는 큐브에 주기적으로 로드, 집계, 저장 (필요한 datat를 뽑아 -> Data Cube)
