# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import os
import requests
import time
import random
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.webdriver.common.by import By
# session = requests.session()
# max_retries = 3
# driver = webdriver.Chrome()

url = "https://ai-bot.cn/"
# output_dir = "D:\java\webstack\webstack-jackssybin\images\\"
output_dir = "D:\\code\\webstack\\webstack-jackssybin\\themes\\WebStack-Hugo\\static\\assets\\images\\logos\\"
# response = requests.get(url)
# driver.get(url)

# https://api.iowen.cn/favicon/www.baidu.com.png

def download_image(url, output_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded to {output_path}")
    else:
        print("Failed to download image")

if __name__ == '__main__':
    title="nav.qinight.com"
    url ="https://api.iowen.cn/favicon/"+title+".png"
    print(url)
    download_image(url,output_dir+"qinight.png")