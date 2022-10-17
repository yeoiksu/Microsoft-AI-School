# Computer Vision 
# Computer Vision API를 사용해서 이미지속에 있는 사물을 인식하는 데모 입니다.

# 네트워크 통신을 위해서 requests 패키지를 import 합니다.
import requests

# 이미지처리를 위해서 matplotlib.pyplot, Image, BytesIO 세 개의 패키지를 import 합니다.
# matplotlib.pyplot는 import 할 때 시간이 조금 걸릴 수 있습니다.
import matplotlib.pyplot as plt
from PIL import Image
from io import  BytesIO

# Subscription Key와 접속에 필요한 URL을 설정합니다.
subscription_key = '5f616e66019948d6907d562e1b401eb1'   # key1
vision_base_url = 'https://labuser37computervision.cognitiveservices.azure.com/vision/v2.0/' # endpoint + vision/v2.0

# 뒤에 뭐를 더붙이는냐에 따라서 기능 결정(ex. object detection 할껀지 content tag 할껀지 결정)
analyze_url = vision_base_url + 'analyze'  # 이미지 분석을 위한 주소

# 분석에 사용할 이미지 url
image_url = 'https://img0.yna.co.kr/etc/inner/KR/2016/10/29/AKR20161029046000004_01_i_P2.jpg'

con   = requests.get(image_url).content   # content 저장
byte  = BytesIO(con) # 이미지를 풀어줌 
image = Image.open(byte)    # 이미지를 가지고 와서 준비 
#. image = Image.open(BytesIO(requests.get(image_url).content))

# computer vision document url : https://learn.microsoft.com/ko-kr/azure/cognitive-services/computer-vision/
headers = {'Ocp-Apim-Subscription-key': subscription_key}
params  = {'visualFeatures': 'Categories,Description,Color'}
data = {'url': image_url}

# get or post
response = requests.post(analyze_url, headers = headers, params = params, json = data) #get or post
result = response.json()
print(result)

image_caption = result['description']['captions'][0]['text']
print(image_caption)







