from datetime import datetime 
from collections import deque 
import pandas as pd
import pymysql
import keyboard

import requests, json # 이메일 및 ip정보 다룰떄 씀
import smtplib # 이메일 로그인할때 씀!
import csv # 파일 읽을때 사용
import os # 파일 읽을때 사용
# !pip install folium
import folium # 지도를 그릴 때 사용
# !pip install asyncio
import asyncio 
# !pip install winsdk
import winsdk.windows.devices.geolocation as wdg
import pandas as pd
import pymysql


# !pip install email-to
from email.mime.text import MIMEText # 이메일 내용 보낼때 사용함 (제목, 내용을 나눠줌)

from email.mime.multipart import MIMEMultipart # 이메일에 HTML 주소를 보냄 

# !pip install geopy
from geopy.geocoders import Nominatim # 위도 적도값을 구해주고 그걸 한국 실제 주소로 바꿔줄때 사용

# !pip install python_dotenv
from dotenv import load_dotenv # .env(비밀번호나 API_KEY처럼 sensitive한 정보를 숨겨줄때 사용함) 파일을 읽어줌
     
     



def get_customer():
    # 기본 DB setting
    conn = pymysql.connect(
    user='bbongs',
    passwd='Qweasd123$',
    host='219.251.99.114',
    db='drone_project',
    charset='utf8'
)
    cursor = conn.cursor()  
    
     # 서비스 이용자 이메일 정보와 드론 발견 주소를 가져옴 
    # (1, 'yu', 'yuyeon', 'yuyeon_msai2022@nextcity.kr')
    address = []
    customers = []
    sql_update = "DELETE FROM `drone_project`.`customer` WHERE email not regexp('.com' or '.co.kr' OR '.net'); " # 이메일이 잘못 입력됬을 경우 삭제 
    cursor.execute(sql_update)
    sql = "SELECT * from customer" 
    cursor.execute(sql)

    # query 결과를 list 형으로 가져옴.
    for row in cursor:
        customers.append(row[2])
        address.append(row[3])
        
    conn.close()
    return address 



# *** 드론 관측 시 이 함수(send_alarm)만 가져와서(from func import send_alarm) 실행시켜 주시면 되요!!! *** 
#00. 현재 좌표와 경고 문구를 이메일로 보내주는 함수    
def send_alarm(target_object,is_first, numb_object, time_before, time_now, address):
    
    # G-MAIL 접속 
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    
    # .env파일에서 G-MAIL 로그인 아이디와 비밀번호를 가져옴
    load_dotenv()
    sender = os.getenv('USER_NAME')
    pw = os.getenv('PASSWORD')

    # 가져온 ID, PASSWORD로 로그인
    s.login(sender , pw)
    
    if is_first == True:
        # 보낼 메시지 설정
        msg = MIMEText(f"*** 경고 ***\n\n 현재시각: {time_before} \n\n 현재 아래 좌표에서 {target_object}이(가) {numb_object}개 관측되었습니다.\n\n {address}")
        msg['Subject'] = f'제목 : {target_object} 관측되었습니다.'
        
    else:     
        # 보낼 메시지 설정
        msg = MIMEText(f"*** 경고 ***\n\n {time_before} ~ {time_now} 동안\n\n 현재 아래 좌표에서 {target_object}이(가) {numb_object}개 관측되었습니다.\n\n {address}")
        msg['Subject'] = f'제목 : {target_object} 관측되었습니다.'
        

    # 각각의 이용자에게 메일을 보냄
    for users in address:
        # 메일 보내기
        s.sendmail(sender, users, msg.as_string())
    
    # 세션 종료
    s.quit()
    print("\n--------------------------------------------------\n")
    print("이메일이 전송되었습니다")
    print("\n--------------------------------------------------\n")

     
# 현재 시간을 리턴해주는 코드!  
def get_current_time():
    now = datetime.now()
    
    mlsec = now.microsecond/10000
    mlsec = round(mlsec)
    
    now_format = now.strftime('%Y-%m-%d %H:%M:%S.')
    now_format += str(mlsec)
    
    return now_format 

