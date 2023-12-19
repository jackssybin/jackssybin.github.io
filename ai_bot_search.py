import requests
from bs4 import BeautifulSoup
import os
import requests
import time
import random
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.webdriver.common.by import By
session = requests.session()
max_retries = 3
driver = webdriver.Chrome()

headers_list = [
    {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666'
    }, {
        'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320'
    }, {
        'user-agent': 'Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+'
    }, {
        'user-agent': 'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML like Gecko) Version/7.2.1.0 Safari/536.2+'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G950U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G965U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; SM-T837A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; U; en-us; KFAPWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGMS323 Build/KOT49I.MS32310c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 550) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/14.14263'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 10 Build/MOB31T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 5X Build/OPR4.170623.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 6 Build/N6F26U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 6P Build/OPP3.170518.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 520)'
    }, {
        'user-agent': 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 9; Pixel 3 Build/PQ1A.181105.017.A1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
    }, {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    }, {
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
    }
]


requests.adapters.DEFAULT_RETRIES = 5


url = "https://ai-bot.cn/"
output_dir = "D:\java\webstack\webstack-jackssybin\images\\"
response = requests.get(url)
driver.get(url)


def download_image(url, output_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded to {output_path}")
    else:
        print("Failed to download image")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有 <div> 标签中 class 为 "url-body" 的元素
    url_body_elements = soup.select('div.url-body')

    # 创建列表用于存放字典
    result_list = []
    # 存放分组的字典 group,list
    result_group_dict ={}

    filter_dict = {}
    # 遍历每个 url-body 元素，找到第一个 <a> 标签和第一个 <img> 标签
    for url_body in url_body_elements:
        # 创建字典存放属性值
        result_dict = {}
        # 查找第一个 <img> 标签
        img_tag = url_body.find('img')
        # 获取 <img> 标签的 data-src 属性
        if img_tag:
            result_dict['Data-Src'] = img_tag.get('data-src', '')
            alt_str = img_tag.get('alt', '')
            if alt_str in filter_dict:
                continue
            filter_dict['Alt'] = alt_str
            result_dict['Alt'] = alt_str
            output_path = os.path.join(output_dir, result_dict['Alt'] + ".png")
            # download_image(result_dict['Data-Src'], output_path)

        tabContent_tag = url_body.find_parent('div', class_='tab-content')
        if tabContent_tag is None:
            continue
        preDiv_tag = tabContent_tag.find_previous('div')

        if preDiv_tag is not None:
            pageNumber_tag = preDiv_tag.find("li",class_="pagenumber")
            if pageNumber_tag is not None:
                result_dict['Group'] = pageNumber_tag.text.strip()
            else:
                result_dict['Group'] = "emptyGroup"
        else:
            result_dict['Group'] = "emptyGroup"

        result_list =result_group_dict.get(result_dict['Group'],[])

        # 查找第一个 <a> 标签
        a_tag = url_body.find('a')
        # 获取 <a> 标签的 title 和 href 属性
        if a_tag:
            result_dict['Title'] = a_tag.get('title', '')
            href_temp = a_tag.get('href', '')
            # result_dict['Href'] = a_tag.get('href', '')

            headers = random.choice(headers_list)
            # href_true_response = requests.get(href_temp)


            for _ in range(max_retries):
                try:
                    # href_true_response = session.get(href_temp, headers=headers, verify=False, timeout=20)
                    # href_soup = BeautifulSoup(href_true_response.text, 'html.parser')
                    # # 查找所有 <div> 标签中 class 为 "url-body" 的元素
                    # span_elements = href_soup.select('span.site-go-url')[0].find('a')
                    # result_dict['Href'] = span_elements.get('href', '')
                    # time.sleep(1)
                    driver.get(href_temp)
                    time.sleep(3)
                    try:
                        # 查找第一个符合条件的 a 标签
                        # span_element = driver.find_element_by_css_selector('span.site-go-url')
                        span_element = driver.find_element(By.CSS_SELECTOR, 'span.site-go-url')
                        # a_element = span_element.find_element_by_css_selector('a')
                        a_element = span_element.find_element(By.TAG_NAME, 'a')
                        # 获取并打印 href 属性
                        href_value = a_element.get_attribute('href')
                        print("第一个符合条件的 a 标签的 href 属性值:", href_value)
                        result_dict['Href'] = href_value
                    except Exception as e:
                        print("未找到符合条件的元素:"+href_temp)
                        result_dict['Href'] = href_temp
                    # Process the response here
                    break  # Break out of the loop if the request is successful
                except ConnectionError as e:
                    print(f"ConnectionError: {e}")
                    # You can log the error or take other actions if needed
                    pass
            else:
                # This block runs if the loop completes without a successful request
                print("Max retries reached. Unable to establish a connection.")

        # 将字典添加到列表中
        result_list.append(result_dict)
        result_group_dict[result_dict['Group']]=result_list

    # 打印列表
    for entry in result_group_dict:
        print("================================================"+entry)
        for val in result_group_dict[entry]:
            print(val)

    # 指定输出文件路径
    output_file_path = 'output_file.txt'

    # 打开文件以写入内容
    with open(output_file_path, 'w') as output_file:
        # 遍历字典中的每一项，按指定格式写入文件
        for key, value in result_group_dict.items():
            output_file.write(f"- taxonomy: AI学习\n")
            output_file.write(f"  icon: fas fa-pencil-alt fa-lg\n")
            output_file.write(f"  list:\n")
            output_file.write(f"    - term: {key}\n")
            output_file.write(f"      links:\n")
            for result_dict_value in value:
                output_file.write(f"        - title: {result_dict_value['Alt']}\n")
                try:
                    output_file.write(f"          url: {result_dict_value['Href']}\n")
                except Exception as e:
                    print("没有对应找到对应的链接地址:"+result_dict_value['Alt'], e)
                output_file.write(f"          logo: {result_dict_value['Alt']}.png\n")
                output_file.write(f"          description: {result_dict_value['Title']}\n\n")

else:
    print("无法获取网页内容，状态码:", response.status_code)



