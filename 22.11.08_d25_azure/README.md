# Day25. Azure. Storage (Queue)
## Storage Account (스토리지 계정)
- 다음 4가지 서비스를 제공
    1) Blob (Object Storage)
    2) Files (File share)
    3) Table (Key-value store)
    4) Queue (Simple Queue)

### 1. Queue
- 메세지를 저장할 수 있는 Simple Queue
- FIFO 지원
- Base64 인코딩 지원
- 최대 64kb message 저장
- message를 주로 주고받는데 사용됨

### 2. Storage 탐색기 시작하기
    [1] windows 11 가상환경 만들기
    [2] 연결 후 Edge에서 'storage explorer download' 검색
    [3] Windows 버전으로 다운르도하고 파일 설치
    [4] 'Microsoft Azure Storage Explorer' 실행 >> 'Sign in with Azure' >> 기본 'Azure' >> 아이디, 비밀번호 입력
    [5] 왼쪽 tab의 연결된 것을 확인 가능 >> 'Open with Browser'