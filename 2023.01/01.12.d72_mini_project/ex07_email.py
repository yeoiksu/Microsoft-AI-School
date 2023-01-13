#### 파일을 읽기 위한 Library
import csv # 파일 읽을때 사용
import os # 파일 읽을때 사용
# !pip install python_dotenv
from dotenv import load_dotenv # .env(비밀번호나 API_KEY처럼 sensitive한 정보를 숨겨줄때 사용함) 파일을 읽어줌

#### 주소를 얻고 지도를 그리기 위한 Library
# !pip install folium
import folium # 지도를 그릴 때 사용
# pip install pyppeteer  
from folium import utilities
from pyppeteer import launch # folium의 html을 png로 변환해줄 때 사용
# !pip install asyncio
import asyncio # CPU 작업과 I/O를 병렬로 처리하게 해줌 
# !pip install winsdk
import winsdk.windows.devices.geolocation as wdg # 원래는 C#용 코드 winrt Library에서 파생되어 나왔었지만, winrt가 사라지고 winsdk가 생김 
# !pip install geopy
from geopy.geocoders import Nominatim # 위도 적도값을 구해주고 그걸 한국 실제 주소로 바꿔줄때 사용

#### 이메일 사용을 위한 Library
import smtplib # 이메일 로그인할때 씀!
# !pip install email-to
from email.mime.text import MIMEText # 이메일 내용 보낼때 사용함 (제목, 내용을 나눠줌)
from email.mime.multipart import MIMEMultipart # 이메일에 문자열 외의 다양한 파일을 보낼 때 사용  

#01. 현재 GPS 통해 좌표값(위도 적도)을 얻기 위한 함수
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
def geocoding_reverse(lat_lng_str): # lat_lng_str 은 str을 인자로 받음 "abcdefg"
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    address = geolocoder.reverse(lat_lng_str) # geolocoder.reverse('위도, 적도') => 실제 주소 

    return address

#03. 위 두개의 함수를 실행시켜 실질적인 주소를 반환
def get_location():
    coordinate = getLoc()
    
    lat = str(coordinate[0])
    lng = str(coordinate[1])
    location = lat+', '+lng

    address = geocoding_reverse(location)
    return address
    
#04. csv파일을 읽어서 이용자의 이메일을 return하는 함수
def get_customer():
    data = []
    customer_data = './2023.01/01.12.d72_dl/customer_email.csv' # *** 파일 주소는 필요시 변경해주세요!! ***
    f = open(customer_data,'r',encoding='utf-8')
    rdr = csv.reader(f)
    
    for line in rdr:
        tmpstring = ''
        tmpstring = line[0]
        data.append(tmpstring)
    
    f.close()
    
    return data

#05. 현재 좌표와 경고 문구를 이메일로 보내주는 함수    
def send_alarm():
    
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
    address = get_location()
    customers = get_customer()
    
    # 보낼 메시지 설정
    msg = MIMEText(f"*** 경고 ***\n\n현재 아래 좌표에서 드론이 관측되었습니다.\n\n {address}")
    msg['Subject'] = '제목 : 드론 경고 알림입니다.'

    # 각각의 이용자에게 메일을 보냄
    for users in customers:
        # 메일 보내기
        s.sendmail(sender, users, msg.as_string())
    
    # 세션 종료
    s.quit()
    print("E-mail Sent to All Customer")

#06. html 형식의 지도를 png로 변환
async def map_to_png(target, m):
    html = m.get_root().render()
    browser = await launch(headless=True)

    page = await browser.newPage()
    with utilities.temp_html_filepath(html) as fname:
        await page.goto('file://{path}'.format(path=fname))

    img_data = await page.screenshot({'path': f'output/out_{target}.png', 'fullPage': 'true', })
    await browser.close()

# # Debugging Tool
if __name__ == '__main__':
    # send_alarm()
    address = getLoc()
    m = folium.Map(location=address, zoom_start=15, prefer_canvas=True, zoom_control=False,scrollWheelZoom=False, dragging=False)
    marker = folium.CircleMarker(address, radius=100, color='red', fill_color='red')
    marker.add_to(m)
    m.save('./2023.01/01.12.d72_dl/mymap.html')

    