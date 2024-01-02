title: centos7安装nginx,jdk,maven(yum方式)
date: '2019-12-16 17:52:56'
updated: '2019-12-17 15:49:11'
tags: [centos7, centos, nginx, yum]
permalink: /articles/2019/12/16/1576489975924.html
---
### 1.添加Nginx 的yum源
```
rpm -Uvh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm  

#查看源是否添加成功 yum search nginx
```

### 2、安装Nginx

```
yum install -y nginx
```
### 3.启动Nginx并设置开机自动运行

```
systemctl start nginx.service 
systemctl enable nginx.service
```
### 4.路径信息
以下是Nginx的默认路径：

(1) Nginx配置路径：/etc/nginx/
(2) PID目录：/var/run/nginx.pid
(3) 错误日志：/var/log/nginx/error.log
(4) 访问日志：/var/log/nginx/access.log
(5) 默认站点目录：/usr/share/nginx/html
事实上，只需知道Nginx配置路径，其他路径均可在/etc/nginx/nginx.conf 以及/etc/nginx/conf.d/default.conf 中查询到。

### 5.yum安装jdk
```
yum -y install java-1.8.0-openjdk
```

### 6.yum安装maven
下载maven安装包资源：

```
wget http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo

```
安装maven：

```
yum -y install apache-maven
```

验证是否安装成功：

```
mav –v
```