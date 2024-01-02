title: HAProxy常见的安装方式
date: '2020-08-28 20:01:24'
updated: '2020-08-28 20:01:24'
tags: [haproxy, nginx, 负载, 动态代理]
permalink: /articles/2020/08/28/1598616084150.html
---

**1>.什么是负载均衡**
```
　负载均衡(Load Balance，简称LB)是一种服务或基于硬件设备等实现的高可用反向代理技术，负载均衡将特定的业务(web服务、网络流量等)分担给指定的一个或多个后端特定的服务器或设备，从而提高了公司业务的并发处理能力、保证了业务的高可用性、方便了业务后期的水平动态扩展。

　　博主推荐阅读:
　　　　https://yq.aliyun.com/articles/1803
```

**2>.为什么使用负载均衡**
```
Web服务器的动态水平扩展
　　　　对用户无感知
　　增加业务并发访问及处理能力
　　　　解决单服务器瓶颈问题(单点故障)
　　节约公网IP地址
　　　　降低IT支出成本
　　隐藏内部服务器IP
　　　　提高内部服务器安全性
　　配置简单
　　　　固定格式的配置文件
　　功能丰富
　　　　支持四层和七层，支持动态下线主机
　　性能较强
　　　　并发数万甚至数十万
```
**3>.常见有哪些负载均衡**
```
软件负载(一般选择开源软件)：
　　四层(可以和硬件防火墙相抗衡的性能)：
　　　　LVS(Linux Virtual Server，生产环境中大多使用DR模式性能要比HAProxy强)
　　　　HAProxy(High Availability Proxy，一般中小型公司使用HAproxy基本上够用了)
　　　　Nginx(需要1.9版本以上才支持)
　　　　……
　　七层：
　　　　HAProxy(和Nginx一样，都支持基于四层和七层的负载均衡)
　　　　Nginx(生产环境中小型企业一般使用HAProxy做四层的负载均衡，使用Nginx做七层的负载均衡)
　　　　……

硬件负载(需要花钱)：
　　F5
　　Netscaler
```
**4>.典型的负载均衡应用场景**
```
　四层(传输层，一般基于监听本地端口实现负载均衡)：
　　　　Redis
　　　　Mysql
　　　　RabbitMQ
　　　　Memcache
　　　　......


　　七层(应用层,直接反向代理到后端服务器)：
　　　　Nginx
　　　　Tomcat
　　　　Apache
　　　　PHP
　　　　图片
　　　　动静分离
　　　　API
```


 

**二.HaProxy概述**

**1>.什么是HAProxy**
```
HAProxy是法国开发者Willy Tarreau开发的一个开源软件，是一款具备高并发、高性能的TCP和HTTP负载均衡器，支持基于cookie的持久性，自动故障切换，支持正则表达式及web状态统计。

　　官网:
　　　　http://www.haproxy.org
　　　　https://www.haproxy.com

　　博主推荐阅读:
　　　　https://cbonte.github.io/haproxy-dconv/
```
**2>.调度器集群(Load Balance Cluster,简称LB Cluster)**
```
四层：
　　　　lvs
　　　　nginx(stream模式且nginx1.9.0或更新版本)
　　　　haproxy(mode tcp)

　　七层：
　　　　http协议:
　　　　　　nginx(http), haproxy(mode http), httpd...


　　关于四层和七层的区别，博主推荐阅读:
　　　　https://www.cnblogs.com/yinzhengjie/p/12127959.html
```
**3>.HAProxy功能**
```
　HAProxy是TCP/ HTTP反向代理服务器(不支持反向代理)，尤其适合于高可用性(需要依赖于keepalive软件)高并发环境
　　　　可以针对HTTP请求添加cookie，进行路由后端服务器
　　　　可平衡负载至后端服务器，并支持持久连接(可以基于用户的源地址进行hash)
　　　　支持基于cookie进行调度
　　　　支持所有主服务器故障切换至备用服务器
　　　　支持专用端口实现监控服务
　　　　支持不影响现有连接情况下停止接受新连接请求
　　　　可以在双向添加，修改或删除HTTP报文首部
　　　　支持基于pattern实现连接请求的访问控制
　　　　通过特定的URI为授权用户提供详细的状态信息

　　历史版本更新功能：1.4 1.5 1.6 1.7 1.8 1.9 2.0-dev
　　　　1.8：多线程，HTTP/2缓存……(生产环境中推荐使用该版本)
　　　　1.7：服务器动态配置，多类型证书……
　　　　1.6：DNS解析支持，HTTP连接多路复用……
　　　　1.5：开始支持SSL，IPV6，keepalived……(CentOS 7.6的yum仓库默认支持的版本，生产环境中并不推荐使用)
```
**三.yum安装HAProxy**
**1>.CentOS安装HAProxy(温馨提示:较新haproxy1.8版本中，比如动态禁用后端服务器，日志管理等功能支持的并没有haproxy1.5系列要友好)**
```
`yum list haproxy`
` yum -y install haproxy`
`haproxy -v　　　　`
`systemctl start haproxy`
`ss -ntl`
`ps -ef | grep haproxy | grep -v grep`
```
**2>.**Ubantu安装HAProxy****
```
` apt-get install haproxy`
```

