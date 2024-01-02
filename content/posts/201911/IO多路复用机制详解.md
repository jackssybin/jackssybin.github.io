title: IO多路复用机制详解
date: '2019-11-05 17:06:51'
updated: '2019-11-05 17:07:01'
tags: [java, 高并发, 线程]
permalink: /articles/2019/11/05/1572944811633.html
---
![](https://img.hacpai.com/bing/20171225.jpg?imageView2/1/w/960/h/540/interlace/1/q/100) 

### 服务器端编程经常需要构造高性能的IO模型，常见的IO模型有四种：

> 一. 同步阻塞IO（Blocking IO）：即传统的IO模型。

>二. 同步非阻塞IO（Non-blocking IO）：默认创建的socket都是阻塞的，非阻塞IO要求socket被设置为NONBLOCK。注意这里所说的NIO并非Java的NIO（New IO）库。

>三. IO多路复用（IO Multiplexing）：即经典的Reactor设计模式，有时也称为异步阻塞IO，Java中的Selector和Linux中的epoll都是这种模型。

>四.  异步IO（Asynchronous IO）：即经典的Proactor设计模式，也称为异步非阻塞IO。

**同步和异步**的概念描述的是用户线程与内核的交互方式：
**同步**是指用户线程发起IO请求后需要等待或者轮询内核IO操作完成后才能继续执行；
**异步**是指用户线程发起IO请求后仍继续执行，当内核IO操作完成后会通知用户线程，或者调用用户线程注册的回调函数。

**阻塞和非阻塞**的概念描述的是用户线程调用内核IO操作的方式：
**阻塞**是指IO操作需要彻底完成后才返回到用户空间；
**非阻塞**是指IO操作被调用后立即返回给用户一个状态值，无需等到IO操作彻底完成。

##### 一、同步阻塞IO
同步阻塞IO模型是最简单的IO模型，用户线程在内核进行IO操作时被阻塞
![](http://images.cnitblog.com/blog/405877/201411/142330286789443.png)
用户线程通过系统调用read发起IO读操作，由用户空间转到内核空间。内核等到数据包到达后，然后将接收的数据拷贝到用户空间，完成read操作.
用户需要等待read将socket中的数据读取到buffer后，才继续处理接收的数据。整个IO请求的过程中，用户线程是被阻塞的，这导致用户在发起IO请求时，不能做任何事情，对CPU的资源利用率不够.
##### 二、同步非阻塞IO
同步非阻塞IO是在同步阻塞IO的基础上，将socket设置为NONBLOCK。这样做用户线程可以在发起IO请求后可以立即返回
![](http://images.cnitblog.com/blog/405877/201411/142332004602984.png)
```
{
    read(socket, buffer);
    process(buffer);
}
```
由于socket是非阻塞的方式，因此用户线程发起IO请求时立即返回。但并未读取到任何数据，用户线程需要不断地发起IO请求，直到数据到达后，才真正读取到数据，继续执行。

用户线程使用同步非阻塞IO模型的伪代码描述为：
```
{
    while(read(socket, buffer) != SUCCESS)
        ;
    process(buffer);
}
```
用户需要不断地调用read，尝试读取socket中的数据，直到读取成功后，才继续处理接收的数据。整个IO请求的过程中，虽然用户线程每次发起IO请求后可以立即返回，但是为了等到数据，仍需要不断地轮询、重复请求，消耗了大量的CPU的资源。一般很少直接使用这种模型，而是在其他IO模型中使用非阻塞IO这一特性。

##### 三、IO多路复用
IO多路复用模型是建立在内核提供的多路分离函数select基础之上的，使用select函数可以避免同步非阻塞IO模型中轮询等待的问题。
![](http://images.cnitblog.com/blog/405877/201411/142332187256396.png)
用户首先将需要进行IO操作的socket添加到select中，然后阻塞等待select系统调用返回。当数据到达时，socket被激活，select函数返回。用户线程正式发起read请求，读取数据并继续执行。

从流程上来看，使用select函数进行IO请求和同步阻塞模型没有太大的区别，甚至还多了添加监视socket，以及调用select函数的额外操作，效率更差。但是，使用select以后最大的优势是用户可以在一个线程内同时处理多个socket的IO请求。用户可以注册多个socket，然后不断地调用select读取被激活的socket，即**可达到在同一个线程内同时处理多个IO请求的目的**。而在同步阻塞模型中，必须通过多线程的方式才能达到这个目的。

用户线程使用select函数的伪代码描述为：
```
{
    select(socket);
    while(1) 
    {
        sockets = select();
        for(socket in sockets) 
        {
            if(can_read(socket)) 
            {
                read(socket, buffer);
                process(buffer);
            }
        }
    }
}
```
其中while循环前将socket添加到select监视中，然后在while内一直调用select获取被激活的socket，一旦socket可读，便调用read函数将socket中的数据读取出来。 
然而，使用select函数的优点并不仅限于此。虽然上述方式允许单线程内处理多个IO请求，但是每个IO请求的过程还是阻塞的（在select函数上阻塞），平均时间甚至比同步阻塞IO模型还要长。如果用户线程只注册自己感兴趣的socket或者IO请求，然后去做自己的事情，等到数据到来时再进行处理，则可以提高CPU的利用率。

##### 四、异步IO
![](http://images.cnitblog.com/blog/405877/201411/142333511475767.png)

#####  I/O多路复用
***重要的事情再说一遍： I/O multiplexing 这里面的 multiplexing 指的其实是在单个线程通过记录跟踪每一个Sock(I/O流)的状态(对应空管塔里面的Fight progress strip槽)来同时管理多个I/O流**. 发明它的原因，是尽量多的提高服务器的吞吐能力。  
  
是不是听起来好拗口，看个图就懂了.*

*![](https://img-blog.csdn.net/20150808203829641?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  
在同一个线程里面， 通过拨开关的方式，来同时传输多个I/O流， (学过EE的人现在可以站出来义正严辞说这个叫“时分复用”了）。  
  
*什么，你还没有搞懂“一个请求到来了，nginx使用epoll接收请求的过程是怎样的”， 多看看这个图就了解了。提醒下，ngnix会有很多链接进来， epoll会把他们都监视起来，然后像拨开关一样，谁有数据就拨向谁，然后调用相应的代码处理。**

*了解这个基本的概念以后，其他的就很好解释了。  
  
**select, poll, epoll 都是I/O多路复用的具体的实现，之所以有这三个鬼存在，其实是他们出现是有先后顺序的。***
I/O多路复用这个概念被提出来以后， select是第一个实现 (1983 左右在BSD里面实现的)。  
  
select 被实现以后，很快就暴露出了很多问题。  
*

* select 会修改传入的参数数组，这个对于一个需要调用很多次的函数，是非常不友好的。  
    
* select 如果任何一个sock(I/O stream)出现了数据，select 仅仅会返回，但是并不会告诉你是那个sock上有数据，于是你只能自己一个一个的找，10几个sock可能还好，要是几万的sock每次都找一遍，这个无谓的开销就颇有海天盛筵的豪气了。  
    
* select 只能监视1024个链接， 这个跟草榴没啥关系哦，linux 定义在头文件中的，参见*FD_SETSIZE。*
* select 不是线程安全的，如果你把一个sock加入到select, 然后突然另外一个线程发现，尼玛，这个sock不用，要收回。对不起，这个select 不支持的，如果你丧心病狂的竟然关掉这个sock, select的标准行为是。。呃。。不可预测的， 这个可是写在文档中的哦.

于是14年以后(1997年）一帮人又实现了poll, poll 修复了select的很多问题，比如  

* poll 去掉了1024个链接的限制，于是要多少链接呢， 主人你开心就好。  
    
* poll 从设计上来说，不再修改传入数组，不过这个要看你的平台了，所以行走江湖，还是小心为妙。

**其实拖14年那么久也不是效率问题， 而是那个时代的硬件实在太弱，一台服务器处理1千多个链接简直就是神一样的存在了，select很长段时间已经满足需求。**  
  
但是poll仍然不是线程安全的， 这就意味着，不管服务器有多强悍，你也只能在一个线程里面处理一组I/O流。你当然可以那多进程来配合了，不过然后你就有了多进程的各种问题。  
  
于是5年以后, 在2002, 大神 Davide Libenzi 实现了epoll.  
  
epoll 可以说是I/O 多路复用最新的一个实现，epoll 修复了poll 和select绝大部分问题, 比如：  

* epoll 现在是线程安全的。  
    
* epoll 现在不仅告诉你sock组里面数据，还会告诉你具体哪个sock有数据，你不用自己去找了。
epoll 当年的patch，现在还在，下面链接可以看得到：
[/dev/epoll Home Page](http://www.xmailserver.org/linux-patches/nio-improve.html)
![](https://img-blog.csdn.net/20150808203809771?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)
**横轴Dead connections 就是链接数的意思，叫这个名字只是它的测试工具叫deadcon. 纵轴是每秒处理请求的数量，你可以看到，epoll每秒处理请求的数量基本不会随着链接变多而下降的。poll 和/dev/poll 就很惨了。*  
  
可是epoll 有个致命的缺点。。只有linux支持。比如BSD上面对应的实现是kqueue。*