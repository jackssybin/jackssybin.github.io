title: ubutun安装chrome浏览器
date: '2019-11-04 20:26:08'
updated: '2019-11-04 20:27:49'
tags: [待分类, python学习]
permalink: /articles/2019/11/04/1572870368019.html
---
![](https://img.hacpai.com/bing/20190814.jpg?imageView2/1/w/960/h/540/interlace/1/q/100) 

### 一、安装Chrome浏览器

**1、安装依赖**

> ```
> sudo apt-get install libxss1 libappindicator1 libindicator7
> ```

**2、下载Chrome安装包**

> ```
> wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
> ```

**3、安装**

> ```
> sudo dpkg -i google-chrome*.deb
> 
> ```
> 
> ```
> sudo apt-get install -f
> ```
**4、ubuntu如何安装lsb_release工具?**
```
sudo apt-get install lsb-core -y
```
### **二、安装ChromeDriver**

**1、安装`xvfb`以便我们可以无头奔跑地运行Chrome**

> ```
> sudo apt-get install xvfb
> ```

**2、安装依赖**

> ```
> sudo apt-get install unzip
> ```

**3、下载安装包**

> ```
> wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip
> 
> ```

**`4、解压缩+添加执行权限`**

> ```
> unzip chromedriver_linux64.zip
> ```

**5、移动**

> ```
> sudo mv -f chromedriver /usr/local/share/chromedriver
> ```

**6、建立软连接**

> ```
> sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
> sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
> ```

### 三、无头运行Chrome

**1、安装Python依赖**

> pip3 install selenium
> 
> pip3 install pyvirtualdisplay

**2、开干**
```
from selenium import webdriver
driver = webdriver.Chrome() # 初始化Chrome
driver.get('https://jackssybin.cn/articles/2019/11/04/1572870368019.html')
print(driver.title)

```