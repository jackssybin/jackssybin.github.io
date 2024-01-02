title: python3下chromedriver + headless + proxy+场景
date: '2019-12-14 23:54:51'
updated: '2019-12-14 23:54:51'
tags: [python3, python学习, python实战, chromedriver]
permalink: /articles/2019/12/14/1576338890909.html
---
### 1.标准头
```
# 导入selenium的浏览器驱动接口
from selenium import webdriver

# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys

# 导入chrome选项
from selenium.webdriver.chrome.options import Options

chromeOptions.add_argument('--headless') #浏览器无窗口加载
chromeOptions.add_argument('--disable-gpu') #不开启GPU加速
   ##解决报错:
    selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start: exited abnormally
    (unknown error: DevToolsActivePort file doesn't exist)
    """
    chromeOptions.add_argument('--disable-dev-shm-usage')  #禁止
    chromeOptions.add_argument('--no-sandbox')#以根用户打身份运行Chrome，使用-no-sandbox标记重新运行Chrome
    """
    #其它设置(可选):
    #chromeOptions.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
    #chromeOptions.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
    #chromeOptions.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")  #伪装其它版本浏览器,有时可以解决代码在不同环境上的兼容问题,或者爬虫cookie有效性保持一致需要设置此参数
```
#### （1）第一个例子：抓取页面内容，生成页面快照

```
# 创建chrome浏览器驱动，
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)

# 加载百度页面
driver.get("http://www.baidu.com/")
# time.sleep(3)

# 获取页面名为wrapper的id标签的文本内容
data = driver.find_element_by_id("wrapper").text
print(data)

# 打印页面标题 "百度一下，你就知道"
print(driver.title)

# 生成当前页面快照并保存
driver.save_screenshot("baidu.png")

# 关闭浏览器
driver.quit()
```

#### （2）模拟用户输入和点击搜索

```
# get方法会一直等到页面被完全加载，然后才会继续程序，通常测试会在这里选择 time.sleep(2)
    driver.get("http://www.baidu.com/")

    # id="kw"是百度搜索输入框，输入字符串"程序猿"
    driver.find_element_by_id("kw").send_keys(u"程序猿")

    # id="su"是百度搜索按钮，click() 是模拟点击
    driver.find_element_by_id("su").click()
    time.sleep(3)

    # 获取新的页面快照
    driver.save_screenshot("程序猿.png")

    # 打印网页渲染后的源代码
    print(driver.page_source)

    # 获取当前页面Cookie
    print(driver.get_cookies())

    # ctrl+a 全选输入框内容
    driver.find_element_by_id("kw").send_keys(Keys.CONTROL, 'a')

    # ctrl+x 剪切输入框内容
    driver.find_element_by_id("kw").send_keys(Keys.CONTROL, 'x')

    # 输入框重新输入内容
    driver.find_element_by_id("kw").send_keys("美女")

    # 模拟Enter回车键
    driver.find_element_by_id("su").send_keys(Keys.RETURN)
    time.sleep(3)

    # 清除输入框内容
    driver.find_element_by_id("kw").clear()

    # 生成新的页面快照
    driver.save_screenshot("美女.png")

    # 获取当前url
    print(driver.current_url)

    # 关闭浏览器
    driver.quit()
```

#### （3）模拟用户登录


```
#加载微博登录页
    driver.get("http://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=")
    time.sleep(3)

    # 找到输入框，键入用户名和密码
    driver.find_element_by_id('loginName').send_keys("worio.hainan@163.com")
    driver.find_element_by_id('loginPassword').send_keys("Qq94313805")

    # 点击登录按钮
    driver.find_element_by_id('loginAction').click()
    time.sleep(3)

    # 快照显示已经成功登录
    print(driver.save_screenshot('jietu.png'))
    driver.quit()
```


#### （4）使用cookies登录
```
    # 加载知乎主页，查看快照知此时处于未登录状态
    driver.get("https://www.zhihu.com")
    time.sleep(1)
    print(driver.save_screenshot("zhihu_nocookies.png"))

    # 操作浏览器登录知乎并抓包cookies
    zhihu_cookies = {
        'aliyungf_tc' : 'dddddddddddddddddd',
        'l_n_c': '1'
    }

    # 将用户登录产生的cookies全部添加到当前会话
    for k, v in zhihu_cookies.items():
        driver.add_cookie({'domain': '.zhihu.com', 'name': k, 'value': v})

    # 再次访问知乎主页并拍照，此时已经是登录状态了
    driver.get("https://www.zhihu.com")
    time.sleep(3)
    print(driver.save_screenshot("zhihu_cookies.png"))

    # 退出浏览器
    driver.quit()
```
#### （5）模拟滚动条的滚动（这个用常规的爬虫很难实现）

```
# 加载知乎主页
    driver.get("https://www.zhihu.com")
    time.sleep(1)

    # 加载本地cookies实现登录
    for k, v in zhihu_cookies.items():
        driver.add_cookie({'domain': '.zhihu.com', 'name': k, 'value': v})

    # 以登录状态再次发起访问
    driver.get("https://www.zhihu.com")
    time.sleep(3)

    # 将页面滚动到最后，执行多次
    for i in range(3):
        js = "var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)
        time.sleep(3)

    # 截图并退出，页面侧边滚动条已经下滑了许多像素
    print(driver.save_screenshot("zhihu_scroll.png"))
    driver.quit()
```

#### （6）一边滚动一边加载   
 ```
# 加载知乎主页
    driver.get("https://www.zhihu.com")
    time.sleep(1)

    # 加载本地cookies实现登录
    for k, v in zhihu_cookies.items():
        driver.add_cookie({'domain': '.zhihu.com', 'name': k, 'value': v})

    # 以登录状态再次发起访问
    driver.get("https://www.zhihu.com")
    time.sleep(3)

    # 将页面滚动到最后，执行多次
    for i in range(3):
        js = "var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)
        time.sleep(3)

    # 截图并退出，页面侧边滚动条已经下滑了许多像素
    print(driver.save_screenshot("zhihu_scroll.png"))
    driver.quit()
```
#### （7）代理访问
```
PROXY = "http://127.0.0.1:8080"
#_____________________启动参数___________________________
options = webdriver.ChromeOptions()
options.add_argument('--headless')  
options.add_argument('--disable-gpu')  
options.add_argument("window-size=1024,768")  
options.add_argument("--no-sandbox")
 
#_____________________代理参数___________________________
desired_capabilities = options.to_capabilities()
desired_capabilities['acceptSslCerts'] = True
desired_capabilities['acceptInsecureCerts'] = True
desired_capabilities['proxy'] = {
    "httpProxy": PROXY,
    "ftpProxy": PROXY,
    "sslProxy": PROXY,
    "noProxy": None,
    "proxyType": "MANUAL",
    "class": "org.openqa.selenium.Proxy",
    "autodetect": False,
}
#_____________________启动浏览器___________________________
driver = webdriver.Chrome(
    chrome_options=options, 
    executable_path=CHROME_DRIVER_PATH,
    desired_capabilities = desired_capabilities,
                         )
```
