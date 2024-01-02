title: 爬虫之urllib库的使用
date: '2019-08-28 20:53:19'
updated: '2019-08-28 20:53:19'
tags: [python学习]
permalink: /articles/2019/09/16/1568643489909.html
---
**首先什么是库？**

简单的说就是别人写好的东西，你拿来调用就可以实现基本的操作。比如电视你只用看，不用知道他是如何成像的。

**urllib库之request（用来模拟HTTP请求）模块**

request的第一个方法urlopen()

我们以淘宝为例写上这样一段代码：

![null](https://upload-images.jianshu.io/upload_images/9489193-6f600ce5f6564529?imageMogr2/auto-orient/strip|imageView2/2/w/633/format/webp)

read()是返回得到的内容，decode('utf8')是编码格式。

返回的结果如下：

![null](https://upload-images.jianshu.io/upload_images/9489193-b57bef85105e3540?imageMogr2/auto-orient/strip|imageView2/2/w/1080/format/webp)

如果我们不想获取页面，只想获取请求的状态码或者头信息只需要

print(html.status)获取状态码,print(html.getheaders())获取头信息，可能你会说那莫多方法我怎么知道他有什么方法，此时只需要print(dir(html))一下，所有的方法，属性尽收眼底。那我怎么知道他是干什么的呢？help()一下就知道。

接下来我们来说一下urlopen()方法的参数：

我们利用上面说的去看一下有什么参数：

![null](https://upload-images.jianshu.io/upload_images/9489193-33cd735fe66f8d37?imageMogr2/auto-orient/strip|imageView2/2/w/572/format/webp)

得到如下结果：

![null](https://upload-images.jianshu.io/upload_images/9489193-9a1d2f2bb86101c3?imageMogr2/auto-orient/strip|imageView2/2/w/1080/format/webp)

卧槽？怎么全英文？？？无奈，苦逼的我只好打开谷歌翻译。。。

**data参数：**

data参数是干什么的？我们知道我们在登录的时候的会填写账号密码，那么我们模拟登录的时候也要填写，这个参数就是做这个的！值得注意的是当我们添加了这个参数之后请求方式就不再是GET，而是POST请求。并且data参数是字节流编码格式我们需要转化一下。

![null](https://upload-images.jianshu.io/upload_images/9489193-97f344cf0f55c33b?imageMogr2/auto-orient/strip|imageView2/2/w/715/format/webp)

httpbin.org/post是一个请求测试网站，如下我们可以看到我们传递的参数已经在里面了。

![null](https://upload-images.jianshu.io/upload_images/9489193-2ef7c3eee14b3b72?imageMogr2/auto-orient/strip|imageView2/2/w/967/format/webp)

**timeout参数：**

tomeout参数是设置超时时间的，如果超出这个时间未得到响应就会抛出超时异常。下面我们来练习一下：

![null](https://upload-images.jianshu.io/upload_images/9489193-af43438b3cf75583?imageMogr2/auto-orient/strip|imageView2/2/w/735/format/webp)

iisinstance()函数用来判断是否是超时，socket.timeout就是超时异常，而e.reason是捕捉的异常，做一个判断。

结果如下：

![null](https://upload-images.jianshu.io/upload_images/9489193-1b4263356cc48070?imageMogr2/auto-orient/strip|imageView2/2/w/389/format/webp)

其他参数用到的时候再说，目前不需要了解吧。

**request的第二个方法Request()**

同样以淘宝为例：

![null](https://upload-images.jianshu.io/upload_images/9489193-5ee999c2a86c7896?imageMogr2/auto-orient/strip|imageView2/2/w/549/format/webp)

结果和上面的结果是一样的，我们可以发现只是请求的对象发生了改变，这有什么用了？这样会让我们更灵活的添加参数或者配置，没什么其他卵用，来说一下Request的参数吧。

help一下：

![null](https://upload-images.jianshu.io/upload_images/9489193-20c239d12f174b19?imageMogr2/auto-orient/strip|imageView2/2/w/1080/format/webp)

url，data和上面的一样，headers表示请求头，是一个字典，我们在爬取网站的时候通常会加上一个User-Agent参数，防止被识别为爬虫，修改它，伪装成浏览器。origin_reg_host是指请求的ip或者host，unverifiable是是否有抓取的权限没有为True，否者是False，mothod为请求方式。

我们试着去添加多个参数：

![null](https://upload-images.jianshu.io/upload_images/9489193-2b6787e655a6dc8e?imageMogr2/auto-orient/strip|imageView2/2/w/1028/format/webp)

结果：

![null](https://upload-images.jianshu.io/upload_images/9489193-ee0cf3d91ff4655b?imageMogr2/auto-orient/strip|imageView2/2/w/1080/format/webp)

也可以用方法去添加，这个就自己去试吧。

**error模块**

1，URLError类

昨天我们导入包的方式感觉很烦，每次写都会很长

想要变得简单点可以这样写：

![null](https://upload-images.jianshu.io/upload_images/9489193-1f4a806076a52b53?imageMogr2/auto-orient/strip|imageView2/2/w/719/format/webp)

随便输入一个网址，并没有直接报错。

![null](https://upload-images.jianshu.io/upload_images/9489193-8d7e4de64edec396?imageMogr2/auto-orient/strip|imageView2/2/w/369/format/webp)

2，HTTPError类（针对HTTP请求错误的类，使用方式和上面的一样）

![null](https://upload-images.jianshu.io/upload_images/9489193-bbcd2a8b316b09d7?imageMogr2/auto-orient/strip|imageView2/2/w/624/format/webp)

结果：

![null](https://upload-images.jianshu.io/upload_images/9489193-a2299cddab3bd239?imageMogr2/auto-orient/strip|imageView2/2/w/768/format/webp)

reason：返回错误原因

code：返回状态码

headers：返回请求头信息

这里只针对爬虫用到的来说一下。

**parse模块**

paese模块总的来说就是对url的操作，各种解析和合并等

拆分的有：

urlparse()

urlsplit()

![null](https://upload-images.jianshu.io/upload_images/9489193-dd76a30237004ce9?imageMogr2/auto-orient/strip|imageView2/2/w/658/format/webp)

结果：

![null](https://upload-images.jianshu.io/upload_images/9489193-1dd82a00e1cf73fd?imageMogr2/auto-orient/strip|imageView2/2/w/1080/format/webp)

urlsplit()和urlparse()一样，不同是是urlsplit()的结果将parsms合并到了path里

合并的有：

urlunparse()合并的列表长度必须为6个

urlunsplit()合并的列表长度变成了5个

![null](https://upload-images.jianshu.io/upload_images/9489193-e70588744c8e9fdb?imageMogr2/auto-orient/strip|imageView2/2/w/737/format/webp)

结果：

![null](https://upload-images.jianshu.io/upload_images/9489193-ee194bc94606c24a?imageMogr2/auto-orient/strip|imageView2/2/w/689/format/webp)

urlunsplit()的写法也一样只是变成了长度变成了5。

序列化和反序列化（我的理解是转化成符合某种格式）

urlencode():将字典转化为get请求的编码格式

parse_qs():将GET请求的参数转化成字典

![null](https://upload-images.jianshu.io/upload_images/9489193-1a65ac986eacf2ea?imageMogr2/auto-orient/strip|imageView2/2/w/486/format/webp)

结果 ：

![null](https://upload-images.jianshu.io/upload_images/9489193-0e50b43d445b19fb?imageMogr2/auto-orient/strip|imageView2/2/w/537/format/webp)

当url中有汉字时我们需要转化成url的编码格式quote（）转化回来unquote（）

![null](https://upload-images.jianshu.io/upload_images/9489193-41e5e1dadd1474c9?imageMogr2/auto-orient/strip|imageView2/2/w/638/format/webp)

结果：

![null](https://upload-images.jianshu.io/upload_images/9489193-5cdeb24b14b76ea8?imageMogr2/auto-orient/strip|imageView2/2/w/557/format/webp)

其实上面讲的有三个模块，request请求模块，parse对url的处理模块和error异常处理模块。

done