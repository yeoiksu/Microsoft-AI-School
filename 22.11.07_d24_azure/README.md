# Day24. Azure. Storage (Blob & File)
## Storage Account (스토리지 계정)
- 비정형 및 반정형 데이터를 저장하는 저장소
- 뛰어난 내구성과 가용성을 제공
- 제한 없는 저장소 용량
- 다음 4가지 서비스를 제공
    1) Blob (Object Storage)
        - 브라우저에 이미지나 문서 직접 제공
        - 분산 액세스용으로 파일 저장
        - 비디오 및 오디오 스트리밍
        - 3가지 유형: 스토리지 계정, 스토리지 계정의 컨테이너, 컨테이너 Blob
    2) Files (File share)
    3) Table (Key-value store)
    4) Queue (Simple Queue)

### Storage Account 리소스 만들기
    [1]  + 리소스 만들기
    [2] 'Storage Account' 만들기 선택
    [3] <기본> 
        - 이름, 지역 설정
        - 중복 : LRS
        <보안>
        - 'Blob 퍼블릭 액세스 사용', '스토리지 계정 키 액세스 사용' 체크를 빼는 것이 보안에 더 좋음
    [4] 검토 + 만들기
    [5] 왼쪽 tab의 엑세스 제어(IAM)에서 제어 가능
    [6] 왼쪽 tab > 설정 > 잠금
        - 권한이 있으면 추가가 가능함
### 1. Blob Container (컨테이너) 만들기
    1) 직접 Blob storage 만들기
        [1] 생성한 Storage Account로 이동 
        [2] 컨테이너 생성: 'Blob serivce' >> '+컨테이너' >> 이름(data), blob 설정 >> 컨테이너 만들기
        [3] 생성한 컨테이너 클릭 >> '업로드' >> 파일(임의의 이미지) 선택 >> 업로드 

    2) Python를 활용하여 Blob storage 만들기
        [1] 왼쪽 tab의 '엑세스키'를 python에 넘겨줘야함.
        [2] 액세스키 >> key1 >> 연결 문자열
            BlobServiceClient.from_connection_string(연결문자열)
        [3] 폴더 안에있는 1_storage_blob.ipynb을 실행
        [4] '액세스 수준 변경' >> Blob으로 바꿈
        [5] URL을 입력하면 text파일을 다운로드 할 수 있음

### 2. File 공유 관리
    1) 직접 파일 공유하기
        [1] 생성한 Storage Account로 이동 
        [2] 왼쪽 tab의 '파일 공유' 선택 >> ' + 만들기' >> 이름 설정
        [3] '업로드' >> 파일(임의의 이미지) 선택 >> 업로드 
    
    2) 가상환경에서 파일 공유하기
        [1] 왼쪽 tab의 '파일 공유' >> 연결 >> Windows >> Show script >> 스크립트 복사
        [2] Windwos 11 VM 생성 후 가상머신에 접속
        [3] Powershell 실행 후 복사한 스크립트를 붙여넣기
        [4] 파일에서 새로운 bird 드라이브가 생성되고 사진이 업로드 된 것을 확인할 수 있다. 
        
    3) script를 직접 줘서 파일 공유하기
        [1] 공유받은 스크립트를 powershell에 직접 입력
        (기존의 연결을 끊은 후 시도해야함!!! )

    4) Snapshot 생성하기
        - 스냅샷 : 파일이 변경되어도 이전 파일의 형태를 저장함. File의 crash 됬을 때 유용함
        - 백업이라고 생각하면 편함
        [1] 왼쪽 tab의 '스냅샷' >> '스냅샷 추가'
