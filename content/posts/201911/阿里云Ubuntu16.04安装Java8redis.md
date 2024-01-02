title: 阿里云Ubuntu16.04安装Java8_redis
date: '2019-11-11 16:23:51'
updated: '2019-11-14 11:52:19'
tags: [java]
permalink: /articles/2019/11/11/1573460631525.html
---
### 一、java8安装
##### 1 Java 8 下载地址
链接：https://pan.baidu.com/s/1NN4XBL5g1Xn7EwzM4YET0g 
提取码：m4mq 
##### 2 以root用户登录将下载的jdk-8u92-linux-x64.tar.gz文件放到~/data/soft/目录下，使用如下命令解压

```

tar zxvf jdk-8u92-linux-x64.tar.gz -C ~/data/soft


```
##### 3 将java目录添加到etc/profile文件中
```
export JAVA_HOME=/root/data/jdk1.8
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
```
##### 4 验证java
```
java -version
```
### 二、redis安装
# 安装Redis服务器端
```
sudo apt-get install redis-server
```
安装完成后，Redis服务器会自动启动，我们检查Redis服务器程序

## 检查Redis服务器系统进程
```
redis     9839  0.0  0.1  40136  3096 ?        Ssl  11:42   0:00 /usr/bin/redis-server 127.0.0.1:6379
root     10139  0.0  0.0  14228   912 pts/1    S+   11:42   0:00 grep --color=auto redis
```
## 通过启动命令检查Redis服务器状态
```
netstat -nlt|grep 6379
tcp        0      0 127.0.0.1:6379          0.0.0.0:*               LISTEN
```
## 通过启动命令检查Redis服务器状态
```
root@iZ2ze8um4r4f2fiahuutedZ:~/data/collectMovies# sudo /etc/init.d/redis-server status
● redis-server.service - Advanced key-value store
   Loaded: loaded (/lib/systemd/system/redis-server.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2019-11-14 11:42:19 CST; 2min 3s ago
     Docs: http://redis.io/documentation,
           man:redis-server(1)
 Main PID: 9839 (redis-server)
    Tasks: 3
   Memory: 836.0K
      CPU: 82ms
   CGroup: /system.slice/redis-server.service
           └─9839 /usr/bin/redis-server 127.0.0.1:6379

Nov 14 11:42:19 iZ2ze8um4r4f2fiahuutedZ systemd[1]: Starting Advanced key-value store...
Nov 14 11:42:19 iZ2ze8um4r4f2fiahuutedZ run-parts[9829]: run-parts: executing /etc/redis/redis-server.pre-up.d/00_example
Nov 14 11:42:19 iZ2ze8um4r4f2fiahuutedZ run-parts[9840]: run-parts: executing /etc/redis/redis-server.post-up.d/00_example
Nov 14 11:42:19 iZ2ze8um4r4f2fiahuutedZ systemd[1]: Started Advanced key-value store.
```
# 通过命令行客户端访问Redis
安装Redis服务器，会自动地一起安装Redis命令行客户端程序。
在本机输入redis-cli命令就可以启动，客户端程序访问Redis服务器。
```
~ redis-cli
redis 127.0.0.1:6379>

# 命令行的帮助

redis 127.0.0.1:6379> help
redis-cli 2.2.12
Type: "help @" to get a list of commands in 
      "help " for help on 
      "help " to get a list of possible help topics
      "quit" to exit


# 查看所有的key列表

redis 127.0.0.1:6379> keys *
(empty list or set)
```
# 修改Redis的配置
## 使用Redis的访问账号

默认情况下，访问Redis服务器是不需要密码的，为了增加安全性我们需要设置Redis服务器的访问密码。设置访问密码为redisredis。

用vi打开Redis服务器的配置文件redis.conf
```
sudo vi /etc/redis/redis.conf

#取消注释requirepass
requirepass redisredis
```
## 让Redis服务器被远程访问

默认情况下，Redis服务器不允许远程访问，只允许本机访问，所以我们需要设置打开远程访问的功能。
用vi打开Redis服务器的配置文件redis.conf
```
sudo vi /etc/redis/redis.conf

#注释bind
#bind 127.0.0.1
```
修改后，重启Redis服务器。
```
sudo /etc/init.d/redis-server restart
Stopping redis-server: redis-server.
Starting redis-server: redis-server.
```
我们在远程的另一台Linux访问Redis服务器
```
redis-cli -a redisredis -h 192.168.1.199

redis 192.168.1.199:6379> keys *
1) "key2"
2) "key3"
```