**程序环境**
```
主程序：
　　　　/usr/sbin/haproxy

　　配置文件：
　　　　/etc/haproxy/haproxy.cfg

　　Unit file：
　　　　/usr/lib/systemd/system/haproxy.service
```

**配置文件的配置段说明**

```
global(全局配置段):
　　　　进程及安全配置相关的参数
　　　　性能调整相关参数
　　　　Debug参数

　　proxies(代理配置段):
　　　　defaults：
　　　　　　为frontend, backend, listen提供默认配置
　　　　frontend：
　　　　　　前端，相当于nginx中的server {}
　　　　backend：
　　　　　　后端，相当于nginx中的upstream {}
　　　　listen：
　　　　　　同时拥有前端和后端配置
```
**HAProxy的global配置参数**
```
chroot
　　　　锁定运行目录

　　deamon
　　　　以守护进程运行

　　stats socket /var/lib/haproxy/haproxy.sockmode 600 level admin 
　　　　指定socket文件路径。

　　user, group, uid, gid
　　　　运行haproxy的用户身份，一般使用id为99的nobody用户即可(说白了生产环境中haproxy一般并不用于web服务器，而是作为代理服务器，因此使用一个无权限登录操作系统的用户即可。)
　　　　具体案例可参考:https://www.cnblogs.com/yinzhengjie/p/12117113.html

　　nbproc
　　　　开启的haproxy进程数，与CPU保持一致

　　nbthread
　　　　指定每个haproxy进程开启的线程数，默认为每个进程只开启一个线程。
　　　　具体案例可参考:https://www.cnblogs.com/yinzhengjie/p/12121468.html

　　cpu-map 
　　　　绑定haproxy进程至指定CPU，比如"cpu-map 1 0"表示将haproxy的第"1"个进程绑定到编号为"0"的CPU上(注意，cpu的核心编号是从0开始的)，而"CPU-map 2 1"则表示将haproxy的第"2"个进程绑定到编号为"1"的CPU上。

　　maxconn
　　　　每个haproxy进程的最大并发连接数

　　maxsslconn
　　　　SSL每个haproxy进程ssl最大连接数

　　maxconnrate
　　　　每个进程每秒最大连接数

　　spread-checks 
　　　　后端server状态check随机提前或延迟检测后端服务器的百分比时间，默认为0，即不延迟也不提前。该参数一般情况下(后端服务器在10台以内)并不需要配置,如果后端服务器数量已经有成百上千的节点，建议2-5(即"20%-50%")之间,比如检测后端服务器的间隔事件是10秒，则延迟或时间为2s-5s之间。 

　　pidfile
　　　　指定pid文件路径,该值最好和启动脚本的pid文件路径指定的要一致，否则指定的pid文件并不生效而是以启动脚本("/usr/lib/systemd/system/haproxy.service")指定的pid文件为准。

　　log 127.0.0.1 local3 info 
　　　　定义全局的syslog服务器；最多可以定义两个。
　　　　具体案例可参考:https://www.cnblogs.com/yinzhengjie/p/12122239.html


　　博主推荐阅读:
　　　　https://cbonte.github.io/haproxy-dconv/1.8/configuration.html#3
```

