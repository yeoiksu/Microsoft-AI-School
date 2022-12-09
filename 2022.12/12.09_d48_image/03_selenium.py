import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.implicitly_wait(10)  # 기다리는 최대시간

driver.get("https://www.google.com/")

elem = driver.find_element(By.NAME, 'q')
elem.clear()

## 검색어로 검색
search = 'banana'
elem.send_keys(search)
elem.send_keys(Keys.RETURN)

# 이미지 메뉴 누르기
driver.find_element(By.XPATH, '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()
# elem.send_keys(Keys.RETURN)
input()


