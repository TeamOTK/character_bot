from bs4 import BeautifulSoup
import lxml
import os
import warnings
from tqdm import tqdm
import time
import csv
from csv import writer
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

import json

warnings.filterwarnings('ignore')
options = Options()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
## for background
options.add_argument("headless") ## 크롤링 창 보이게 하려면 주석 처리
options.add_argument('--window-size=1920, 1080')
options.add_argument('--no-sandbox')
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--start-maximized') 
#options.add_argument('--start-fullscreen') ## 전체 화면 없애려면 주석 처리
options.add_argument('--disable-blink-features=AutomationControlled')

class Namu:
    def __init__(self, save_path):
        self.url = 'https://namu.wiki/w/%ED%95%9C%ED%95%B4%EB%82%98'
        self.save_path = save_path
    
    def __wait_until_find(self, driver, xpath):
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        return element
            
    def __wait_and_click(self, driver, xpath):
        WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        button = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button)
    
    def get_info(self):
        ## Selenium
        driver = webdriver.Chrome(service=Service(), options=options)
        driver.get(self.url)
        
        ## BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        text = soup.get_text()
        title = text.split("1. 개요[편집]")[1].split("2. 정체(?)[편집]")[0]
        bg = text.split("2. 정체(?)[편집]")[1].split("3. 대인 관계[편집]")[0]
        story = text.split("5. 여담[편집]")[1].split("6. 어록[편집]")[0]
        line = text.split("6. 어록[편집]")[1].split("파워링크")[0]
        
        
        # contents = soup.find_all("div", class_="_1TSYs3S7")
        # for content in contents:
        #     print(content.text)
        
        #print(text)       
        driver.quit()
        
        return {'title': title, 'bg': bg, 'story': story, 'line': line}

        
    def save_csv(self, filename, reply_list):
        if not os.path.exists(os.path.dirname(self.save_path + filename)):
            os.makedirs(os.path.dirname(self.save_path + filename))
    
        with open(self.save_path+filename, 'w', newline='') as f:
            wr = csv.writer(f)
            wr.writerow(['reply'])
            for reply in reply_list:
                wr.writerow([reply.string])  
    
if __name__ == '__main__':
    
    save_path = 'src/data/hhn.json'
    
    crawler = Namu(save_path)
    information = crawler.get_info()

    with open(save_path, 'w', encoding="utf-8") as json_file:
        json.dump(information, json_file, ensure_ascii=False)