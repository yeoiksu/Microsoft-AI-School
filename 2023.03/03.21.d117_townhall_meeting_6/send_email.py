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

# 기본 DB setting
conn = pymysql.connect(
    user='bbongs',
    passwd='Qweasd123$',
    host='219.251.99.114',
    db='drone_project',
    charset='utf8'
)

cursor = conn.cursor() 

# *** 드론 관측 시 이 함수(send_alarm)만 가져와서(from func import send_alarm) 실행시켜 주시면 되요!!! *** 
#00. 현재 좌표와 경고 문구를 이메일로 보내주는 함수    
def send_alarm(target_object,is_first, time_before, time_now):
    
    # G-MAIL 접속 
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    
    # .env파일에서 G-MAIL 로그인 아이디와 비밀번호를 가져옴
    load_dotenv()
    sender = os.getenv('USER_NAME')
    pw = os.getenv('PASSWORD')

    # 가져온 ID, PASSWORD로 로그인
    s.login(sender , pw)
    
    # 서비스 이용자 이메일 정보와 드론 발견 주소를 가져옴 
    # (1, 'yu', 'yuyeon', 'yuyeon_msai2022@nextcity.kr')
    address = []
    customers = []
    sql = "SELECT * from customer" 
    cursor.execute(sql)

    # query 결과를 list 형으로 가져옴.
    for row in cursor:
        customers.append(row[2])
        address.append(row[3])
    

    if is_first == 1:
        
        # 보낼 메시지 설정
        msg = MIMEText(f"*** 경고 ***\n\n 현재시각: {time_before} \n\n 현재 아래 좌표에서 {target_object}이(가) 관측되었습니다.\n\n {address}")
        
        msg['Subject'] = f'제목 : {target_object} 관측되었습니다.'

    # 각각의 이용자에게 메일을 보냄
    for users in address:
        # 메일 보내기
        s.sendmail(sender, users, msg.as_string())
    
    # 세션 종료
    s.quit()
    print("E-mail Sent to All Customer")


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
    

    
# # Debugging Tool
# send_alarm()

# import io 
# from PIL import Image

# address = getLoc()
# print(address)

# map_ = folium.Map(location=address, zoom_start=13, prefer_canvas=True, zoom_control=False,scrollWheelZoom=False, dragging=False)
# marker = folium.CircleMarker(address, radius=50, color='red', fill_color='red')
# marker.add_to(map_)
# map_.save('mymap.html')

# import multiprocessing


# def worker(procnum, return_dict):
#     """worker function"""
#     print(str(procnum) + " represent!")
#     return_dict[procnum] = procnum


# if __name__ == "__main__":
#     manager = multiprocessing.Manager()
#     return_dict = manager.dict()
#     jobs = []
#     for i in range(5):
#         p = multiprocessing.Process(target=worker, args=(i, return_dict))
#         jobs.append(p)
#         p.start()

#     for proc in jobs:
#         proc.join()
#     print(return_dict.values())