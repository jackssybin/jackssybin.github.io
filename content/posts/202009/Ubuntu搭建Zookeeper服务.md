title: Ubuntu 搭建Zookeeper服务
date: '2020-09-10 13:58:21'
updated: '2020-09-10 14:07:47'
tags: [zookeeper, zk, centos, linux]
permalink: /articles/2020/09/10/1599717501006.html
---
![](https://b3logfile.com/bing/20190620.jpg?imageView2/1/w/960/h/540/interlace/1/q/100) 

### 1、下载安装包

官方下载地址[http://apache.fayea.com/zookeeper/](http://apache.fayea.com/zookeeper/)

### 2、安装

安装前确保系统已安装过JDK，[JDK安装过程可参照](https://www.cnblogs.com/kingsonfu/p/9801556.html)

2.1 解压下载好的tar.gz安装包到某个目录下，可使用命令：

```
tar -zxvf zookeeper-3.5.4-beta.tar.gz
```

2.2 进入解压目录的conf目录，复制配置文件zoo_sample.cfg并命名为zoo.cfg，相关命令为：

```
cp zoo_sample.cfg zoo.cfg
```

2.3 编辑zoo.cfg文件

```
vi zoo.cfg
```

主要修改如下：

```
# 增加dataDir和dataLogDir目录，目录自己创建并指定，用作数据存储目录和日志文件目录
dataDir=/home/local/zk/data
dataLogDir=/home/local/zk/logs
# 指定server地址，server.id=hostname:port:port。第一个端口用于集合体中的 follower 以侦听 leader；第二个端口用于 Leader 选举。第一个hostname即为本服务器地址
server.1=192.168.242.131:2888:3888
```

2.4 修改好zoo.cfg配置之后，在创建好的data目录中添加myid文件，里面的内容设置为zoo.cfg中配置的server.1中的数字，即1，有多台可以进行类似配置。

2.5 配置系统环境变量

```
vi /etc/profile
```

添加

```
export ZOOKEEPER_HOME=/home/kinson/zk 
PATH=$ZOOKEEPER_HOME/bin:$PATH
```

使添加的配置其生效

```
source /etc/profile
```

2.6 服务启动及客户端相连，最好是在root用户下启动

```
zkServer.sh start
```

启动完之后可以查看启动状态

```
zkServer.sh status
```

客户端连接

```
zkCli.sh -server localhost:2181
```

连接成功如下图：

![](https://img2018.cnblogs.com/blog/761230/201903/761230-20190331142727565-746364350.png)

之后就可以使用一些基础命令，比如 ls，create，delete，get 来测试了。

### 3、ZK常用命令

3.1 ZK服务命令

```
# 启动ZK服务       
zkServer.sh start
# 查看ZK服务状态 
zkServer.sh status
# 停止ZK服务       
zkServer.sh stop
# 重启ZK服务       
zkServer.sh restart
```

3.2 ZK客户端命令

```
# 显示根目录下、文件： 
ls /  #使用ls命令来查看当前ZooKeeper中所包含的内容
# 显示根目录下、文件： 
ls2 /  #查看当前节点数据并能看到更新次数等数据
# 创建文件，并设置初始内容：
create /zk "kinson"  #创建一个新的znode节点"zk"以及与它关联的字符串
# 获取文件内容： 
get /zk  # 确认 znode 是否包含我们所创建的字符串
# 修改文件内容： 
set /zk "king"  #对zk所关联的字符串进行设置
# 删除文件 
delete /zk  #将znode节点zk删除
# 退出客户端： 
quit
# 帮助命令： 
help
```



