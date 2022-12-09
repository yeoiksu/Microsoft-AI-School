import PIL
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import base64
from PIL import Image
from io import BytesIO
import os
import urllib.request
import pandas as pd 
from collections import defaultdict
# from selenium.webdriver.chrome.o


def selenium_scroll_option(driver):
    SCROLL_PAUSE_SEC = 5
    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 3초 대기
        time.sleep(SCROLL_PAUSE_SEC)
        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def main():
    os.makedirs('./2022.12/22.12.09_d48_image/data/selenium', exist_ok=True)
    N = 120
    search_list = ['T-Shirt', "Trouser", "Dress", "Bag", "Sandal"]
    # 브라우저 로딩 시간 고려한 시간
    # time sleep과는 다르게 로딩 다되면 바로 실행
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    for search in search_list:

        ##### 1
        print("\n\n>>>>> ", search)

        img_dir = f'./2022.12/22.12.09_d48_image/data/selenium/{search}'
        os.makedirs(img_dir, exist_ok=True)
        driver.get('https://www.google.com')
        elem = driver.find_element(By.NAME, 'q')
        elem.clear()
        elem.send_keys(search)  # 검색
        elem.send_keys(Keys.RETURN)  # 엔터
        assert "No results found." not in driver.page_source

        # 이미지 메뉴 누르기
        # driver.find_element(By.XPATH, '/html/body/div[7]/div/div[4]/div/div[1]/div/div[1]/div/div[2]/a').click()
        driver.find_element(By.XPATH, '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()  # 이미지
        selenium_scroll_option(driver)

        # driver.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input').click()
        # selenium_scroll_option(driver)
        img_srcs = driver.find_elements(By.CLASS_NAME, 'rg_i')

        url_list = []
        last = 0

        ##### 2 이미지 저장
        print(search, " image start")

        for idx, img_src in enumerate(img_srcs):
            base64_image = img_src.get_attribute('src')
            try:
                if base64_image:  # 64일 때
                    if 'base64' in base64_image:
                        img = Image.open(BytesIO(base64.b64decode(base64_image.split(',')[-1])))  # decode 후 저장
                        img.save(os.path.join(img_dir, str(idx)+'.png'))
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
        [urllib.request.urlretrieve(url, os.path.join(img_dir, str(last+i)+'.png')) for i, url in enumerate(set(url_list))]
        print(len(set(url_list)))

        # csv 파일 생성
        ##### 3
        label_list = []
        data_dir = './2022.12/22.12.09_d48_image/data/selenium/' + search
        print(data_dir)

        for label in os.listdir(data_dir):
            label_list.append(label)

        df_dict = {
            'file_name' : [],
            'label' : []
        }

        for idx, label in enumerate(label_list):
            df_dict['file_name'].append(label)
            df_dict['label'] = search

        df = pd.DataFrame(df_dict)
        df.to_csv(data_dir + '.csv')

    driver.close()


if __name__ =='__main__':
    main()
