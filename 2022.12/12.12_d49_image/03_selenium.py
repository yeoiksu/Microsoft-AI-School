from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from multiprocessing import Pool
import time
import os
import urllib.request
import pandas as pd
import shutil

folder_path = './2022.12/12.12_d49_image/data'
chromedriver_path = './2022.12/chromedriver.exe'

def create_folder(directory):
    # 폴더 생성
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("error : Creating directory ... " + directory)


# 검색 키워드 호출
key = pd.read_csv(folder_path+'/keyword.txt', encoding= 'utf-8', names =['keyword'])
keyword = []
[keyword.append(key['keyword'][x]) for x in range(len(key))]

def image_download(keywords):
    create_folder(folder_path + '/' + keywords + '_low_resolution' )

    # 크롬 드라이브 호출
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    
    driver = webdriver.Chrome(chromedriver_path, options= options)
    driver.implicitly_wait(3)

    # 검색
    print('검색 >> ', keywords)
    driver.get("https://www.google.co.kr/imghp?h1=ko")
    keyword = driver.find_element_by_xpath(
        '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    keyword.send_keys(keywords)
    keyword.send_keys(Keys.RETURN)

    # 스크롤 내리기 -> 결과 더보기 버튼 클릭
    print("스크롤 ..... ", keywords)
    elem = driver.find_element_by_tag_name('body')
    N = 50
    for i in range(N):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.4)
    try:
        driver.find_element_by_xpath(
            '//*[@id="islmp"]/div/div/div/div[2]/div[1]/div[2]/div[2]/input').click()
        for i in range(N):
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.4)
    except:
        pass

    images = driver.find_elements_by_css_selector("img.rg_i.Q4LuWd")
    print(keywords+' 찾은 이미지 개수:', len(images))

    links = []
    for i in range(1, len(images)):
        try:
            print('//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img')

            driver.find_element_by_xpath(
                '//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img').click()
            links.append(driver.find_element_by_xpath(
                '//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a/img').get_attribute('src'))
            # driver.find_element_by_xpath('//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a').click()
            print(keywords+' 링크 수집 중..... number :'+str(i)+'/'+str(len(images)))
        except:
            continue

    forbidden = 0
    for index, i in enumerate(links):
        try:
            url = i 
            start = time.time()  
            urllib.request.urlretrieve(url, folder_path + '/'+ keywords +'_high_resolution/' + keywords + "_" + str(index) +".jpg" )
            print(str(index+1) + '/'+str(len(links)) + " " + keywords+ ' 다운로드 중...... Download time : ' + str(time.time() - start)[:5]+ ' 초' )
        except:
            forbidden += 1
            continue
    print(keywords + ' ---다운로드 완료---')

def reDefine():
    folder_path = './2022.12/12.12_d49_image/data'
    apple_path  = './2022.12/12.12_d49_image/data/사과_high_resolution/'
    banana_path = './2022.12/12.12_d49_image/data/바나나_high_resolution/'
    kiwi_path   = './2022.12/12.12_d49_image/data/키위_high_resolution/'

    for name in os.listdir(folder_path):
        os.makedirs(os.path.join(folder_path, 'apple') , exist_ok=True)
        os.makedirs(os.path.join(folder_path, 'banana'), exist_ok=True)  
        os.makedirs(os.path.join(folder_path, 'kiwi')  , exist_ok=True) 

        if '사과' in name:
            for index, item in enumerate(os.listdir(apple_path)):
                shutil.copyfile(apple_path + item, folder_path + '/apple/apple_' + str(index) + '.jpg')
        elif '바나나' in name:
            for index, item in enumerate(os.listdir(banana_path)):
                shutil.copyfile(banana_path + item, folder_path + '/banana/banana_' + str(index) + '.jpg') 
        elif '키위' in name:
            for index, item in enumerate(os.listdir(kiwi_path)):
                shutil.copyfile(kiwi_path + item, folder_path + '/kiwi/kiwi_' + str(index) + '.jpg')             

if __name__ == '__main__':
    pool = Pool(processes=3)
    pool.map(image_download, keyword)
    reDefine()
    
