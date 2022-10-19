# Day11. Pandas & Matplotlib Pyplot

## 1. Pandas
- Series에서 index와 value 추출:

        series_name.index  : index 추출
        series_name.values : values 추출

- Dataframe에 Series 객체 추가:
        
        dframe_name['key'] = Series([넣을 values])

- Series에서 삭제:
        
        series_name= series_name.drop('key이름')
        series_name.drop('key이름')

- Dataframe에서 삭제:

        dframe_name = dframe_name.drop(['key이름']) : key이름과 일치한 "행" 삭제 (아무것도 작성 안하면 axis=0)
        dframe_name = dframe_name.drop(['key이름'], axis=0 ) : key이름과 일치한 "행" 삭제 (위와 같음)
        dframe_name = dframe_name.drop(['key이름'], axis=1 ) : key이름과 일치한 "열" 삭제

- Series에서 Slicing:

        series_name['key1 이름': 'key2 이름']

- Series에서 정렬:

        series_name.sort_values(): 오름차순
        series_name.sort_values(ascending= False): 내림차순

- Dataframe에서 정렬:
        
        dframe_name.sort_index(): 오름차순 정렬 (기본으로 행을 
        기준으로 함)
        dframe_name.sort_index(axis=1): 오름차순, 열1을 기준으로 정렬
        dframe_name.sort_values( by = ['key1'] ): ke1이름을 가진 열을 기준으로 오름차순 정렬 

- Pandas를 이용한 기초 분석:

        dframe_sample = dframe_name[['key1', 'key2']]: key1과 key2의 열의 값을 출력함
        dframe_sample.min() : dframe_sample의 각 열의 최소값
        dframe_sample.max() : dframe_sample의 각 열의 최대값
        dframe_sample.mean(): dframe_sample의 각 열의 평균값
        dframe_sample.corr(): dframe_sample의 각 열의 상관 관계 출력

- Group화 하기

        for a, b in dataframe.groupby(['속성1']):
                1. a는 key
                2. b는 '속성1'로 그룹화된 데이터
        for (a1 a2), b in dataframe.groupby(['속성1', '속성2]):
                1. a1은 속성1의 key
                2. a2은 속성2의 key
                3. b는 '속성1', '속성2'로 그룹화된 데이터
                4. 그룹화 할 속성이 2개 이상일 때는 tuple로 묶어서 생성해야함

        dframe_group = dframe_name['key1'].groupby(dframe_name['key2']): 'key2'로 그룹화 되어있는 'key1'를 보기





    
