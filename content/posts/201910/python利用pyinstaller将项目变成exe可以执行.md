title: python利用pyinstaller将项目变成exe可以执行
date: '2019-10-09 16:19:39'
updated: '2019-10-09 16:20:03'
tags: [python实战]
permalink: /articles/2019/10/09/1570609179378.html
---
**1.安装pyinstaller**
```
pip3 install pyinstaller
```
pyinstaller --onefile hello.py

**2.生成exe**
跳到python文件目录下面运行命令 pyinstaller --onefile python文件名

--onefile的作用是产生的结果汇成一个exe的文件,文件存放再dist目录底下。
```
pyinstaller --onefile hello.py
```

**3.执行exe**
双击即可执行