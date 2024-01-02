title: Python3下request处理cookie的两种方法
date: '2020-06-16 22:29:23'
updated: '2020-06-16 22:29:23'
tags: [python3, requests, session, cookie]
permalink: /articles/2020/06/16/1592317763420.html
---
![](https://img.hacpai.com/bing/20190706.jpg?imageView2/1/w/960/h/540/interlace/1/q/100)

# 一、获取cookie

手动获取：手工登录获取cookie，登录成功后可以不断更新cookie到文件中存储。
参考：https://www.jianshu.com/p/5ef0c7bb1ed2
```
#导入requests包
import requests

targetURL = '目标网站地址'

#设置头UA
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

#开启一个session会话
session = requests.session()

#设置请求头信息
session.headers = headers

#申明一个用于存储手动cookies的字典
manual_cookies={}

##打开手动设置的cookies文件
#部分网站需要滑动验证，这里通过浏览器登录成功后获取cookies手动存到文本来绕过验证，后续cookies自动更新
with open("manual_cookies.txt",'r',encoding='utf-8') as frcookie:
    cookies_txt = frcookie.read().strip(';')  #读取文本内容
    #手动分割添加cookie
    for item in cookies_txt.split(';'):
        name,value=item.strip().split('=',1)  #用=号分割，分割1次
        manual_cookies[name]=value  #为字典cookies添加内容

#将字典转为CookieJar：
cookiesJar = requests.utils.cookiejar_from_dict(manual_cookies, cookiejar=None,overwrite=True)

#将cookiesJar赋值给会话
session.cookies=cookiesJar

#向目标网站发起请求
res = session.get(targetURL)

#将CookieJar转为字典：
res_cookies_dic = requests.utils.dict_from_cookiejar(res.cookies)

#将新的cookies信息更新到手动cookies字典
for k in res_cookies_dic.keys():
    manual_cookies[k] = res_cookies_dic[k]

print(manual_cookies)

#重新将新的cookies信息写回文本
res_manual_cookies_txt = ""

#将更新后的cookies写入到文本
for k in manual_cookies.keys():
    res_manual_cookies_txt += k+"="+manual_cookies[k]+";"

#将新的cookies写入到文本中更新原来的cookies
with open('manual_cookies.txt',"w",encoding="utf-8") as fwcookie:
    fwcookie.write(res_manual_cookies_txt);
```
## 二 、使用cookie

* 方法一： 


```
# cookies是字典格式，这种cookie不能放在headers里
cookies = {

      name1 ：value1，

      name2：value2

}

response = request.post(url, data=data, cookies=cookies)
```

* 方法二：使用requests.session, 通过CookieJar来处理cookie。

```
session = requests.session()

# cookie处理，将字典类型的cookie转换成cookiejar，由session自动处理cookie，
报文请求的时候就不需要再加上cookie了。见上面的例子，已经写的很详细了，不需要再写了
```

* 方法三，headers中加cookie。
```

headers = { 

'User-Agent':'Apache-HttpClient/4.5.2 (Java/1.8.0_66)',

'cookie':'_zap=191e4816-acf0-41ab-85ca-c54c2ff9ca1f; d_c0="ABCsEEAYPQ2PTofKIlzwxMJDdb8R-_6iVQA=|'

}

response = requests.post(url,data=data,headers=headers)
```
