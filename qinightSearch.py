import requests
import os
from selenium import webdriver
import re
from urllib.parse import urlparse

url = "https://nav.qinight.com/"
# output_dir = "D:\java\webstack\webstack-jackssybin\images\\"
# output_dir = "D:\code\webstack\webstack-jackssybin\themes\WebStack-Hugo\static\assets\images\logos"
output_dir = "D:\\data\\images\\"
# 创建列表用于存放字典
result_list = []
# 存放分组的字典 group,list
result_group_dict ={}
group_type_dict = {}
# 创建字典存放属性值
result_dict = {}

def writeDetailByDictMap():
    global e
    # 打印列表
    for entry in result_group_dict:
        print("================================================" + entry)
        for val in result_group_dict[entry]:
            print(val)
    # 指定输出文件路径
    output_file_path = 'output_file.txt'
    # 打开文件以写入内容
    with open(output_file_path, 'w',encoding='UTF-8') as output_file:
        # 遍历字典中的每一项，按指定格式写入文件
        for key, value in result_group_dict.items():
            output_file.write(f"- taxonomy: {key}\n")
            output_file.write(f"  icon: {group_type_dict[key]} \n")
            output_file.write(f"  list:\n")
            output_file.write(f"    - term: {key}\n")
            output_file.write(f"      links:\n")
            for result_dict_value in value:
                output_file.write(f"        - title: '{result_dict_value['Alt']}'\n")
                output_file.write(f"          url: {result_dict_value['Href']}\n")
                output_file.write(f"          logo: {result_dict_value['Alt']}.png\n")
                output_file.write(f"          description: {result_dict_value['Title']}\n")
            output_file.write(f"\n")


# # 创建列表用于存放字典
# result_list = []
# # 存放分组的字典 group,list
# result_group_dict ={}
# # 创建字典存放属性值
# result_dict = {}
# result_dict['Data-Src'] = img_tag.get('data-src', '')
# result_dict['Alt'] = alt_str
# result_dict['Group']
# result_dict['Title'] = a_tag.get('title', '')
# result_dict['Href'] = a_tag.get('href', '')

# 分类
# result_list.append(result_dict)
# result_group_dict[result_dict['Group']]=result_list
# 详情
def crawlDetail():
    driver = webdriver.Chrome()
    driver.get(url)
    global result_dict, result_list
    divClassTypes = driver.find_elements_by_class_name('site-name')
    divDetailNams = driver.find_elements_by_class_name('site-list')
    type_index = 0
    for typeClass in divClassTypes:
        try:
            typeClassFaIcon = typeClass.find_element_by_tag_name("i").get_attribute("class")
            group_text = typeClass.text
            print(group_text + " _ " + typeClassFaIcon)
            group_type_dict[group_text] = typeClassFaIcon

            divDetail = divDetailNams[type_index]
            # for divDetail in divDetailNams:
            urlLists = divDetail.find_elements_by_class_name("urllist")
            for urlDetail in urlLists:
                result_dict = {}
                # result_dict['Href'] = urlDetail.get_attribute("data-url")
                aDetail = urlDetail.find_element_by_tag_name("a")
                imgDetail = urlDetail.find_element_by_tag_name("img")
                pDetail = urlDetail.find_elements_by_tag_name("p")
                result_dict['Data-Src'] = imgDetail.get_attribute("src")
                result_dict['Href'] = aDetail.get_attribute("href")
                icon_domain = get_domain_from_url(result_dict['Href'])
                icon_title = remove_douhao(icon_domain)
                result_dict['Alt'] = remove_spaces_rep(icon_title)
                # 下载图片
                output_path = os.path.join(output_dir, result_dict['Alt'] + ".png")
                if not file_exists(output_path):
                    icon_url = "https://api.iowen.cn/favicon/" + icon_domain + ".png"
                    print(icon_url)
                    download_image(icon_url, output_path)
                result_dict['Title'] = pDetail[1].text
                result_dict['Group'] = group_text
                result_list.append(result_dict)
        except Exception as e:
            print("=========error============="+e)
            pass
        result_group_dict[group_text] = result_list
        print(result_list)
        result_list = []
        type_index = type_index + 1
    driver.quit()

def get_domain_from_url(url):
    # 解析URL
    parsed_url = urlparse(url)
    # 提取域名
    domain = parsed_url.netloc
    # 使用正则表达式提取域名（不包括端口号）
    domain = re.search(r'^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)', domain).group(1)
    return domain
def file_exists(file_path):
    return os.path.exists(file_path)
def remove_spaces_rep(string):
    return string.replace(" ", "")

def remove_douhao(string):
    return string.replace(".","")
def download_image(url, output_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded to {output_path}")
    else:
        print("Failed to download image")


def main():
    print("Hello, World!")
    crawlDetail()
    writeDetailByDictMap()
    # print(get_domain_from_url("http://www.baiu.com"))

if __name__ == '__main__':
    main()