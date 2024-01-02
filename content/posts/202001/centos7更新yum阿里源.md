title: centos7更新yum阿里源
date: '2020-01-03 15:05:32'
updated: '2020-01-03 15:05:32'
tags: [centos7, yum, 阿里云]
permalink: /articles/2020/01/03/1578035132098.html
---
# 1. 备份原来的yum源
```
$sudo cp /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak 
```
# 2.设置aliyun的yum源

```
$sudo wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo 
```
# 3.添加EPEL源

```
$sudo wget -P /etc/yum.repos.d/ http://mirrors.aliyun.com/repo/epel-7.repo
```

# 4.清理缓存，生成新缓存，执行yum更新

```
$sudo yum clean all
$sudo yum makecache
$sudo yum update
```