def calculate_time_min(t_before, t_after):
    t_prev = update_time_string(t_before)
    t_now = update_time_string(t_after)
    
    
    format_date = '%Y-%m-%d %H:%M:%S'
    t_prev = datetime.strptime(t_prev, format_date)
    t_now = datetime.strptime(t_now, format_date)
    date_calculated = t_now-t_prev

    date_calculated = int(date_calculated.seconds/60)
    return date_calculated


def update_time_string(time_data):
    tmp_time = time_data
    tmp_lenght = len(tmp_time)
    max_lenght = 19 
    
    
    if tmp_lenght > max_lenght:
        tmp_time = tmp_time[0:len(tmp_time)-(tmp_lenght-max_lenght)]
    else:
        pass

    return tmp_time

    

# DB에 업로드하는 코드!
def DB_process(label_saved):

    detect ='''
    CREATE TABLE detect (
    id int NOT NULL AUTO_INCREMENT,
    cctv VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
    Latitude DECIMAL(20,5) NULL DEFAULT NULL,
    Longitude DECIMAL(20,5) NULL DEFAULT NULL,
    StartTime DATETIME NULL DEFAULT NULL,
    EndTime DATETIME NULL DEFAULT NULL,
    detection VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8_general_ci',

    PRIMARY KEY (id)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;
'''
    # from mysql.connector import (connection)
    # 기본 DB setting
    conn = pymysql.connect(
    user='bbongs',
    passwd='Qweasd123$',
    host='219.251.99.114',
    db='drone_project',
    charset='utf8'
)
    cursor = conn.cursor()    
    # label_saved  = {1: ['helicopter', '2023-03-09 22:44:42.52', '2023-03-09 22:44:43.84']}
    tmp_dict = label_saved  
    detect_info = []
               
    tmp_key = list(tmp_dict.keys())
    tmp_values = list(tmp_dict.values())
   
    
    for i in range(len(tmp_values)):
        data_keys = tmp_key[i]
        
        data_values = tmp_values[i]
        data_values.insert(0,data_keys)
        detect_info.append(data_values)
  
    # [1, cctv1, 38.38274, 128.33009, 2023-01-03 01:40:00, 2023-01-03 01:43:00, drone]
    # [2023-01-03 01:40:00, 2023-01-03 01:43:00, drone] list 형 데이터로 부탁드립니당
    cursor = conn.cursor()
    cctv, Latitude, Longitude = 'cctv1', 38.38274, 128.33009    # 고정값 설정
    for i in range(len(detect_info)):
        index = (detect_info[i][0])
        detection = (detect_info[i][1])
        StartTime = (detect_info[i][2])
        EndTime = (detect_info[i][3])
        
        sql="""
    INSERT INTO detect (cctv, Latitude, Longitude, StartTime, EndTime, detection, num  ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
        cursor.execute(sql, (cctv, Latitude, Longitude, StartTime, EndTime, detection, index))

        conn.commit()
        
    conn.close()
    
    print("\n--------------------------------------------------\n")
    print("데이터가 전송되었습니다")
    print("\n--------------------------------------------------\n")

# DB에 데이터를 보낸 뒤 현재 리스트를 업데이트 
'''
데이터는 아래처럼 들어옴, key가 1일때, value가 ['helicopter', '2023-03-09 22:44:44.52', '2023-03-09 22:44:43.84']
    1: ['helicopter', '2023-03-09 22:44:36.52', '2023-03-09 22:44:45.84'], 
    2: ['drone', '2023-03-09 22:44:36.52', '2023-03-09 22:44:45.84'],
    3: ['bird', '2023-03-09 22:44:36.52', '2023-03-09 22:44:40.84']
    
만약 마지막 프레임 시점이 time = '2023-03-09 22:44:45.84' 라면 
1,2값은 업데이트(시작시간이 끝난시간 값으로) 되고, 3번 같은 경우 끝난 시간보다 먼저 종료 되었기에 리스트에서 삭제
'''
def remove_error(list, time):
    list_copy = list 
    remove_list = []
    
    for key, value in list_copy.items():
        tmpList = value 
        if tmpList[2] == tmpList[1] and tmpList[2] != time:
            remove_list.append(key)
    
    for r_key in remove_list:
        del list_copy[r_key]
            
    return list_copy


def update_List(list, time):
    list_copy = list
    
    remove_list = []
    
    for key, value in list_copy.items():
        tmpList = value
        if tmpList[2] == time: 
            tmpList[1] = tmpList[2]
            list_copy[key]=tmpList 
        else:
            remove_list.append(key)
            
    for r_key in remove_list:
        list_copy.pop(r_key,None)
        
    return list_copy
    
def update_Format(list):
    list_copy = list
    
    for key, value in list_copy.items():
        if len(value) == 4:
            list_copy[key] = [value[1],value[2],value[3]]
    
    
    
    
    for key, value in list_copy.items():
        tmpList = value
        
        if len(tmpList[1]) > 22:
            tmp = 22 - len(tmpList[1])
            tmpList[1] = tmpList[1][0:22]
        elif len(tmpList[1]) < 22:
            tmp = 22 - len(tmpList[1])
            tmpStr = '0'*tmp
            tmpList[1] = tmpList[1]+tmpStr
        else:
            pass
            
        if len(tmpList[2]) > 22:
            tmp = 22 - len(tmpList[1])
            tmpList[2] = tmpList[2][0:22]
        elif len(tmpList[2]) < 22:
            tmp = 22 - len(tmpList[2])
            tmpStr = '0'*tmp
            tmpList[2] = tmpList[2]+tmpStr
        else:
            pass
        
        list_copy[key] = tmpList

        
    return list_copy


#01. 현재 IP주소를 통해 좌표값(위도 적도)을 얻기 위한 함수
async def getCoords():
    locator = wdg.Geolocator()
    pos = await locator.get_geoposition_async()
    return [pos.coordinate.latitude, pos.coordinate.longitude]

def getLoc():
    try:
        return asyncio.run(getCoords())
    except PermissionError:
        print("ERROR: You need to allow applications to access you location in Windows settings")

#02. 얻은 좌표값을 실질적은 주소로 바꿔주는 함수
def geocoding_reverse(lat_lng_str): 
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    address = geolocoder.reverse(lat_lng_str)

    return address


#03. 위 두개의 함수를 실행시켜 실질적인 주소를 반환
def get_location():
    coordinate = getLoc()
    
    lat = str(coordinate[0])
    lng = str(coordinate[1])
    location = lat+', '+lng

    address = geocoding_reverse(location)
    return address
    
    
def cal_abs(val):
    if val>=0:
        pass 
    else:
        val*= -1 
        
    return val 
# Debugging Tool
# tmp = {1: ['helicopter', '2023-03-09 22:44:36.52', '2023-03-09 22:44:43.84'], 
# 2: ['drone', '2023-03-09 22:44:36.52', '2023-03-09 22:44:46.84'],
# 3: ['bird', '2023-03-09 22:44:40.84', '2023-03-09 22:44:40.84']}

# current = '2023-03-09 22:44:45.84'
# result = remove_error(tmp, current)
# print(result)
# s1,s2 = '2023-03-09 22:44:36.52', '2023-03-09 22:44:46.84' 
# s1 = datetime.now()
# s2 = datetime.now()
# result = abs(s1.second - s2.second)
# print(result)

# tmp = {2: [ 'bird', '2023-03-21 11:37:26.100', '2023-03-21 11:37:22.25'], 1: [ 'balloon', '2023-03-21 11:37:22.25', '2023-03-21 11:37:22.25'], 4: ['bird', '2023-03-21 11:37:23.77', '2023-03-21 11:37:23.84']}
# current = '2023-03-09 22:44:45.84'
# result = remove_error(tmp, current)
# print(result)
# tmp = {1: [1, 'bird', '2023-03-21 17:57:48.68', '2023-03-21 17:57:48.68'], 2: ['drone', '2023-03-21 17:57:50.85', '2023-03-21 17:57:50.85']}

# for i in range(0,3):
#     if i in tmp.keys():
#         tmp_val = tmp[i]
        
#         if len(tmp_val) == 4:
         
#             tmp[i] = [tmp_val[1],tmp_val[2],tmp_val[3]]
        
# print(tmp)