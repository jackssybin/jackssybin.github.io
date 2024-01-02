title: python基础之常用模块
date: '2019-08-03 20:53:19'
updated: '2019-11-04 12:24:12'
tags: [python学习]
permalink: /articles/2019/09/16/1568646255462.html
---
![](https://img.hacpai.com/bing/20190408.jpg?imageView2/1/w/960/h/540/interlace/1/q/100) 

# Python生成requirements.txt方法
pip freeze > requirements.txt

安装requirements.txt依赖

pip install -r requirements.txt
# 常用模块
socket模块

常用于通讯，任何通讯工具中都含有socket，比如qq，微信。

udp实例：

# 导入模块

import socket

def main():

    # 创建套接字 

    # 参数一：ip协议，socket.AF_INET表示ipv4协议。

    # 参数二：使用udp协议还是tcp协议 socket.SOCK_DGRAM表示udp协议。

    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    # 绑定信息，里面是一个元组，第一个参数为ip，""表示自己的ip

    # 第二个表示端口号

    udp_socket.bind(("",7890))

    # 接收对方的ip地址

    dest_ip = input("请输入对方的ip：")

    # 接收对方的端口(port)

    dest_port = int(input("请输入对方的接收端口:"))

    # 接收发送消息

    send_data = input("请输入需要发送的消息：")

    # 发送消息

    # 参数一：表示需要发送的消息。

    # 参数二：一个元组，第一个为对方的ip地址，第二个为对方的端口号

    udp_socket.sendto(send_data.encode("utf-8"),(dest_ip,dest_port))

    # 接收消息 1024表示能接收的最大值。

    recv_data = udp_socket.recvfrom(1024)

    # 输出接收到的消息，返回的也是一个元组，1，发送过来的信息2，表示发送方的ip和端口

    # 为什么需要解码gbk？因为Windows的编码为gbk

    print(recv_data[0].decode("gbk"))  

    # 关闭套接字

    udp_socket.close()

if __name__ == "__main__":

    main()

可以看到上文需要输入对方的ip地址和端口号，为什么？

简单来说就是通过ip地址找到你的电脑，再通过端口号找到接收的程序。

其他的注释应该很清楚了。tcp和udp的区别？

tcp是传输比较稳定，不掉包，udp是传输快，容易掉包。

掉包的意思就是说发送过去，对方一不定可以接收到（当然数据过大的时候会出现这种情况。）

这里补充几个名词的含义。

单工：比如说收音机，只能发，或者只能收消息。

半双工：能发也能收，但是在同一时刻只能收或只能发。

全双工：同一时刻能发也能收。

tcp实例

import socket

def main():

    # 创建套接字 

    # 参数一：ip协议，socket.AF_INET表示ipv4协议。

    # 参数二：使用udp协议还是tcp协议 socket.SOCK_STREAM表示tcp协议

    tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 绑定信息，里面是一个元组，第一个参数为ip，""表示自己的ip

    # 第二个表示端口号

    tcp_socket.bind(("",7890))

    # 接收对方的ip地址

    dest_ip = input("请输入对方的ip：")

    # 接收对方的端口(port)

    dest_port = int(input("请输入对方的接收端口:"))

    # 链接服务器

    tcp_socket.connec((dest_ip,dest_port))

    # 接收发送消息

    send_data = input("请输入需要发送的消息：")

    # 发送消息

    tcp_socket.send(send_data.encode("utf-8"))

    # 接收消息 1024表示能接收的最大值。

    recv_data = tcp_socket.recv(1024)

    # 输出接收到的消息，返回的也是一个元组，1，发送过来的信息2，表示发送方的ip和端口

    # 为什么需要解码gbk？因为Windows的编码为gbk

    print(recv_data[0].decode("gbk"))  

    # 关闭套接字

    tcp_socket.close()

if __name__ == "__main__":

    main()

time模块

import time #导入模块

time.sleep(5) # 停留5秒，不给钱不优化那种

time.time() # 返回从1970年1月1日到现在经历了多少秒。

# 格式化时间

time.strftime("%Y-%m-%d %H:%M:%S") # 2018-11-08 21:50:01

time.strftime("%Y/%m/%d %H:%M:%S") # 2018/11/08 21:50:01 

其他格式：

%Y 四位数的年份表示（000-9999）

%m 月份（01-12）

%d 月内中的一天（0-31）

%H 24小时制小时数（0-23）

%I 12小时制小时数（01-12） 

%M 分钟数（00=59）

%S 秒（00-59）

%a 本地简化星期名称

%A 本地完整星期名称

%b 本地简化的月份名称

%B 本地完整的月份名称

%c 本地相应的日期表示和时间表示

%j 年内的一天（001-366）

%p 本地A.M.或P.M.的等价符

%U 一年中的星期数（00-53）星期天为星期的开始

%w 星期（0-6），星期天为星期的开始

%W 一年中的星期数（00-53）星期一为星期的开始

%x 本地相应的日期表示

%X 本地相应的时间表示

%Z 当前时区的名称

%% %号本身 

# 以上自己可以试试。

time.localtime() # 结构化时间

# time.struct_time(tm_year=2018, tm_mon=11, tm_mday=8, tm_hour=21, tm_min=59, tm_sec=14, tm_wday=3, tm_yday=312, tm_isdst=0)

time.tm_year # 返回年

# 将时间戳转化为结构化时间

t = time.time()

time.localtime(t) # 现在的时间

time.gmtime() # 国外某地点现在的时间

# 将格式化时间转化为时间戳

strtime = '2018-11-08 21:50:01'

time.mktime(strtime)

# 将格式化时间转化为结构化时间

time.strptime('2018-11-8','%Y-%m-%d')

# 将结构化时间转化为格式化时间

time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(1600000000))

