title: centos7 安装chromedriver
date: '2019-11-30 13:21:29'
updated: '2019-11-30 13:47:42'
tags: [python实战, python学习, centos7, python3]
permalink: /articles/2019/11/30/1575091289510.html
---
## 1.安装浏览器

指定yum 源

wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo

安装
```
curl https://intoli.com/install-google-chrome.sh | bash

ldd /opt/google/chrome/chrome | grep "not found"
```
安装后，执行：
```
google-chrome-stable --no-sandbox --headless --disable-gpu --screenshot https://www.baidu.com/
```
成功之后会生成一个图片

查看 版本 很重要
```
google-chrome --version

#Google Chrome 78.0.3904.108  
#所以下载我们也只能下载对应的版本
```

## 2. 安装chromedriver
下载：https://npm.taobao.org/mirrors/chromedriver/ 索引 挑选自己系统匹配的
```
wget https://npm.taobao.org/mirrors/chromedriver/78.0.3904.11/chromedriver_linux64.zip
```
unzip 解压
```
unzip chromedriver_linux64.zip

./chromedriver

Starting ChromeDriver 79.0.3945.36 (3582db32b33893869b8c1339e8f4d9ed1816f143-refs/branch-heads/3945@{#614}) on port 9515
Only local connections are allowed.
Please protect ports used by ChromeDriver and related test frameworks to prevent access by malicious code.
[1575091012.429][SEVERE]: bind() failed: Cannot assign requested address (99)
```

如果出现了  Cannot assign requested address (99)


```
#执行命令修改如下内核参数 （需要root权限） 
#调低端口释放后的等待时间，默认为60s，修改为15~30s：

sysctl -w net.ipv4.tcp_fin_timeout=30

#修改tcp/ip协议配置， 通过配置/proc/sys/net/ipv4/tcp_tw_resue, 默认为0，修改为1，释放TIME_WAIT端口给新连接使用：

sysctl -w net.ipv4.tcp_timestamps=1

#修改tcp/ip协议配置，快速回收socket资源，默认为0，修改为1：

sysctl -w net.ipv4.tcp_tw_recycle=1

#允许端口重用：

sysctl -w net.ipv4.tcp_tw_reuse = 1
```

安装完成
 建立软连接：

ln -s /root/data/soft/chromedriver /usr/bin/chromedriver

## 3. 测试代码
```
#coding=utf8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)
#driver = webdriver.Chrome()
driver.get("https://www.baidu.com")

print(driver.page_source)
#driver.quit()
```