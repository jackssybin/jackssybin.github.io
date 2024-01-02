title: Linux服务器kdevtmpfsi挖矿病毒解决方法
date: '2020-05-11 11:28:15'
updated: '2020-05-20 23:18:00'
tags: [linux, 矿机病毒, cpu100, kdevtmpfsi]
permalink: /articles/2020/05/11/1589167695782.html
---
![](https://img.hacpai.com/bing/20200514.jpg?imageView2/1/w/960/h/540/interlace/1/q/100) 

## 问题描述
* Linux服务器（包括但不限于CentOS）出现名为kdevtmpfsi的进程，占用高额的CPU、内存资源；
* 并且单纯的kill -9 进程ID 例：kill -9 12345 无法完全杀死，不久便会复活；
* 同2.理杀死 kdevtmpfsi的守护进程kinsing，一小段时间又会出现这对进程；(网上文档有人会有守护进程。我机器没这个，也没在定时任务里找到额外的定时任务)
* 找到并删除这2个进程对应的可执行文件例：find / -name kinsing，一小段时间又会出现。

## 问题根源
1. 服务器安装的redis镜像有问题，被植入kdevtmpfsi挖矿程序。
2. redis未设置密码、或者密码过于简单
3. 服务器被植入定时任务：下载病毒程序、并唤起，及进程存活监测
4. 很纳闷，我的服务器都没有redis，以前短暂安装过。后来就没起来过。也出这个问题了

## 解决方法 (定时任务杀进程，也是守护进程)
* 编写shell脚本 vim /data/shell/kill_kdevtmpfsi.sh；
```
#! /bin/sh
step=1
for (( i = 0; i < 60; i = (i+step) )); do
                date >> /root/data/shell/clear_date_log.txt
                KID=$(ps -ef |grep kdevtmpfsi |grep -w 'kdevtmpfsi'|grep -v 'grep'|awk '{print $2}')
                if [ $KID];then #

                                                              echo "[info]kdevtmpfsiIDΪ:$KID" >> /root/data/shell/clear_date_log.txt
                kill -9 $KID
                rm -f /tmp/kdevtmpfsi
    fi
                sleep $step
done

exit 0
```

* 新增定时任务；  
```
crontab -e 
#新增
*/1 * * * * /data/shell/kill_kdevtmpfsi.sh
```
* 更改redis 默认端口，更改bind 本机端口,不要暴漏在外网。黑客是全网段扫描的。也真是服了
* top 看进程短暂启动。马上被杀掉。也算是解决了

### 另一种 redis配置不规范被入侵。
[https://blog.csdn.net/Dancen/article/details/75313424](https://blog.csdn.net/Dancen/article/details/75313424)


