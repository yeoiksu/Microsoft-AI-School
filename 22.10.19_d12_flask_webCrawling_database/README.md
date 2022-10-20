# Day12. Flask & Web Crawling & Database

## 1. Flask
- 무료 Flask IDE : 구름 IDE
- Flask에 대해 더 알고 싶으면 구글에 "Jump to Flask" 검색

## 2. Web Crawling

### 2.1. requests.get()을 이용해 html5를 가져온다
```python
import requests

result = requests.get(URL).text
```
- URL을 읽어와서 TEXT 형태로 result에 저장한다

### 2.2.  BeautifulSoup(text, parser)을 이용해 원하는 정보를 가져온다
```python
import bs4

parser = 'html.parser'
bsObj = bs4.BeautifulSoup(result, parser)

# find : 첫번째 꺼를 찾음
# find('tag이름', {'class or key': 'class or key 이름'} )
bsObj.find('a', {'class': 'basicList_link__JLQJf'}).text

# find_all : 해당조건을 만족하는 모든 요소를 리스트로 반환
items = bsObj.find_all('a', {'class': 'basicList_link__JLQJf'})
```
- parser : 구조화 되있는 데이터를 이해하는 해석기
- find, find_all() 함수 사용


## 3. Azure Database
### Azure Data Services
    [1] MS SQL
    [2] MySQL
    [3] MariaDB
    [4] PostgreSQL
### 3.1. Azure와 Workbench 설정하기
#### 3.1.1. MS Azure SQL 만들기
    [1] MS Azure에서 로그인
    [2] 자신의 리소스그룹 선택
    [3] +만들기
    [4] 'Azure Databse for MySQL' 검색 후 만들기 
    [5] '유연한 서버' 선택 후 만들기
    [6] '서버 이름', '지역','MySQL버전' 설정
    [7] '워크로드 유형'에서 '개발 및 취미'으로 설정 
    [8] '서버 구성'을 클릭해서 디테일 설정
        - 기본: 기본으로 설정, "관리자 계정"에서 사용자 이름 암호 설정
        - 네트워크: "방화벽 규칙"
        - 보안 등등 skip하고 검토+만들기, 방화벽 없이 만들기   
#### 3.1.2 MySQL WorkBench 실행하여 Azure와 연결
    [1] "MySQL Workbench"에서 실행이후 Connection + 클릭하고 'Connection Name' 설정
    [2] 'Host Name'에서 Azure MySQL의 '서버 이름'을 복사해서 Workbench의 'Host Name'에 입력
    [3] 'Port'는 3306(기본), 'Username'은 Azure에서 설정한 '서버 이름'을 똑같이 입력 
    [4] Azure MySQL > '네트워크' 에서 자신의 ip 주소를 입력해야함. 아래의 '현재 클라이언트 IP 주소 추가(xxx.xxx.xxx.xxx)'클릭하고 설정 저장
    [5] Azure의 알림에 업데이트 완료가 됬다면 Workbench에서 'Test Connection'클릭 
    [6] Succesfully connected 메세지가 떴다면 OK를 누르면 기본 Setting은 끝 !!!
    [7] https://www.mysqltutorial.org/mysql-sample-database.aspx 에서 MySQL 샘플 데이터베이스 다운로드
    [8] Workbench에서 파일 마크를 클릭하여 다운로드 받은 database 파일을 열고 '번개' 마크를 클릭하여 실행
    [9] 왼쪽 'Schemas'에서 'refresh all'을 클릭하여 업데이트 된 databse를 볼 수 있다.

### 3.2. SQL 기본언어
#### 아래의 링크를 눌러 기본적인 SQL 강의 확인하기 [MySQL Tutorial Link](https://www.mysqltutorial.org/mysql-basics/) 

#### 1) ORDER BY :

```sql
SELECT 
    orderNumber,
    orderLineNumber,
    quantityOrdered * priceEach AS subtotal
FROM
    orderdetails
ORDER BY subtotal DESC
LIMIT 5;
```
- DECS: 내림차순, ASC: 오름차순
- AS: 별칭 설정 가능
- LIMIT: 출력 5개만

#### 2) WHERE :
- officeCode1 = '' AND officeCode2 = '' : AND는 둘다 만족
  officeCode1 = '' OR  officeCode2 = '' : OR은 하나만 만족
- officeCode BETWEEN 1 AND 3 : 1 ~ 3 사이
  officeCode BETWEEN 'a' AND 'z' : a ~ z 사이
- officeCode LIKE '%son' : 'son'으로 끝나는 모든 것(%) => 최대한 사용 안하는게 좋음 (데이터베이스에 많은 부화를 생성) 
- officeCode IN (1, 2, 3) : 1 2 3 중에 있으면
- officeCode IS NULL : NULL 값이면 (0이나 empty string은 아님)

#### 3) SELECT DISTINCT : 중복되는거 없이 한번만 SELECT 하고 싶을 때 

#### 4) JOIN : 중복되는거 없이 한번만 SELECT 하고 싶을 때