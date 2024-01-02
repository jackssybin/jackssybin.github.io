title: 查看Linux占用内存/CPU最多的进程
date: '2019-11-20 22:43:32'
updated: '2020-01-09 22:58:43'
tags: [调优, linux]
permalink: /articles/2019/11/20/1574261012104.html
---
### 1.可以使用以下命令查使用内存最多的10个进程       
ps -aux | sort -k4nr | head -n 10


### 2.可以使用一下命令查使用CPU最多的10个进程       
ps -aux | sort -k3nr | head -n 10

### 3. 那么多进程中如何查看一个进程的情况
```
ps aux | grep xx 
找到进程号 top -p pid
```
### 4. top显示不全 bw设置宽度
top -c  -bw 500

### 5. 批量杀掉共类进程
```
kill -9 `ps -ef |grep java|grep -v grep|awk '{print $2}'`
```