title: selenium经常使用api
date: '2019-10-28 17:17:13'
updated: '2020-03-30 00:38:52'
tags: [python学习]
permalink: /articles/2019/10/28/1572254233777.html
---
![](https://img.hacpai.com/bing/20180107.jpg?imageView2/1/w/960/h/540/interlace/1/q/100) 

[python-selenium官方文档可详细看用法](https://python-selenium-zh.readthedocs.io/zh_CN/latest/7.WebDriver%20API/)
### 1.浏览器chromeDriver获取信息
1.driver.current_url：用于获得当前页面的URL
2.driver.title：用于获取当前页面的标题
3.driver.page_source:用于获取页面html源代码  
4.driver.current_window_handle:用于获取当前窗口句柄  
5.driver.window_handles:用于获取所有窗口句柄  
6.driver.find_element_by***** 定位元素，有18种  
7.driver.get(url):浏览器加载url。  
8.driver.forward()：浏览器向前（点击向前按钮）。  
9.driver.back()：浏览器向后（点击向后按钮）。  
10.driver.refresh()：浏览器刷新（点击刷新按钮）。  
11driver.close()：关闭当前窗口，或最后打开的窗口。  
12.driver.quit():关闭所有关联窗口，并且安全关闭session。  
13.driver.maximize_window():最大化浏览器窗口。  
14.driver.set_window_size(宽，高)：设置浏览器窗口大小。  
15.driver.get_window_size()：获取当前窗口的长和宽。  
16.driver.get_window_position()：获取当前窗口坐标。  
17.driver.get_screenshot_as_file(filename):截取当前窗口。  
18.driver.implicitly_wait(秒)：隐式等待，通过一定的时长等待页面上某一元素加载完成。若提前定位到元素，则继续执行。若超过时间未加载出，则抛出NoSuchElementException异常。  
19.driver.switch_to_frame(id或name属性值)：切换到新表单(同一窗口)。若无id或属性值，可先通过xpath定位到iframe，再将值传给switch_to_frame()  
driver.switch_to.frame(id或name,或定位到的frame)  
20.driver.switch_to.parent_content():跳出当前一级表单。该方法默认对应于离它最近的switch_to.frame()方法。  
21.driver.switch_to.default_content():跳回最外层的页面。  
22.driver.switch_to_window(窗口句柄)：切换到新窗口。  
23.driver.switch_to.window(窗口句柄):切换到新窗口。  
24.driver.switch_to_alert():警告框处理。处理JavaScript所生成的alert,confirm,prompt.  
25.driver.switch_to.alert():警告框处理。  
26.driver.execute_script(js):调用js。  
27.driver.get_cookies():获取当前会话所有cookie信息。  
28.driver.get_cookie(cookie_name)：返回字典的key为“cookie_name”的cookie信息。  
29.driver.add_cookie(cookie_dict):添加cookie。“cookie_dict”指字典对象，必须有name和value值。  
30.driver.delete_cookie(name,optionsString):删除cookie信息。  
31.driver.delete_all_cookies():删除所有cookie信息。
>*find_element_by_id 
*find_element_by_name 
*find_element_by_xpath 
*find_element_by_link_text 
*find_element_by_partial_link_text 
*find_element_by_tag_name 
*find_element_by_class_name 
*find_element_by_css_selecto  ##这个经常用

### 2.获取元素之后，属性事件
1.element.size:获取元素的尺寸。  
2.element.text：获取元素的文本。  
3.element.tag_name:获取标签名称。  
4.element.clear():清除文本。  
5.element.send_keys(value):输入文字或键盘按键（需导入Keys模块）。  
6.element.click()：单击元素。  
7.element.get_attribute(name):获得属性值  
8.element.is_displayed():返回元素结果是否可见（True 或 False）  
9.element.is_selected():返回元素结果是否被选中（True 或 False）  
10.element.find_element*():定位元素，用于二次定位。

### 3.通过属性获取元素，并执行js事件
```
 send_code_wrapper = self.driver.find_element_by_xpath('//div[@node-type="activation_wrapper"]')
            send_code_flag = send_code_wrapper.is_displayed()
            if not send_code_flag:
                try:
                    js = 'arguments[0].style.display = "block"'
                    self.driver.execute_script(js, send_code_wrapper)
                except:
 //document.evaluate(\\"//div[@node-type=\\"activation_wrapper\\"]\\", document, null,XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.style.display = "block"
                    pass
```

### 3.具体使用
```
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
if __name__ == '__main__':
    #  0 读取版本信息
    chromedriver = "D:\code\good_items\Panda-Learning\chrome\chromedriver.exe"
    os.environ["webriver.chrome.driver"] = chromedriver
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get('http://www.baidu.com')
    input=browser.find_element_by_id("kw")
    input.send_keys("jackssybin.cn")
    search_btn = browser.find_element_by_id("su")
    search_btn.click()
    print(browser.page_source)

```
