title: 阿里云ubutun python3.5.2卸载更新到3.6方法亲测有效
date: '2019-11-04 15:10:25'
updated: '2019-11-04 15:10:25'
tags: [python学习]
permalink: /articles/2019/11/04/1572851425831.html
---
### 1.首先卸载一下python3.5的包
```
sudo apt-get remove python3.5
```
### 2.卸载python3.5以及它的依赖包

```
sudo apt-get remove --auto-remove python3.5
```
### 3.手动删除usr/bin 下面的包
如果前两步还不能删除完，自己去usr/bin/下删除python3.5相关的文件

### 4.安装python3.6
```
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:jonathonf/python-3.6 
sudo apt-get update 
sudo apt-get install python3.6
```
### 5.安装python3.6 pip
```
apt-get install python3-pip
python3.6 -m pip install --upgrade pip
```
### 6.安装python3.6 pip
查询安装版本
```
python3 -V
python -V
pip -V
```
