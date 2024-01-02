title: Nginx 虚拟主机配置
date: '2019-10-21 18:02:56'
updated: '2019-10-21 18:04:42'
tags: [nginx]
permalink: /articles/2019/10/21/1571652176584.html
---
![](https://img.hacpai.com/bing/20180630.jpg?imageView2/1/w/960/h/540/interlace/1/q/100) 

## 1.虚拟主机概念

* 所谓虚拟主机，在 Web 服务里就是一个独立的网站站点，这个站点对应独立的域名（也可能是IP 或端口），具有独立的程序及资源，可以独立地对外提供服务供用户访问。
    
* 在 Nginx 中，使用一个 server{} 标签来标识一个虚拟主机，一个 Web 服务里可以有多个虚拟主机标签对，即可以同时支持多个虚拟主机站点。
    
* 虚拟主机有三种类型：基于域名的虚拟主机、基于端口的虚拟主机、基于 IP 的虚拟主机。
## 2.基于域名的虚拟主机

域名的虚拟主机是生产环境中最常用的。

### 2.1 编辑配置文件
```
[root@localhost conf]# vim nginx.conf
worker_processes  1;
events {
    worker_connections  1024;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    server {
        listen       80;
        server_name  www.abc.com;
        location / {
            root   html/www;
            index  index.html index.htm;
        }
    }
   
    server {
        listen       80;
        server_name  bbs.abc.com;
        location / { 
            root   html/bbs;
            index  index.html index.htm;
        }   
    }   

    server {
        listen       80;
        server_name  blog.abc.com;
        location / { 
            root   html/blog;
            index  index.html index.htm;
        }   
    }   
}
```

规范化 Nginx 配置文件，将每个虚拟主机配置成单独的文件，放在统一目录中（如：vhosts）

创建vhosts目录

```
[root@localhost conf]# mkdir -p /usr/local/nginx/conf/vhosts
```

编辑 nginx.conf 主配置文件
```
[root@localhost conf]# vim nginx.conf
worker_processes  1;
events {
    worker_connections  1024;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    include vhosts/*.conf;
}
```

创建每个虚拟主机配置文件：

```
[root@localhost conf]# vim vhosts/www.abc.com.conf
server {
        listen       80;
        server_name  www.abc.com;
        location / {
                root   html/www;
                index  index.html index.htm;
        }
}



[root@localhost conf]# vim vhosts/bbs.abc.com.conf
server {
        listen       80;
        server_name  bbs.abc.com;
        location / {
                root   html/bbs;
                index  index.html index.htm;
        }
}

[root@localhost conf]# vim vhosts/blog.abc.com.conf
server {
        listen       80;
        server_name  blog.abc.com;
        location / {
                root   html/blog;
                index  index.html index.htm;
        }
}
```

### 2.2 创建虚拟主机站点对应的目录和文件
```
[root@localhost html]# cd /usr/local/nginx/html/
[root@localhost html]# for n in www bbs blog
> do
> mkdir ${n}
> echo "http://${n}.abc.com" > ${n}/index.html
> done
```
### 2.3 编辑 /etc/hosts 文件，域名解析

```
echo "127.0.0.1 www.abc.com bbs.abc.com blog.abc.com" >> /etc/hosts

```

### 2.4 重新加载 Nginx 配置

```
[root@localhost conf]# /usr/local/nginx/sbin/nginx -t
[root@localhost conf]# /usr/local/nginx/sbin/nginx -s reload

```

### 2.5 访问测试

```
[root@localhost html]# curl http://www.abc.com
http://www.abc.com
[root@localhost html]# curl http://blog.abc.com
http://blog.abc.com
[root@localhost html]# curl http://bbs.abc.com 
http://bbs.abc.com
```
## 3.基于端口的虚拟主机
基于端口的虚拟主机生产环境不多见，只需要修改主机监听端口就可以了，域名相同也可以，因为基于端口的虚拟主机就是他通过端口来唯一分区不通的虚拟主机的，只要端口不同就是不同的虚拟主机。

### 3.1 编辑配置文件
```
[root@localhost conf]# vim nginx.conf
worker_processes  1;
events {
    worker_connections  1024;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    server {
        listen       80;
        server_name  www.abc.com;
        location / {
            root   html/www;
            index  index.html index.htm;
        }
    }
   
    server {
        listen       81;
        server_name  www.abc.com;
        location / { 
            root   html/bbs;
            index  index.html index.htm;
        }   
    }   

    server {
        listen       82;
        server_name  www.abc.com;
        location / { 
            root   html/blog;
            index  index.html index.htm;
        }   
    }   
}
```

### 3.2 创建虚拟主机站点对应的目录和文件

```
[root@localhost html]# cd /usr/local/nginx/html/
[root@localhost html]# for n in 80 81 82
> do
> mkdir ${n}
> echo "http://www.abc.com:${n}" > ${n}/index.html
> done

```

### 3.3 编辑 /etc/hosts 文件，域名解析

```
echo "127.0.0.1 www.abc.com" >> /etc/hosts

```

### 3.4 重新加载 Nginx 配置

```
[root@localhost conf]# /usr/local/nginx/sbin/nginx -t
[root@localhost conf]# /usr/local/nginx/sbin/nginx -s reload

```

### 3.5 访问测试

```
[root@localhost html]# curl http://www.abc.com:80
http://www.abc.com:80
[root@localhost html]# curl http://www.abc.com:81
http://www.abc.com:81
[root@localhost html]# curl http://www.abc.com:82
http://www.abc.com:82
```

## 4.基于 IP 的虚拟主机

基于 IP 的虚拟主机在生产环境中不常使用，只需要将基于域名的虚拟主机中的域名修改为 IP 就可以了，前提是服务器有多个IP地址。如果需要不同的 IP 对应不同的服务，可在网站前端的负载均衡器上配置。

## 5.虚拟主机别名配置
```
虚拟主机别名，就是为虚拟主机设置除了主域名以外的一个或多个域名名字，这样就能实现用户访问的多个域名对应同一个虚拟主机网站的功能。

[root@localhost conf]# cat vhosts/www.abc.com.conf 
server {
    listen       80;
    server_name  www.abc.com abc.com;   # 这里设置abc.com作为别名
    location / {
        root   html/www;
        index  index.html index.htm;
    }
}
```