title: centos7下安装redis
date: '2019-11-23 17:37:02'
updated: '2019-11-27 15:38:30'
tags: [redis, centos, linux服务配置安装]
permalink: /articles/2019/11/23/1574501821804.html
---
## 一、安装redis
### 第一步：下载redis安装包

```
wget http://download.redis.io/releases/redis-4.0.6.tar.gz
```

### 第二步：解压压缩包

```
tar -zxvf redis-4.0.6.tar.gz
```
### 第三步：yum安装gcc依赖

```
yum install gcc
```
### 第四步：跳转到redis解压目录下  and 编译安装

```
cd redis-4.0.6
make MALLOC=libc
cd src && make install
```
## 二、启动redis的三种方式
先切换到redis src目录下 
```
 cd src
```
### 1、直接启动redis
```
./redis-server
```
redis启动成功，但是这种启动方式需要一直打开窗口，不能进行其他操作，不太方便。
按 ctrl + c可以关闭窗口。
### 2、以后台进程方式启动redis
第一步：修改redis.conf文件
将
```
daemonize no
```
修改为
```
daemonize yes
```
第二步：指定redis.conf文件启动
```
./redis-server /usr/local/redis-4.0.6/redis.conf
```
第三步：关闭redis进程

首先使用ps -aux | grep redis查看redis进程
```
ps -aux | grep redis
kill -9 pid
```
### 3、设置redis开机自启动
1、在/etc目录下新建redis目录

```
mkdir /etc/redis
```
2、将/usr/local/redis-4.0.6/redis.conf 文件复制一份到/etc/redis目录下，并命名为6379.conf
```
 cp /usr/local/redis-4.0.6/redis.conf /etc/redis/6379.conf
```
该文件会作为开机启动的配置文件，修改配置的时候需要修改该文件
3、将redis的启动脚本复制一份放到/etc/init.d目录下
```
cp /usr/local/redis-4.0.6/utils/redis_init_script /etc/init.d/redisd
```
/etc/init.d/redisd 文件才是真正启动文件
4、设置redis开机自启动

先切换到/etc/init.d目录下

然后执行自启命令
```
chkconfig redisd on
#service redisd does not support chkconfig　
```

看结果是redisd不支持chkconfig

解决方法：

使用vim编辑redisd文件，在第一行加入如下两行注释，保存退出
```
# chkconfig:   2345 90 10
# description:  Redis is a persistent key-value database
```
注释的意思是，redis服务必须在运行级2，3，4，5下被启动或关闭，启动的优先级是90，关闭的优先级是10。
再次执行开机自启命令，成功
```
chkconfig redisd on
```
现在可以直接已服务的形式启动和关闭redis了
```
service redisd start
service redisd stop
或是redis-cli SHUTDOWN 也可以关闭
再或者就直接杀掉该进程
```
5、设置redis支持远程访问
(1).开启阿里云 安全组配置，将端口暴漏出去。
(2).将redis.conf 里的redis.conf bind127.0.0.1 这一行注释掉，任意IP都可以访问；
找到 protected-mode yes 改为 protected-mode no；保存之后重启redis
6、命令行客户端执行
```
redis-cli -h 127.0.0.1 -p 6379
```