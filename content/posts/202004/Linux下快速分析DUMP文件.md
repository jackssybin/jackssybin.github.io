title: Linux下快速分析DUMP文件
date: '2020-04-20 21:37:33'
updated: '2020-04-20 21:37:33'
tags: [jvm, 内存溢出, linux, mat]
permalink: /articles/2020/04/20/1587389853090.html
---
dump文件传输到本地进行分析， 常常需要大量的等待时间。 使用IBM的eclipse的MAT工具可以直接在服务器上进行快速DUMP分析。

 

### 运行环境要求

* linux操作系统
* JDK8 以上

### 下载MAT的linux版本

[Eclipse的MAT工具下载链接](http://www.eclipse.org/mat/downloads.php)  
MAT支持各种操作系统，找到Linux版本下载下来

```
# 运行uname -m 看一下linux是 x86_64还是 x86的帮助你选择下载那个版本。
uname -m
#x86_64

```

```
http://iso.mirrors.ustc.edu.cn/eclipse/mat/1.8/rcp/MemoryAnalyzer-1.8.0.20180604-linux.gtk.x86_64.zip

```

### 解压配置MAT基本参数

```
unzip MemoryAnalyzer-1.8.0.20180604-linux.gtk.x86_64.zip
## 修改MAT的内存大小， 注意这个大小要根据你dump文件大小来的，如果dump文件是5GB那么 这里最好配>5GB 否则会报MAT内存不足的异常
## 修改MemoryAnalyzer.ini 的 -Xmx6024m 
vi MemoryAnalyzer.ini

```

### jmap dump整个堆
```
jmap -dump:format=b,file=jmap.info PID
```

### MAT分析 dump

```
 ./ParseHeapDump.sh jmap.info  org.eclipse.mat.api:suspects org.eclipse.mat.api:overview org.eclipse.mat.api:top_components

```

### 等待结果….

结果会生产如下三个zip文件，很小可以直接拷贝到本机

```
jmap_Leak_Suspects.zip
jmap_System_Overview.zip
jmap_Top_Components.zip

```

### 查看报告结果

有两种查看报告的方法

* 直接把zip下载到本地，然后解压用浏览器查看index.html
* 把zip下载到本地， 用MAT可视化工具解析zip

#### 如果有异常Unable to initialize GTK+

遇到这个问题的话，是因为ParseHeapDump.sh  
里面需要调用GTK的一些东西。解决方法：

```
vi ParseHeapDump.sh
#注释掉 "$(dirname -- "$0")"/MemoryAnalyzer -consolelog -application org.eclipse.mat.api.parse "$@"这一行
#然后加入下面
#注意plugins/org.eclipse.equinox.launcher_1.5.0.v20180512-1130.jar要根据你自己本地的文件名做修改调整
java -Xmx4g -Xms4g \
-jar  plugins/org.eclipse.equinox.launcher_1.5.0.v20180512-1130.jar \
-consoleLog -consolelog -application org.eclipse.mat.api.parse "$@"

```

然后继续运行

```
 ./ParseHeapDump.sh jmap.info  org.eclipse.mat.api:suspects org.eclipse.mat.api:overview org.eclipse.mat.api:top_components
```
