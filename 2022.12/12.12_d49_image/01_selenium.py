from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib.request

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("error : Creating directory... " + directory)

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

keywords = "사과"  # 키워드 입력
folder_path = './2022.12/12.12_d49_image/data'
create_folder(os.path.join(folder_path, keywords))

chromedriver_path = './2022.12/chromedriver.exe'
driver = webdriver.Chrome(chromedriver_path, options= options)
driver.implicitly_wait(3)

driver.get("https://www.google.co.kr/imghp?h1=ko")

# input  -> /html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input
# button -> /html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/button

## 위 아래 같은 코드
# keyword = driver.find_element_by_xpath(
#     '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
# keyword.send_keys(keywords)
# driver.find_element_by_xpath(
#     '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/button').click()

### 1. 검색어 검색하기
elem = driver.find_element_by_name("q")
elem.send_keys(keywords)
elem.send_keys(Keys.RETURN)

### 2. 스크롤 자동 내리기
num = 60

print(keywords, " 스크롤 중 ......")
elem = driver.find_element_by_tag_name('body')
for i in range(num):
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
try:
    driver.find_element_by_xpath(
        '//*[@id="islmp"]/div/div/div/div[2]/div[1]/div[2]/div[2]/input').click()  # 결과
    for i in range(num):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
except:
    pass

### 3. 이미지 개수 파악
links = []
images = driver.find_elements_by_css_selector("img.rg_i.Q4LuWd")

for image in images:
    if image.get_attribute('src') != None:
        links.append(image.get_attribute('src'))

print(keywords + " 찾은 이미지 개수 : ", len(links))
time.sleep(2)

### 4. 이미지 다운로드
for index, i in enumerate(links):
    url = i 
    start = time.time()
    # urllib.request.urlretrieve(url, folder_path + '/' + keywords + "_img_download/" + keywords + "_" + str(index) +".jpg" )
    urllib.request.urlretrieve(url, folder_path + '/'+ keywords +'/' + keywords + "_" + str(index) +".jpg" )
    print(str(index+1) + '/'+str(len(links)) + " " + keywords+ ' 다운로드 중...... Download time : ' + str(time.time() - start)[:5]+ ' 초' )
print(keywords + ' ---다운로드 완료---')

driver.close()