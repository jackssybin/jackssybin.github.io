title: 实战4Scrapy自动爬取腾讯招聘职位信息
date: '2019-09-05 20:53:19'
updated: '2019-09-17 01:06:30'
tags: [scrapy, python实战]
permalink: /articles/2019/09/17/1568651606327.html
---
![](https://img.hacpai.com/bing/20180613.jpg?imageView2/1/w/960/h/540/interlace/1/q/100) 

###### 创建爬虫项目:

*scrapy startproject 项目名*
*scrapy startproject tencent*

###### 查看当前可以使用的爬虫模板:

*scrapy genspider -l*

###### 基于任意模板生成一个爬虫文件:

*scrapy genspider -t 模板 自定义爬虫名 域名*
*scrapy genspider -t basic tencentSpider careers.tencent.com*

###### 执行爬虫文件(后面有：--nolog 表示不打印日记):

scrapy crawl 爬虫名 --nolog
#### 我们打开腾讯招聘网页，并观察切换页面时候的变化以及我们需要爬取的信息字段的效果图如下：
![null](https://upload-images.jianshu.io/upload_images/10590983-76ed68c20d3da523.png?imageMogr2/auto-orient/strip|imageView2/2/w/881/format/webp)

#### 修改了实体文件之后，我们在观察需要提取数据的标签特点，效果图如下：
![null](https://upload-images.jianshu.io/upload_images/10590983-0af800ace2b66334.png?imageMogr2/auto-orient/strip|imageView2/2/w/1157/format/webp)

#### 从途中可以看到，我们需要的数据都在 tr 标签中，但是细心的同学会发现，由于这些列表是斑马线的颜色，因此他们有两个不同的 class 属性类型，好了，我们现在Spisers 文件夹下创建一个基于 basic 模板的爬虫文件并处理爬取操作：
```
# -*- coding: utf-8 -*-

import scrapy
from tencent.items import TencentItem


class TencentSpider(scrapy.Spider):
    name = 'tencentspider'  # 爬虫名
    allowed_domains = ['tencent.com']  # 指定爬取的域名

    # 拼接 url
    myUrl = "https://hr.tencent.com/position.php?&start="
    offset = 0

    start_urls = [myUrl + str(offset)]  # 开始爬取的url

    def parse(self, response):
        # 获取所有tr列表标签
        node_list = response.xpath('//tr[@class="even"]|//tr[@class="odd"]')

        # 循环抓取tr标签列表里的具体数据
        for node in node_list:
            # 创建一个容器对象用于存储每个数据
            item = TencentItem()

            item['positionName'] = node.xpath('./td[1]/a/text()').extract_first()
            item['positionLink'] = node.xpath('./td[1]/a/@href').extract_first()

            # 类别有可能为空，因此需要判断一下
            if len(node.xpath('./td[2]/text()')):
                item['positionType'] = node.xpath('./td[2]/text()').extract_first()
            else:
                item['positionType'] = ""

            item['peopleNumber'] = node.xpath('./td[3]/text()').extract_first()
            item['workLocation'] = node.xpath('./td[4]/text()').extract_first()
            item['publishTime'] = node.xpath('./td[5]/text()').extract_first()

            # yield 的重要性，是返回数据后还能回来接着执行后面的代码，return 就直接结束了
            yield item  # 将数据返回给引擎在转交管道处理

        # 第一种方式：拼接url    使用场景：页面没有可以点击的请求链接，必须
        # 通过拼接url才能获取响应
        if self.offset < 400:
            # 重新拼接url
            self.offset += 10
            url = self.myUrl + str(self.offset)
            # 构建并发送请求给引擎再转交调度器
            yield scrapy.Request(url, callback=self.parse)  # 回调方法处理的是请求之后的数据
``````
#### 要实现实体管道功效就必须要在 settings.py 文件中激活：
```
#激活管道组件
ITEM_PIPELINES = {
   'tencent.pipelines.TencentPipeline': 300,
}
``````
#### 为防止网站反爬，我们可以设置文件的相应配置：
```
#设置请求头  - 用户代理
DEFAULT_REQUEST_HEADERS = {
  'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

#禁用 COOKIE
COOKIES_ENABLED = False

# Obey robots.txt rules  是否遵循网站协议
ROBOTSTXT_OBEY = True #建议遵循网站规则，也是尊重他人的表现

#设置下载延时
DOWNLOAD_DELAY = 0.3 
```
#### 万事俱备，接下来我们执行以下我们的爬虫文件(注意：执行的爬虫名字是爬虫文件里的名字而非爬虫文件名)后其中的最终效果图如下：
![null](https://upload-images.jianshu.io/upload_images/10590983-f38299f47be4d20d.png?imageMogr2/auto-orient/strip|imageView2/2/w/1049/format/webp)

#### 到目前为止项目基本完成，其实如果我们想自动爬取所有信息并且网页上有翻页按钮即“下一页”的时候，我们可以使用以下方式进行实现：

```csharp
  #第二种方式：直接从 response 获取需要爬取的链接并发送请求处理，直到链接全部提取完为止
        if len(response.xpath('//a[@class="noactive" and @id="next"]')) == 0:
            #获取“下一页”按钮的链接
            url = response.xpath('//a[@id="next"]/@href').extract_first()
            #构建链接并发送请求
            yield scrapy.Request("https://hr.tencent.com/"+ url, callback = self.parse)

```
参考:[https://www.jianshu.com/p/6935b36fd86c](https://www.jianshu.com/p/6935b36fd86c)