****HAProxy的Proxies配置参数****
```
　defaults [<name>] 
　　　　默认配置项，针对以下的frontend、backend和lsiten生效，可以多个name。  
　　　　defaults常用的配置参数:
            option redispatch
                当server Id对应的服务器挂掉后，强制定向到其他健康的服务器,生产环境推荐添加该参数进行调优。
            option abortonclose 
                当服务器负载很高的时候，自动结束掉当前队列处理比较久的链接，生产环境推荐添加该参数进行调优。
            option http-keep-alive 
                开启会话保持,如"option http-keep-alive 60"则表示会话保持时间为60s。
            option forwardfor 
                开启IP透传，无法自定义"forwardfor"这个变量，而在nginx中式可以自定义的，生产环境中推荐添加该擦承诺书进行调优。
            mode  
                指定默认工作类型，比如"mode http"表示默认基于http协议工作，"mode tcp"则表示默认基于tcp协议工作。
            timeout connect 
                转发客户端请求到后端server的最长连接时间(TCP之前),如"timeout connect 60s"则表示客户端请求到haproxy服务器之后，由haproxy将请求转发到后端服务器，若超过60s(即1分钟)后端服务器依旧没有响应客户端则超时（说白了就是客户端和后端服务器建立连接的超时时间）。
            timeout server 
                转发客户端请求到后端服务端的超时超时时长(TCP之后),如"timeout server 600s"则表示客户端请求到haproxy服务器之后，由haproxy将请求转发到后端的服务器，若后端服务器(比如数据库查询操作)在600s(10分钟)内依旧没有响应则超时（说白了就是客户端已经和后端服务器建立连接后，定义执行查询或写入操作的超时时间）。
            timeout client 600s  
                与客户端的最长空闲时间，表示客户端和服务器端已经建立连接，若在指定的规定的时间内发起了新的请求则无需重新建立连接，直接使用上一次的连接即可。
            timeout http-keep-alive 120s 
                session会话保持超时时间，范围内会转发到相同的后端服务器。
            timeout check 5s 
                对后端服务器的检测超时时间。

　　frontend <name> 前端servername，类似于Nginx的一个虚拟主机server。
            bind：
                指定HAProxy的监听地址，可以是IPV4或IPV6，可以同时监听多个IP或端口，可同时用于listen字段中
                语法为:"bind [<address>]:<port_range> [, ...] [param*]",如"bind 172.30.1.102:80,172.30.1.102:8080,172.30.1.102:8081"
            mode http/tcp 
                指定负载协议类型
            use_backend backend_name 
                调用的后端服务器组名称(即使用backend关键字定义的后端服务器组)

　　backend <name> 后端服务器组，等于nginx的upstream
        mode http/tcp 
            指定负载协议类型
        option
            配置选项,option后面加httpchk，smtpchk, mysql-check, pgsql-check，ssl-hello-chk方法，可用于实现更多应用层检测功能。
        server 
　　　　　　　　定义后端realserver
　　　　　　　　后端服务器状态监测及相关配置如下所示:
　　　　　　　　　　check 
　　　　　　　　　　　　对指定real进行健康状态检查，默认不开启
　　　　　　　　　　addr IP
　　　　　　　　　　　　可指定的健康状态监测IP
　　　　　　　　　　port num
　　　　　　　　　　　　指定的健康状态监测端口,比如LA/NMP架构中，咱们可以指定检测PHP的9000端口。
　　　　　　　　　　inter num
　　　　　　　　　　　　健康状态检查间隔时间，默认2000 ms
　　　　　　　　　　fall num
　　　　　　　　　　　　后端服务器失效检查次数，默认为3
　　　　　　　　　　rise num
　　　　　　　　　　　　后端服务器从下线恢复检查次数，默认为2
　　　　　　　　　　weight 
　　　　　　　　　　　　默认为1，最大值为256，0表示不参与负载均衡
　　　　　　　　　　backup
　　　　　　　　　　　　将后端服务器标记为备份状态，即当其它可用节点都挂掉后该节点才会被启用。
　　　　　　　　　　disabled
　　　　　　　　　　　　将后端服务器标记为不可用状态，即手动将某个后台节点下线。
　　　　　　　　　　redirect prefix http://node101.yinzhengjie.org.cn 
将请求临时重定向至其它URL，只适用于http模式
　　　　　　　　　　maxconn <maxconn> 当前后端server的最大并发连接数，若并发数没有超过规定的最大值时则当前节点响应用户请求(说白了就是未达到最大并发连接数时所有用户请求的连接数它一个节点来处理)，若超过则需要其它节点来一起响应用户请求(说白了就是达到最大并发连接数时它和别的节点一起来处理用户请求的连接数)。
　　　　　　　　　　backlog <backlog> 当server的连接数达到上限后的后援队列长度
　　listen <name> 将frontend和backend合并在一起配置。  
　　　　可参考案例:https://www.cnblogs.com/yinzhengjie/p/12114195.html  
  

　　温馨提示:
　　　　以上的name字段只能使用"-","_",".",和":"进行分割字符，并且严格区分大小写，例如："Web_80"和"web_80"是完全不同的两组服务器。
　　
　　博主推荐阅读:
　　　　https://cbonte.github.io/haproxy-dconv/1.8/configuration.html#4
```

haproxy配置
```
cat /etc/haproxy/haproxy.cfg 
global
maxconn 100000
chroot /yinzhengjie/softwares/haproxy
#stats socket /var/lib/haproxy/haproxy.sock mode 600 level admin
user haproxy
group haproxy
daemon
nbproc 4
cpu-map 1 0
cpu-map 2 1
cpu-map 3 2
cpu-map 4 3
nbthread 2
pidfile /yinzhengjie/softwares/haproxy/haproxy.pid
log 127.0.0.1 local5 info

defaults
option http-keep-alive
option  forwardfor
option redispatch
option abortonclose
maxconn 100000
mode http
timeout connect 300000ms
timeout client  300000ms
timeout server  300000ms

listen stats
 mode http
 bind 0.0.0.0:9999
 stats enable
 log global
 stats uri     /haproxy-status
 stats auth    admin:admin

#官网80端口访问入口
listen WEB_PORT_81
    bind 0.0.0.0:81
    mode http
    server web01 59.110.240.154:80 check inter 3000 fall 3 rise 5

#官网443端口访问入口
listen WEB_PORT_443
    bind 0.0.0.0:443
    mode tcp
    server web01 59.110.240.154:443 check inter 3s fall 3 rise 5

systemctl restart haproxy
ss -ntl

```