其他类型时间

time.asctime() # Thu Nov  8 22:22:27 2018

time.ctime(1600000000) # Sun Sep 13 20:26:40 2020

random随机数模块

实例：

    # 导入模块

    import random

    # 随机整数

    random.randint(0,5) # 返回大于0小于等于5的整数

    # 随机偶数

    random.randrange(0,10,2) # 返回大于等于0小于10的偶数，2为步长，和列表一样

    # 随机返回其中一个值

    random.choice([1,2,3,4,5]) # 随机返回其中一个值

    # 随机返回多个值

    random.sanple([1,2,3,4,5],3) # 随机返回3个值，返回几个取决于第二个参数

    # 打乱列表顺序

    list = [1,2,3,4,5]

    random.shuffle(list) # 随机打乱列表的顺序)

os 模块（与操作系统相关）

实例：

    #导入模块

    import os

    # getcwd() 获取当前工作目录(当前工作目录默认都是当前文件所在的文件夹)

    os.getcwd() 

    # chdir()改变当前工作目录

    os.chdir('/python/Demo')

    # listdir() 获取指定文件夹中所有内容的名称列表

    os.listdir('/python/Demo')

    # mkdir()创建文件夹

    os.mkdir('Test')

    # makedirs()递归创建文件夹

    os.makedirs('/python/Demo/Test/A/B')

    # rmdir() 删除空目录

    os.rmdir('Demo')

    # removedirs递归删除文件夹  必须都是空目录

    os.removedirs('/python/Demo/Test/A/B')

    # stat()获取文件或者文件夹的信息

    os.stat('/python3/Demo.py)

    # system()执行系统命令

    os.system('ls -al')  #获取隐藏文件

    # abspath()将相对路径转化为绝对路径

    path = './Demo' #相对

    result = os.path.abspath(path)

    print(result)

    # dirname()获取完整路径当中的目录部分 

    path = '/python3/Demo/Test' 

    os.path.dirname(path) # /python3/Demo

    # basename()获取完整路径当中的主体部分

    os.path.basename(path) # Test

    #split() 将一个完整的路径切割成目录部分和主体部分

    result = os.path.split(path)

    print(result) #返回一个元组('/python3/Demo', 'Test')

    # join()将2个路径合并成一个

    path1 = '/python3/Demo'

    path2 = 'Test.py'

    os.path.join(path1,path2)# '/python3/Demo/Test.py'

    # splitext() 将一个路径切割成文件后缀和其他两个部分,主要用于获取文件的后缀

    path = '/python3/Demo/Test.py'

    os.path.splitext(path) # ('/python3/Demo/Test', '.py')

    # getsize()  获取文件的大小

    path = '/python3/Demo/Test.py'

    os.path.getsize(path)

    # isfile()检测是否是文件

    path = '/python3/Demo/Test.py'

    os.path.isfile(path)

    # isdir()检测是否是文件夹

    os.path.isdir(path)

    # islink() 检测是否是链接

    os.path.islink(path)

    # getctime()获取文件的创建时间

    # getmtime()获取文件的修改时间

    # getatime()获取文件的访问时间

    # getenv() 获取系统的环境变量

    # curdir表示当前文件夹  .表示当前文件夹

    print(os.curdir)

    #pardir表示上一层文件夹  ..表示上一层文件夹

    #name 获取代表操作系统的名称字符串

    print(os.name)

    #sep 获取系统路径间隔符号 

    print(os.sep) # window是\ linux事/

    #linesep  获取操作系统的换行符号

    print(os.linesep) # window 是\r\n  linux/unix 是 \n

sys 模块(和python解释器交互)

 # 导入模块

    import sys

    sys.exit() # 退出程序 

    # sys.exit(0) 正常退出 sys.exit(1)遇见错误退出

    print(sys.platform) # 操作系统名称

    print(sys.version) # python解释器的版本

    sys.path # 返回模块的搜索路径

    sys.argv # 实现从程序外部向程序传递参数。在终端才能看出效果，现在知道就好

序列化与反序列化模块

str = "[1,2,3,4,5,6]"

# 当我们想要像调用列表一样调用上面的字符串时，我们需要反序列化

# 同理 当我们将比如列表转换为字符串类型就称之为序列化

# json 每个语言都通用的序列化格式。但是能用json转化的数据类型较少

# pickle python中的所有数据类型都可以序列化，但是只有python认识

# shelve 新来的，方便，不完善

json:

 # 导入模块

    import json # 可以转化的有 数字，字符串，列表，字典，元组（转化为列表）

    # 序列化

    list = [1,2,3,4,5]

    print(type(list)) # <class 'list'> 列表类型

    str = json.dumps(list)

    print(type(str)) # <class 'str'> 此时就转化为了字符串格式

    # 反序列化

    attr = json.loads(str)

    print(type(attr)) # <class 'list'> 列表类型

    # 序列化写入文件

    f = open('txt','w',encoding = 'utf-8')

    json.dump(list,f，ensure_ascii=False) # 把list 序列化写入文件 ensure_ascii=False如果有中文需要加上

    f.close()

    # 从文件里拿出数据反序列化

    f = open('txt','r',encoding = 'utf-8')

    txt =json.load(f)

    f.close()

    print(type(txt)) # list 返回的list

pickle:

    # 导入模块

    import pickle # 可以序列化所有数据类型

    # 使用方法也是  dumps，dumps，loads，load

    # 不同的是 dumps 返回的是bytes类型 loads之后就正常了。

    # 同样的写入文件的时候需要wb，和rb

shelve:

    # 导入模块

    import shelve

    # 序列化

    # 拿到句柄

    ff = shelve.open('text')

    # 这样就序列化了

    ff['txt'] = [1,2,3,4,5]

    ff.close()

    # 反序列化

    # 拿到句柄

    # 这样就反序列化了

    ff = shelve.open('text')

    txt = ff['txt']

    ff.close()

    print(txt)

collections模块

当我们想要表示一个点的坐标时

实例：

    # 导入模块

    from collections import namedtuple

    # namedtuple参数一：起的名字，参数二：坐标名

    Spot = namedtuple('spot',['x','y'])

    # 添加数据

    s = Spot(3,4)

    # 输出x

    print(s.x)   

    # 输出y

    print(s.y)

queue模块# 队列

实例：

    # 导入模块

    import queue

    # 创建一个队列

    q = queue.Queue()

    q.put(1)

    q.put(2)

    print(q.get()) # 1

    print(q.get()) # 2

    print(q.get()) # 发生堵塞,不会报错

    # 先进先出

deque # 双端队列

实例：

    # 导入模块

    from collections import deque 

    # 创建一个双端队列

    de = deque()

    # 从前面添加数据

    de.appendleft(111)

    # 从后面添加数据

    de.append(222) 

    # 在指定位置添加数据

    de.insert(1,333)

    # 从前面取数据

    print(de.popleft())

    # 从后面取数据

    print(de.pop())

当我们想要一个字典key值有序时

实例：

    # 导入模块

    from collections import OrderedDict

    d = {'q':'1','w':'2','e':'3'}

    # 因为字典的key值是无序的，想要变得有序这样既可：

    ordict = OrderedDict(d)

给字典设置默认value值。

    from collections import defaultdict

    dict = defaultdict(list)

    print(dict['key1']) # 输出[]

# 参数必须是可以调用的比如list，set，dict，也可以是自己写的函数，随意。

# 为什么设置默认值？因为当不存在value值时，不能调用字典的append方法。

当我们想要统计一个单词某个字母出现的个数时

    # 导入模块

    from collections import Counter

    num = Counter('qweasdqwertdgfdaDSD')

    print(num) # 结果：Counter({'q': 4, 'w': 4, 'e': 4})

    print(num['q']) # 4 