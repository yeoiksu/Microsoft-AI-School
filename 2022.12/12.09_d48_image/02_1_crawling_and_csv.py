import PIL
import cv2
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import base64
from PIL import Image
from io import BytesIO
import os
import urllib.request
import pandas as pd 

def main():
    # crawling()
    saveCSV()

def selenium_scroll_option(driver):
    SCROLL_PAUSE_SEC = 3                                                         # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 끝까지 스크롤 다운
        time.sleep(SCROLL_PAUSE_SEC)                                             # 3초 대기
        new_height = driver.execute_script("return document.body.scrollHeight")  # 스크롤 다운 후 스크롤 높이 다시 가져옴
        if new_height == last_height:
            break
        last_height = new_height

### 1. Crawling
def crawling():
    file_path = './2022.12/12.09_d48_image/data/selenium'
    chromedriver_path = './2022.12/chromedriver.exe'
    os.makedirs(file_path, exist_ok=True)

    N = 200  # 데이터 수집 개수
    SEARCH_LIST = ['T-Shirt', "Trouser", "Dress", "Bag", "Sandal"]
    driver = webdriver.Chrome(chromedriver_path)
    driver.implicitly_wait(10)
     
    for search in SEARCH_LIST:
        img_dir = os.path.join(file_path, search)
        os.makedirs(img_dir, exist_ok=True)
        driver.get('https://www.google.com')
        elem = driver.find_element(By.NAME, 'q')
        elem.clear()
        elem.send_keys(search)          # 검색
        elem.send_keys(Keys.RETURN)     # 엔터
        assert "No results found." not in driver.page_source

        # 이미지 메뉴 누르기
        driver.find_element(By.XPATH, '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()
        selenium_scroll_option(driver)
        img_srcs = driver.find_elements(By.CLASS_NAME, 'rg_i')

        url_list = []
        last = 0
        for idx, img_src in enumerate(img_srcs):
            base64_image = img_src.get_attribute('src')
            try:
                if base64_image:  # 64일 때
                    if 'base64' in base64_image:
                        img = Image.open(BytesIO(base64.b64decode(base64_image.split(',')[-1])))  # decode 후 저장
                        img.save(os.path.join(img_dir, search+str(idx)+'.png'))
                        last = idx + 1
                    else:
                        url_list.append(base64_image)
            except PIL.UnidentifiedImageError:
                print(base64_image)
            except AttributeError:
                print(base64_image)
                continue
            if int(N) == idx:
                break
        [urllib.request.urlretrieve(url, os.path.join(img_dir, search+str(last+i)+'.png')) for i, url in enumerate(set(url_list))]
    driver.close()
    
#### 2. Image Reszie & Save CSV file
def saveCSV():
    SEARCH_LIST = ['T-Shirt', "Trouser", "Dress", "Bag", "Sandal"]
    TRAIN_PERCENTAGE = 0.8  # training 비율
    IMAGE_SIZE = 28         # 이미지 사이즈

    file_path = './2022.12/12.09_d48_image/data/selenium'
    df_dict_train= {
    'file_name':[],
    'label':[]
    }
    df_dict_test= {
    'file_name':[],
    'label':[]
    }

    os.makedirs(os.path.join(file_path, 'train'), exist_ok=True)
    os.makedirs(os.path.join(file_path, 'test') , exist_ok=True)

    for idx in range(len(SEARCH_LIST)):
        img_dir = os.path.join(file_path, SEARCH_LIST[idx])  # image file path
        for index, item in enumerate(os.listdir(img_dir)):
            image = cv2.imread(os.path.join(img_dir,item), cv2.IMREAD_GRAYSCALE)    # gray scale
            image = cv2.resize(image,(IMAGE_SIZE,IMAGE_SIZE))                       # resize
            if int(index) < len(os.listdir(img_dir)) * TRAIN_PERCENTAGE :   # train 비율 80%             
                cv2.imwrite( os.path.join(file_path, 'train', item), image)
                df_dict_train['file_name'].append(item)
                df_dict_train['label'].append(idx)
            else:                                                           # test  비율 20%
                cv2.imwrite( os.path.join(file_path, 'test', item), image)
                df_dict_test['file_name'].append(item)
                df_dict_test['label'].append(idx)
        df_train = pd.DataFrame(df_dict_train)
        df_test  = pd.DataFrame(df_dict_test)
        
    df_train.to_csv(os.path.join(file_path, 'annotation_train.csv'))
    df_test.to_csv (os.path.join(file_path, 'annotation_test.csv'))

    print(df_test['label'].value_counts())
    
if __name__ =='__main__':
    main()
