title: python第二大神器requests
date: '2019-08-29 20:53:19'
updated: '2019-08-29 20:53:19'
tags: [python学习]
permalink: /articles/2019/09/16/1568643366664.html
---
**首先你要安装requests库**

安装代码：pip3 install requests

如果你没有安装pip3 请自行百度安装，本公众号已和百度达成合作不会的都可以去百度哦，不收费。

**进入正题，我们来看一下requests的强大之处吧**

1，get请求

![null](https://upload-images.jianshu.io/upload_images/9489193-886f951f9a9d0e43?imageMogr2/auto-orient/strip|imageView2/2/w/646/format/webp)

是不是简单粗暴？相比上一篇舒服多了。

有什么属性？我也不知道哎，dir()一下？

![null](https://upload-images.jianshu.io/upload_images/9489193-1d09eebf582e2d82?imageMogr2/auto-orient/strip|imageView2/2/w/1080/format/webp)

**简单介绍几个属性：**

status_code：状态码

url：url

text：内容

cookies：就是cookies

我们试着用get请求添加一些参数，用params参数就好

![null](https://upload-images.jianshu.io/upload_images/9489193-d9d2886806cd4a84.png?imageMogr2/auto-orient/strip|imageView2/2/w/660/format/webp)

返回的结果：

![null](https://upload-images.jianshu.io/upload_images/9489193-bd14dc274e8b39d8.png?imageMogr2/auto-orient/strip|imageView2/2/w/1080/format/webp)

添加headers:

以知乎为例：知乎不加头信息会500报错。

  

![null](https://upload-images.jianshu.io/upload_images/9489193-af7915045c6d82cc.png?imageMogr2/auto-orient/strip|imageView2/2/w/839/format/webp)

返回结果：

![null](https://upload-images.jianshu.io/upload_images/9489193-bed7b21410090c3c.png?imageMogr2/auto-orient/strip|imageView2/2/w/1080/format/webp)

**2，post请求以及添加参数**

![null](https://upload-images.jianshu.io/upload_images/9489193-195a63bdf0bde3ac.png?imageMogr2/auto-orient/strip|imageView2/2/w/914/format/webp)

返回结果：

![null](https://upload-images.jianshu.io/upload_images/9489193-93a52b9ef7c33d80.png?imageMogr2/auto-orient/strip|imageView2/2/w/1080/format/webp)

**3，尝试用cookies登录知乎**

其实urllib中也有有对cookies的操作，不过很麻烦，相比起来requests简单许多

登录知乎时打开开发者模式，

如图：

![null](https://upload-images.jianshu.io/upload_images/9489193-af33b89671baaa42.png?imageMogr2/auto-orient/strip|imageView2/2/w/1080/format/webp)

复制下cookie值，在headers中添加cookie值：

![null](https://upload-images.jianshu.io/upload_images/9489193-6bfa5de6d0b11ca8.png?imageMogr2/auto-orient/strip|imageView2/2/w/874/format/webp)

你会发现你已经可以看到登录后的结果了！

此时要思考一个问题，每次爬取页面不会只有一个请求，那么每次请求都要添加cookies是很麻烦的，因此就有了会话维持，就会用到requests.Session()来设置，本节先不讲，后面会提到。

**4，本节我们来简单的利用所学实现下载图片，音乐。**

下载图片：

首先找到一个图片网站：我选择的是千图网找到一张图片，右键复制链接地址

，然后写上这样一段代码：

![null](https://upload-images.jianshu.io/upload_images/9489193-ca3418a7e60a6512.png?imageMogr2/auto-orient/strip|imageView2/2/w/969/format/webp)

open()  可以对文本，图片等进行操作

open()的第一个参数是你图片存放的位置和名称，第二个参数为可进行的操作，比如w是写入，r是读取，wb是对二进制文件的操作，我们的图片，音乐都是二进制文件，运行之后你会发现，在此文件夹下已经有一张图片了，这里就不截图了，值得注意的是此时如果你要打印text会是一段乱码，因为是图片，而content会是以b开头，说明是bytes类型，是一串二进制数据。

下载音乐：

我选择的是网易云音乐，（这里要找到音乐的地址，稍微会麻烦一些）打开网易云，搜索你想要下载的音乐，然后打开开发者模式点击一下播放。

![null](https://upload-images.jianshu.io/upload_images/9489193-0d9fd96b8f305cd9.png?imageMogr2/auto-orient/strip|imageView2/2/w/1080/format/webp)

                                       

找到这首歌的url，即文件的源地址，这个地址应该是临时地址，有时间限制的。复制这个地址在新的页面打开应该是这样：

![null](https://upload-images.jianshu.io/upload_images/9489193-470c13641a64950d?imageMogr2/auto-orient/strip|imageView2/2/w/803/format/webp)

然后把请求的地址修改成你复制的地址，把存放的地址结尾改为mp3结尾即可。

![null](https://upload-images.jianshu.io/upload_images/9489193-8ab22098570a3294?imageMogr2/auto-orient/strip|imageView2/2/w/797/format/webp)

因为使用方法其实都大同小异，就没有细说，根据前面的内容，应该是可以掌握的。不懂方法，不知道什么属性help一下，常见的都写在这里，后期如果写爬虫，涉及到没说过还会继续说，毕竟在项目中才会学的更多。

完。