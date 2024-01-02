# 一个基于 Hugo 的静态响应式网址导航主题 

本项目是基于**纯静态**的网址导航网站 [webstack.cc](https://github.com/WebStackPage/WebStackPage.github.io) 制作的 [Hugo](https://gohugo.io/) 主题，是一个基于 Hugo 的静态响应式网址导航主题。<br/>

## 主题开源地址

- GitHub：[https://github.com/shenweiyan/WebStack-Hugo](https://github.com/shenweiyan/WebStack-Hugo)
- Gitee：[https://gitee.com/shenweiyan/WebStack-Hugo](https://gitee.com/shenweiyan/WebStack-Hugo)

## 主题演示地址

- [https://bioit.top](https://bioit.top)
- [https://so.gd.cn](https://so.gd.cn)


## 特色功能

这是 Hugo 版 WebStack 主题。可以借助 Github Pages 或者 Coding 直接托管部署，无需服务器。

总体说一下特点：

- 采用了一直以来最喜欢的 hugo 部署方式，方便高效。
- 主要的配置信息都集成到了 config.toml，一键完成各种自定义的配置。
- 导航的各个信息都集成在 data/webstack.yml 文件中，方便后续增删改动。
```
- taxonomy: 科研办公
  icon: fas fa-flask fa-lg
  list:
    - term: 生物信息
      links:
        - title: NCBI
          logo: ncbi.jpg
          url: https://www.ncbi.nlm.nih.gov/
          description: National Center for Biotechnology Information.
        - title: Bioconda
          logo: bioconda.jpg
          url: https://anaconda.org/bioconda/
          description: "Bioconda :: Anaconda.org."
    - term: 云服务器
      links:
        - title: 阿里云
          logo: 阿里云.jpg
          url: https://www.aliyun.com/
          description: 上云就上阿里云。
        - title: 腾讯云
          logo: 腾讯云.jpg
          url: https://cloud.tencent.com/
          description: 产业智变，云启未来。
```
- 做了手机电脑自适应以及夜间模式。
- 增加了搜索功能，以及下拉的热词选项（基于百度 API）。
- 增加了一言、和风天气的 API。

## 使用说明

这是一个开源的公益项目，你可以拿来制作自己的网址导航，也可以做与导航无关的网站。

WebStack 有非常多的魔改版本，这是其中一个。如果你对本主题进行了一些个性化调整，欢迎来本项目中 issue 分享一下！


## 安装说明

关于 Windows/Linux 下详细的安装与使用说明，请参考文档：

[WebStack-Hugo | 一个静态响应式导航主题](https://www.yuque.com/shenweiyan/cookbook/webstack-hugo) - [语雀](https://www.yuque.com/shenweiyan)


## 感谢

本主题的部分代码参考了以下几个开源项目，特此感谢。

- [WebStackPage/WebStackPage.github.io](https://github.com/WebStackPage/WebStackPage.github.io)
- [liutongxu/liutongxu.github.io](https://github.com/liutongxu/liutongxu.github.io)
- [iplaycode/webstack-hugo](https://github.com/iplaycode/webstack-hugo)

感谢以下所有朋友对本主题所做出的贡献。

[@yanbeiyinhanghang](https://github.com/yinhanghang) [@jetsung](https://github.com/jetsung)

## 赞赏

如果你觉得本项目对你有所帮助，欢迎请作者喝杯热咖啡 >.<

![donate-wecaht-aliapy](https://user-images.githubusercontent.com/26101369/212630361-aa393be8-581e-4a97-bfe2-256e883791fb.jpg)

使用说明与技巧
这是一个开源的公益项目，你可以拿来制作自己的网址导航，也可以做与导航无关的网站。

左导航栏图标
左侧、顶部导航栏图标用的都是 Font Awesome 图标库 v5 版本 Free 的图标。链接如下：

🔗 https://fontawesome.com/v5/search?o=r&m=free


调整头部搜索栏
头部搜索栏的默认位置可以通过下面的方法进行修改。

1. 直接修改 layouts/partials/content_search.html，调整对应部分的位置。
2. 调整默认的搜索（即点击"常用/搜索/工具 ...." 时下指箭头的指向），把对应的 id 添加到对应的 label 里面。



自定义头部导航
WebStack-Hugo 把头部的导航菜单的各个信息集成在了 data/header.yml 文件中，每个人可以根据自己的需要调整。
- item: 首页
  icon: fa fa-home
  link: "./"

- item: 作者
  icon: fa fa-book
  link: https://www.yuque.com/shenweiyan

- item: 配置
  icon: fa fa-cog
  link: ""
  list:
    - name: 源码
      url: "#"
    - name: 图标
      url: "#"

获取网站图标
Bio & IT 网址导航默认使用的是个人收集的网站图标，主要是查看网站源码、百度、谷歌等途径把对应导航的图标下载下来，这个方法比较原始繁琐，适合导航不是很多的情况。

你也可以使用一为提供的的 Favicon 图标 api：https://api.iowen.cn/doc/favicon.html。

接口地址：https://api.iowen.cn/favicon
返回格式：图片
请求方式：get
请求示例：
    ■ https://api.iowen.cn/favicon/www.iowen.cn.png
    ■ https://api.iowen.cn/favicon/www.baidu.com.png

请求参数说明：
名称  必填  类型  说明  
  url 是 string  需要获取图标的URL地址，如：www.iowen.cn，确保URL能够正常打开
不需要 http(s):// ，且结尾必须填 .png
返回参数说明：
名称  类型  说明
无 无 无
返回示例：返回网址图标
