title: Centos7安装Python3.7
date: '2019-11-30 12:42:18'
updated: '2019-11-30 12:42:18'
tags: [python学习, centos7, python3]
permalink: /articles/2019/11/30/1575088937927.html
---
## 1.安装编译相关工具

```
yum -y groupinstall "Development tools"
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
yum install libffi-devel -y
```
## 2.下载安装包解压

```
cd #回到用户目录
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
tar -xvJf  Python-3.7.0.tar.xz
```
## 3.编译安装

```
mkdir /usr/local/python3 #创建编译安装目录
cd Python-3.7.0
./configure --prefix=/usr/local/python3
make && make install
```

## 4.创建软连接

```
ln -s /usr/local/python3/bin/python3 /usr/local/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip3
```

## 5.验证是否成功

```
python3 -V
pip3 -V
```

现在就可以愉快的玩耍了