from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib.request
import pandas as pd
from multiprocessing import Pool

folder_path = './2022.12/12.12_d49_image/data'
chromedriver_path = './2022.12/chromedriver.exe'

key = pd.read_csv(folder_path+'/keyword.txt', encoding= 'utf-8', names =['keyword'])
keyword = []
[keyword.append(key['keyword'][x]) for x in range(len(key))]

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("error : Creating directory... " + directory)


def image_download(keywords):
    create_folder(folder_path + '/' + keywords + '_low_resolution' )

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(chromedriver_path, options= options)
    driver.implicitly_wait(3)

    # 검색 
    print("검색 >>> ", keywords)
    driver.get("https://www.google.co.kr/imghp?h1=ko")

    keyword = driver.find_element_by_xpath(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    keyword.send_keys(keywords)
    keyword.send_keys(Keys.RETURN)
    
    # 스크롤 내리기
    num = 60
    print("스크롤...... ", keywords )
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

    links = []
    images = driver.find_elements_by_css_selector("img.rg_i.Q4LuWd")

    # for image in images:
    #     if image.get_attribute('src') != None:
    #         links.append(image.get_attribute('src'))
    print(keywords + " 찾은 이미지 개수 : ", len(links))

    # for index, i in enumerate(links):
    #     url = i 
    #     start = time.time()  

    #     urllib.request.urlretrieve(url, folder_path + '/'+ keywords +'_low_resolution/' + keywords + "_" + str(index) +".jpg" )
    #     print(str(index+1) + '/'+str(len(links)) + " " + keywords+ ' 다운로드 중...... Download time : ' + str(time.time() - start)[:5]+ ' 초' )
    # print(keywords + ' ---다운로드 완료---')

    links = []
    for i in range(1, len(images)):
        try:
            # //*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img
            # //*[@id = "islrg"]/div[1]/div[40]/a[1]/div[1]/img
            driver.find_element_by_xpath(
                '//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img')
            links.append(driver.find_element_by_xpath(
                '//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a/img').get_attribute('src'))
            print(keywords + '링크 수집 중 ... number :  ' +
                  str(i) + '/' + str(len(images)))
        except:
            continue    


# 실행
if __name__ == '__main__':
    pool = Pool(processes = 3)  # 3개 동시에
    pool.map(image_download, keyword)

