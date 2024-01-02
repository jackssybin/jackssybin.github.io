title: centos7开启ssh服务
date: '2019-12-12 22:57:08'
updated: '2019-12-12 22:57:08'
tags: [centos7, sshd, 远程连接]
permalink: /articles/2019/12/12/1576162628044.html
---
开启ssh服务需要root权限，先用root账户登陆

先检查有没有安装ssh服务：
```
rpm -qa | grep ssh
```

如果没有安装ssh服务就安装 ： 
```
yum install openssh-server
```
安装好后在ssh配置文件里进行配置 : 
```
vim /etc/ssh/sshd_config
```
开启ssh服务,这个命令没有回显
```
systemctl start sshd.service
```
开启后用 ps -e | grep sshd 检查一下ssh服务是否开启
netstat -an | grep 22检查一下22端口是否开启
将ssh服务添加到自启动列表中：
```
systemctl enable sshd.service
```