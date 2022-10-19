# Day11. Pandas & Matplotlib Pyplot

## 1. Pandas
- Series index와 value 추출:

        series_name.index  : index 추출
        series_name.values : values 추출

- Dataframe에 Series 객체 추가:
        
        dframe_name['key'] = Series([넣을 values])

- Series에서 삭제:
        
        series_name= series_name.drop('key이름')
        series_name.drop('key이름')

- Dataframe에서 삭제:

        dframe_name = dframe_name.drop(['key이름']) : key이름과 일치한 "행" 삭제
        dframe_name = dframe_name.drop(['key이름'], axis=0 ) : key이름과 일치한 "행" 삭제 (위와 같음)
        dframe_name = dframe_name.drop(['key이름'], axis=1 ) : key이름과 일치한 "열" 삭제
        




    
