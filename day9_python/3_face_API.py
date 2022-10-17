import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

subscription_key = '0dc27627213048ee97ad2f75990b8c8e'
face_api_url = 'https://labuser37face.cognitiveservices.azure.com/face/v1.0/detect'
image_url = 'http://image.koreatimes.com/article/2021/05/10/20210510094734601.jpg'
image = Image.open(BytesIO(requests.get(image_url).content))

print(image)

headers = {'Ocp-Apim-Subscription-key': subscription_key}
params = {
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'Smile'
}
data = {'url': image_url}

response = requests.post(face_api_url, params=params, headers=headers,json=data)
faces = response.json()
print(faces)

draw = ImageDraw.Draw(image)
def DrawBox(faces):
   for face in faces:
     rect  = face['faceRectangle']
     left  = rect['left']
     top   = rect['top']
     width = rect['width']
     height= rect['height']

     draw.rectangle(((left,top),(left+width, top+height)), outline ='red')

     face_attributes = face['faceAttributes']
     smile = face_attributes['smile']

     draw.text((left,top), str(smile), fill='red')
     
DrawBox(faces)
image
