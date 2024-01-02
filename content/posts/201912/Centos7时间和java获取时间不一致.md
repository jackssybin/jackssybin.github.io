title: Centos7时间和java获取时间不一致
date: '2019-12-24 23:18:44'
updated: '2019-12-24 23:18:44'
tags: [centos7, jvm, json时间转换, java]
permalink: /articles/2019/12/24/1577200724607.html
---
## 问题描述
遇到一个问题，web显示的时间比服务器时间快12小时。Tomcat和MySQL安装在同一台服务器，系统是centos7，且服务器时间和MySQL时间一致，均是当前北京时间。

## 解决思路
1、在程序中使用java的函数设定时区。
2、在启动java程序时加参数-Duser.timezone=GMT+8
3、修改/etc/sysconfig/clock文件，然后重启服务。 （PS：jre是从/etc/sysconfig/clock这个文件中获取时区信息的）

附/etc/sysconfig/clock文件内容：
```
#设置上海时区
ZONE="Asia/Shanghai"
UTC=false
ARC=false
## ZONE -- 时区
## UTC -- 表明时钟设置为UTC。
## ARC -- 仅用于alpha表明使用ARC。
```
4、修改MySQL连接参数
```
jdbc:mysql://localhost:3306/test?useUnicode=true&characterEncoding=UTF-8&useOldAliasMetadataBehavior=true&autoReconnect=true&serverTimezone=UTC
```
自此终于能看到正常的时间了