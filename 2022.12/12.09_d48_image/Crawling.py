from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import PIL
from PIL import Image
from io import BytesIO
import urllib.request
import time, os, base64

def selenium_scroll_option(driver):
    SCROLL_PAUSE_SEC = 3

    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(SCROLL_PAUSE_SEC)

        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

def main():
    os.makedirs('./crawling', exist_ok=True)
    search_list = input('검색어 입력(,로 구분) :')
    N = input('수집할 데이터 개수 :')
    search_list = [i.strip() for i in search_list.split(',')]
    
    chrome_web = webdriver.Chrome()
    chrome_web.implicitly_wait(10)

    for search in search_list:
        img_dir = f'./crawling/{search}'
        os.makedirs(img_dir, exist_ok=True)
        chrome_web.get('https://google.com')
        elem = chrome_web.find_element(By.NAME, 'q')
        elem.clear()
        elem.send_keys(search)
        elem.send_keys(Keys.RETURN)
        assert 'No results found.' not in chrome_web.page_source

        chrome_web.find_element(By.XPATH, '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()
        selenium_scroll_option(chrome_web)

        chrome_web.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input').click()
        selenium_scroll_option(chrome_web)
        img_srcs = chrome_web.find_elements(By.CLASS_NAME, 'rg_i')

        url_list = []
        cnt = 0
        for idx, img_src in enumerate(img_srcs):
            base64_image = img_src.get_attribute('src')
            try:
                if base64_image:
                    if 'base64' in base64_image:
                        img = Image.open(BytesIO(base64.b64decode(base64_image.split(',')[-1])))
                        img.save(os.path.join(img_dir, search + str(idx) + '.png'))
                        last = idx + 1
                        cnt += 1
                    else:
                        url_list.append(base64_image)

            except PIL.UnidentifiedImageError:
                print(base64_image)
            except AttributeError:
                print(base64_image)
                continue
            if int(N) == idx:
                break
        [urllib.request.urlretrieve(url, os.path.join(img_dir, search + str(last+i) + '.png')) for i, url in enumerate(set(url_list))]
        print(len(set(url_list)) + cnt)
    
    chrome_web.close()

if __name__ == '__main__':
    main()



