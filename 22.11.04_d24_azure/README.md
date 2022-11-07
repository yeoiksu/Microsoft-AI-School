# Day23. Azure. Storage
## 1. Storage Account (스토리지 계정)
- 비정형 및 반정형 데이터를 저장하는 저장소
- 뛰어난 내구성과 가용성을 제공
- 제한 없는 저장소 용량
- 다음 4가지 서비스를 제공
    1) Blob (Object Storage)
    2) Files (File share)
    3) Table (Key-value store)
    4) Queue (Simple Queue)

## 1.1. Storage Account 리소스 만들기
    [1]  + 리소스 만들기
    [2] 'Storage Account' 만들기 선택
    [3] <기본> 
        - 이름, 지역 설정
        - 중복 : LRS
    [4] 검토 + 만들기
## 1.2. Storage Account 설정
    [1] 왼쪽 tab의 엑세스 제어(IAM)에서 제어 가능
    [2] 왼쪽 tab > 설정 > 잠금
        - 권한이 있으면 추가가 가능함