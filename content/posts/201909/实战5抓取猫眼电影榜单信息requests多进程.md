title: 实战5抓取猫眼电影榜单信息（requests+多进程）
date: '2019-09-06 21:33:18'
updated: '2019-09-06 21:33:18'
tags: [python实战, python学习]
permalink: /articles/2019/09/17/1568727178145.html
---
**1**.目标网址[https://maoyan.com/board/4?offset=0](https://maoyan.com/board/4?offset=0)
一、引入相应的模块并编写获取源码的函数

```python
import requests, re, json
from lxml import etree
from multiprocessing import Pool
# 获取源码
def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    return response.text
```

二、使用肉眼大法观察源码并且编写解析信息函数：
![null](https://upload-images.jianshu.io/upload_images/10590983-32eeb2fb360604ed.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)
代码如下 ( 这里使用两种方式进行解析：***XPath 和 正则*** )：

```python
# 获取内容信息
def parse_html(html):
    selector = etree.HTML(html)
    index_list = selector.xpath('//i[starts-with(@class, "board-index board-index")]/text()')  # 排名
    img_list = selector.xpath('//img/@data-src')  # 图片链接
    title_list = selector.xpath('//p[@class="name"]//text()')  # 电影名
    name_list = selector.xpath('//p[@class="star"]/text()')  # 主演
    time_list = selector.xpath('//p[@class="releasetime"]/text()')  # 上映时间
    score1_list = selector.xpath('//i[@class="integer"]/text()')  # 评分
    score2_list = selector.xpath('//i[@class="fraction"]/text()')  # 评分

    for i in range(len(title_list)):
        yield {
            'index': index_list[i],
            'img': img_list[i],
            'title': title_list[i],
            'name': name_list[i].strip()[3:],
            'time': time_list[i].strip()[5:],
            'score': score1_list[i] + score2_list[i]
        }

    # pattern = re.compile(
    #     '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?title="(.*?)" data-act="boarditem-click".*?>'
    #     '(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    # # 匹配
    # items = re.findall(pattern, html)
    # # 变成字典       yield:生成器
    # for item in items:
    #     yield {
    #         'index': item[0],
    #         'image': item[1],
    #         'title': item[2],
    #         'actor': item[3].strip()[3:],
    #         'time': item[4].strip()[5:],
    #         'score': item[5] + item[6]
    #     }

```

三、编写一个将数据放入本地文件的函数：

```python
#  写入本地文件
def write_file(content):
    with open('d:/data/crawl/lcy.txt', 'a', encoding='utf-8') as f:  # a 模式 是追加形式，如果没有则创建
        f.write(json.dumps(content, ensure_ascii=False) + '\n')  # 进行编码以防乱码
        f.close()  # 关闭资源
```

四、再编写一个主函数用语调用其他函数：

```python
# 主函数
def main(offset):
    url = "http://maoyan.com/board/4?offset=" + str(offset)
    html = get_html(url)
    parse_html(html)
    for item in parse_html(html):
        print("正在写入-》 ", item)
        write_file(item)


if __name__ == '__main__':   # 判断文件入口
    for i in range(0, 100, 10):
        main(i)
```
执行后效果图如下：
![null](https://upload-images.jianshu.io/upload_images/10590983-fd9eb29db149a878.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

11.png

五、接下来开始引入多进程，我们对 文件入口 分支结构做如下修改即可：

```bash
if __name__ == '__main__': #判断文件入口
    # for i in range(0, 100, 10):
    #     main(i)

    # 进程池的使用有四种方式：apply_async、apply、map_async、map。
    # 其中apply_async和map_async是异步的，也就是启动进程函数之后会继续执行后续的代码
    # 不用等待进程函数返回，而apply、map是阻塞的。apply_async和map_async方式提供了一些获取进程函数
    # 状态的函数：ready()、successful()、get()。
    # PS：join()语句要放在 close()语句后面。

    pool = Pool(processes=6)  
    pool.map(main, [i+10 for i in range(10)])  # 通过构造一个数组之后，如果有新的请求添加到进程池如果其没有满则创建新进程来执行请求，如果满了则等待
    # 调用join之前，一定要先调用close() 函数，否则会出错, close()执行后不会有新的进程加入到pool,join函数等待素有子进程结束
    pool.close()
    pool.join()

```

运行后发现得到同样的效果，并且速度很快