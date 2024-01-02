title: python3线程池/进程池应用ThreadPoolExecutor
date: '2019-11-19 11:32:01'
updated: '2019-11-19 11:32:01'
tags: [线程, python学习, python实战, 高并发]
permalink: /articles/2019/11/19/1574134321234.html
---
## 多种方法实现 python 线程池
####  一、 既然多线程可以缩短程序运行时间，那么，是不是线程数量越多越好呢？
显然，并不是，每一个线程的从生成到消亡也是需要时间和资源的，太多的线程会占用过多的系统资源（内存开销，cpu开销），而且生成太多的线程时间也是可观的，很可能会得不偿失，这里给出一个最佳线程数量的计算方式：
**最佳线程数的获取：**

1、通过用户慢慢递增来进行性能压测，观察QPS（即每秒的响应请求数，也即是最大吞吐能力。），响应时间

2、根据公式计算:服务器端最佳线程数量=((线程等待时间+线程cpu时间)/线程cpu时间) * cpu数量

3、单用户压测，查看CPU的消耗，然后直接乘以百分比，再进行压测，一般这个值的附近应该就是最佳线程数量。

#### 二、如何实现线程池？
1、使用threadpool模块，这是个python的第三方模块，支持python2和python3
```
#! /usr/bin/env python
# -*- coding: utf-8 -*-

import threadpool
import time

def sayhello (a):
    print("hello: "+a)
    time.sleep(2)

def main():
    global result
    seed=["a","b","c"]
    start=time.time()
    task_pool=threadpool.ThreadPool(5)
    requests=threadpool.makeRequests(sayhello,seed)
    for req in requests:
        task_pool.putRequest(req)
    task_pool.wait()
    end=time.time()
    time_m = end-start
    print("time: "+str(time_m))
    start1=time.time()
    for each in seed:
        sayhello(each)
    end1=time.time()
    print("time1: "+str(end1-start1))

if __name__ == '__main__':
    main()
```
threadpool是一个比较老的模块了，现在虽然还有一些人在用，但已经不再是主流了，关于python多线程，现在已经开始步入未来（future模块）了

2、未来：使用concurrent.futures模块，这个模块是python3中自带的模块
#测试代码
```
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor,wait,as_completed
import time
import urllib.request
URLS = ['http://www.163.com', 'https://www.baidu.com/', 'https://github.com/']
URLS_ten=['http://www.163.com', 'https://www.baidu.com/', 'https://github.com/','http://www.163.com', 'https://www.baidu.com/', 'https://github.com/','http://www.163.com', 'https://www.baidu.com/', 'https://github.com/', 'https://www.baidu.com/']
executorProcessThread = ProcessPoolExecutor(max_workers=3)
executor = ThreadPoolExecutor(max_workers=3)

def load_url(url):
    with urllib.request.urlopen(url, timeout=60) as conn:
        print('%r page is %d bytes' % (url, len(conn.read())))

def testProcessThread():
    for url in URLS:
        future = executorProcessThread.submit(load_url, url)
        print(future.done())


def testThread():#submit 返回无序
    for url in URLS:
        future = executor.submit(load_url, url)
        print(future.done())

def testThreadMap():#按照顺序执行
    executor.map(load_url, URLS)


def testThreadWait():
    f_list = []
    for url in URLS:
        future = executor.submit(load_url, url)
        f_list.append(future)
    # print(wait(f_list))#默认是ALL_COMPLETE 程序会阻塞直到线程池里面的所有任务都完成，再执行主线程
    # print(wait(f_list, return_when='FIRST_COMPLETED')) #FIRST_COMPLETED参数，程序并不会等到线程池里面所有的任务都完成。
    print(wait(f_list, return_when='FIRST_EXCEPTION'))  # FIRST_EXCEPTION参数，程序报错就退出


if __name__ == '__main__': # 要加main
    starttime = time.time()
    #进程模型
    # testProcessThread()
    #线程模型 submit 返回无序
    # testThread()
    #进程模型 map  返回有序
    # testThreadMap()
    #线程返回有序 等待模式
    testThreadWait();
    print('多线程主线程')
    endtime = time.time()
    print(endtime - starttime)
    starttime2 = time.time()
    for url in URLS:
        load_url(url)
    endtime2 = time.time()
    print(endtime2 - starttime2)

``````
