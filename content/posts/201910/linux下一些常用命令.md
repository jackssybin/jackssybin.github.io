title: linux下一些常用命令
date: '2019-10-25 11:22:58'
updated: '2019-10-25 17:05:48'
tags: [linux]
permalink: /articles/2019/10/25/1571973778513.html
---
1.根据端口查进程
```
lsof -i:port  
netstat -nap | grep port
```
2.根据进程号查端口:
```
lsof -i|grep pid  
netstat -nap | grep pid
```
3.根据进程名查找pid、port：
```
ps -ef |grep tomcat  
ps -ef |grep port(根据port查找相关进程)  
ps -ef |grep pid(根据pid查找相关进程)
```
4.根据进程号查服务路径：
```
ll /proc/26357/cwd    #26357是进程号
1 root root 0 Oct 25 10:08 /proc/26357/cwd -> /root/data/proxy_pool/Api/
```
5.查询所有进程号 top
```
top
```
6.查看进程中的线程号信息
```
ps -T -p 18043   # ps 语法

1.top -H -p 18043  #top 实时的哈
shift+H开启show threads on功能，展示线程资源占用情况  
　　找到消耗CPU等最多的PID为:18045
2.  printf "%x\n" 18045  -->467d
3. jstack 18043|grep 467d  #(定位到线程)
>>"VM Thread" os_prio=0 tid=0x00007f36e406f800 nid=0x467d runnable 

```
转载评论里[https://hacpai.com/member/fenglidac](https://hacpai.com/member/fenglidac) 的精髓图片
![null](https://img.hacpai.com/file/2019/10/599b9b3ca5bb7-ee5d7502.png?imageView2/2/w/1280/format/jpg/interlace/1/q/100)