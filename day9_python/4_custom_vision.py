# Custom Vison 이해와 실습

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials

ENDPOINT = 'https://labuser37custom.cognitiveservices.azure.com/'

# key, resource id 입력
training_key   = '5b8c184773434e57bab7a63123ee6014'
prediction_key = '78b534d1a6a949d89993db5ebac2ebb8'
prediction_resource_id = '/subscriptions/7ae06d59-97e1-4a36-bbfe-efb081b9b03b/resourceGroups/RG37/providers/Microsoft.CognitiveServices/accounts/labuser37custom'

publish_iteration_name = "classifyModel"

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)

# project를 새로 만든다
print ("Creating project...")
project = trainer.create_project("Labuser37 Project")

# 태그를 만든다
Jajangmyeon_tag = trainer.create_tag(project.id, "Jajangmyeon")
Jjambong_tag    = trainer.create_tag(project.id, "Jjambong")
Tangsuyuk_tag   = trainer.create_tag(project.id, "Tangsuyuk")

# Training 시작
print('Training....')
iteration = trainer.train_project(project.id)

import time

# completed가 아니면 무한 loop
while (iteration.status != 'Completed'):
  iteration = trainer.get_iteration(project.id, iteration.id)
  print('Status: ' + iteration.status)
  time.sleep(0.5)

print('Done Training !!!')