# 웹크롤링하여 실시간 환율 알아보기
import requests
from bs4 import BeautifulSoup

def get_exchange_rate(target1, target2):
    headers ={
        'User-Agent' : 'Mozilla/5.0',
        'Content-Type' : 'text/html; charset= utf-8'
    }

    response = requests.get('https://kr.investing.com/currencies/{}={}'.format(target1, target2), headers= headers)
  
    content = BeautifulSoup(response.content, 'html.parser')
    containers = content.find('span', {'data-test':'instrument-price-last'})

    print(containers.text)