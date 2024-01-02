title: 如何定位java进程中使用最耗内存的进程
date: '2019-09-23 17:17:37'
updated: '2019-11-18 11:06:56'
tags: [java, jstack, 线程, 调优]
permalink: /articles/2019/09/23/1569230256915.html
---
### 1.清除进程和线程的关系
### 2.知道linux查看进程对应线程的命令
查看进程命令
```
ps -ef |grep java
```
查看进程对应线程命令
```
top -Hp <pid>
```
找到最大线程的pid号
### 3.打印堆栈信息
```
jstack <pid>
```
jstack 里面存的是16进制的数字。所以需要把十进制转换为16进制
```
printf "%x\n" pid
jstack pid |grep 'nid' -C5 –color
```
找到了16进制的pid号。那就直接可以在jstack里搜索找到对应进程信息了，就能找到对应的代码了

**生成dump文件：**
```
 jmap -dump:format=b,file=/path/heap.bin 进程ID
    
 jmap -dump:live,format=b,file=/path/heap.bin 进程ID
```
**live参数：**

表示我们需要抓取目前在生命周期内的内存对象,也就是说GC收不走的对象,然后我们绝大部分情况下,需要的看的就是这些内存。而且会减小dump文件的大小。

### 4.案例
* 背景
    
* 1、java 正则表达式回溯造成 CPU 100%
    
* 2、线程死锁，程序 hang 住
    
* 3、免费实用的脚本工具大礼包
    

* （1）show-duplicate-java-classes
    
* （2）find-in-jars
    
* （3）housemd pid [java_home]
    
* （4）jvm pid
    
* （5）greys[@IP:PORT]
    
* （6）sjksjk --commands sjk --help

```
#查线程cpu100  4步走
1. top oder by with P：1040 // 首先按进程负载排序找到  axLoad(pid)  
2. top -Hp 进程PID：1073    // 找到相关负载 线程PID  
3. printf “0x%x\n”线程PID： 0x431  // 将线程PID转换为 16进制，为后面查找 jstack 日志做准备  
4. jstack  进程PID | vim +/十六进制线程PID -        // 例如：jstack 1040|vim +/0x431 -
```
**工具：**
show-busy-java-threads.sh（[https://github.com/oldratlee/useful-scripts](https://github.com/oldratlee/useful-scripts)）
**示例代码：**
```
import java.util.ArrayList;  
import java.util.List;  
import java.util.regex.Matcher;  
import java.util.regex.Pattern;  
public class RegexLoad {  
    public static void main(String[] args) {  
        String[] patternMatch = {"([\\w\\s]+)+([+\\-/*])+([\\w\\s]+)",  
                "([\\w\\s]+)+([+\\-/*])+([\\w\\s]+)+([+\\-/*])+([\\w\\s]+)"};  
        List<String> patternList = new ArrayList<String>();  
  
        patternList.add("Avg Volume Units product A + Volume Units product A");  
        patternList.add("Avg Volume Units /  Volume Units product A");  
        patternList.add("Avg retailer On Hand / Volume Units Plan / Store Count");  
        patternList.add("Avg Hand Volume Units Plan Store Count");  
        patternList.add("1 - Avg merchant Volume Units");  
        patternList.add("Total retailer shipment Count");  
  
        for (String s :patternList ){  
  
            for(int i=0;i<patternMatch.length;i++){  
                Pattern pattern = Pattern.compile(patternMatch[i]);  
  
                Matcher matcher = pattern.matcher(s);  
                System.out.println(s);  
                if (matcher.matches()) {  
  
                    System.out.println("Passed");  
                }else  
                    System.out.println("Failed;");  
            }  
  
        }  
    }  
}
```
编译javac RegexLoad.java  &java RegexLoad 运行之后。top发现占用cpu99的一个java进程
工具使用
```
第一次执行。我的返回了 sh编译错误，兼容性问题，因为linux将sh默认指向了dash，而不是bash
root@iZ2ze8um4r4f2fiahuutedZ:~/data/java/useful-scripts# sh show-busy-java-threads
show-busy-java-threads: 13: show-busy-java-threads: Syntax error: "(" unexpected
通过
在root下面执行 dpkg-reconfigure dash,选择no 解决问题。继续执行
sh show-busy-java-threads.sh 
立即定位到了繁忙的进程
```

**工具使用api说明：**
```
show-busy-java-threads.sh  
# 从 所有的 Java进程中找出最消耗CPU的线程（缺省5个），打印出其线程栈。    
show-busy-java-threads.sh -c <要显示的线程栈数>  
show-busy-java-threads.sh -c <要显示的线程栈数> -p <指定的Java Process>  
# -F选项：执行jstack命令时加上-F选项（强制jstack），一般情况不需要使用  
show-busy-java-threads.sh -p <指定的Java Process> -F  
show-busy-java-threads.sh -s <指定jstack命令的全路径>  
# 对于sudo方式的运行，JAVA_HOME环境变量不能传递给root，  
# 而root用户往往没有配置JAVA_HOME且不方便配置，  
# 显式指定jstack命令的路径就反而显得更方便了  
show-busy-java-threads.sh -a <输出记录到的文件>   
show-busy-java-threads.sh -t <重复执行的次数> -i <重复执行的间隔秒数>  
# 缺省执行一次；执行间隔缺省是3秒  
  
##############################  
# 注意：  
##############################  
# 如果Java进程的用户 与 执行脚本的当前用户 不同，则jstack不了这个Java进程。  
# 为了能切换到Java进程的用户，需要加sudo来执行，即可以解决：  
sudo show-busy-java-threads.sh
```
# 3、免费实用的脚本工具大礼包

除了正文提到的 show-busy-java-threads.sh，oldratlee 同学还整合和不少常见的开发、运维过程中涉及到的脚本工具，觉得特别有用的我简单列下：

## （1）show-duplicate-java-classes

偶尔会遇到本地开发、测试都正常，上线后却莫名其妙的 class 异常，历经千辛万苦找到的原因竟然是 Jar冲突！这个工具就可以找出Java Lib（Java库，即Jar文件）或Class目录（类目录）中的重复类。

Java开发的一个麻烦的问题是Jar冲突（即多个版本的Jar），或者说重复类。会出NoSuchMethod等的问题，还不见得当时出问题。找出有重复类的Jar，可以防患未然。

```
# 查找当前目录下所有Jar中的重复类show-duplicate-java-classes
# 查找多个指定目录下所有Jar中的重复类
show-duplicate-java-classes path/to/lib_dir1 /path/to/lib_dir2
# 查找多个指定Class目录下的重复类。Class目录 通过 -c 选项指定
show-duplicate-java-classes -c path/to/class_dir1 -c /path/to/class_dir2
# 查找指定Class目录和指定目录下所有Jar中的重复类的Jar
show-duplicate-java-classes path/to/lib_dir1 /path/to/lib_dir2 -c path/to/class_dir1 -c path/to/class_dir2
```

例如：

```
# 在war模块目录下执行，生成war文件$ mvn install...
# 解压war文件，war文件中包含了应用的依赖的Jar文件$ unzip target/*.war -d target/war...
# 检查重复类$ show-duplicate-java-classes -c target/war/WEB-INF/classes target/war/WEB-INF/lib...
```

## （2）find-in-jars

在当前目录下所有jar文件里，查找类或资源文件。

用法：注意，后面Pattern是grep的 扩展正则表达式。

```
find-in-jars 'log4j\.properties'
find-in-jars 'log4j\.xml$' -d /path/to/find/directory
find-in-jars log4j\\.xml
find-in-jars 'log4j\.properties|log4j\.xml'
```

示例：

```
$ ./find-in-jars 'Service.class$'
./WEB-INF/libs/spring-2.5.6.SEC03.jar!org/springframework/stereotype/Service.class
./rpc-benchmark-0.0.1-SNAPSHOT.jar!com/taobao/rpc/benchmark/service/HelloService.class
```

## （3）housemd pid [java_home]

很早的时候，我们使用BTrace排查问题，在感叹BTrace的强大之余，也曾好几次将线上系统折腾挂掉。2012年淘宝的聚石写了HouseMD，将常用的几个Btrace脚本整合在一起形成一个独立风格的应用，其核心代码用的是Scala，HouseMD是基于字节码技术的诊断工具, 因此除了Java以外, 任何最终以字节码形式运行于JVM之上的语言, HouseMD都支持对它们进行诊断, 如Clojure(感谢@Killme2008提供了它的使用入门), scala, Groovy, JRuby, Jython, kotlin等.

使用housemd对java程序进行运行时跟踪，支持的操作有：

* 查看加载类    
* 跟踪方法    
* 查看环境变量    
* 查看对象属性值    
* 详细信息请参考: https://github.com/CSUG/HouseMD/wiki/UserGuideCN
    
## （4）jvm pid

执行jvm debug工具，包含对java栈、堆、线程、gc等状态的查看，支持的功能有：

```
========线程相关=======
1 : 查看占用cpu最高的线程情况
2 : 打印所有线程
3 : 打印线程数
4 : 按线程状态统计线程数
========GC相关=======
5 : 垃圾收集统计（包含原因）可以指定间隔时间及执行次数，默认1秒, 10次
6 : 显示堆中各代的空间可以指定间隔时间及执行次数，默认1秒，5次
7 : 垃圾收集统计。可以指定间隔时间及执行次数，默认1秒, 10次
8 : 打印perm区内存情况*会使程序暂停响应*
9 : 查看directbuffer情况========堆对象相关=======
10 : dump heap到文件*会使程序暂停响应*默认保存到`pwd`/dump.bin,可指定其它路径
11 : 触发full gc。*会使程序暂停响应*
12 : 打印jvm heap统计*会使程序暂停响应*
13 : 打印jvm heap中top20的对象。
*会使程序暂停响应*参数：
	1:按实例数量排序,
	2:按内存占用排序，默认为1
14 : 触发full gc后打印jvm heap中top20的对象。
*会使程序暂停响应*参数：
	1:按实例数量排序,
	2:按内存占用排序，默认为1
15 : 输出所有类装载器在perm里产生的对象。可以指定间隔时间及执行次数
========其它=======
16 : 打印finalzer队列情况
17 : 显示classloader统计
18 : 显示jit编译统计
19 : 死锁检测
20 : 等待X秒，默认为1
```
进入jvm工具后可以输入序号执行对应命令  
可以一次执行多个命令，用分号";"分隔，如：1;3;4;5;6  
每个命令可以带参数，用冒号":"分隔，同一命令的参数之间用逗号分隔，如：

```
Enter command queue:1;5:1000,100;10:/data1/output.bin
```

## （5）greys[@IP:PORT]

PS：目前Greys仅支持Linux/Unix/Mac上的Java6+，Windows暂时无法支持

Greys是一个JVM进程执行过程中的异常诊断工具，可以在不中断程序执行的情况下轻松完成问题排查工作。和HouseMD一样，Greys-Anatomy取名同名美剧“实习医生格蕾”，目的是向前辈致敬。代码编写的时候参考了BTrace和HouseMD两个前辈的思路。

使用greys对java程序进行运行时跟踪(不传参数，需要先greys -C pid,再greys)。支持的操作有：

* 查看加载类，方法信息
    
* 查看JVM当前基础信息
    
* 方法执行监控（调用量，失败率，响应时间等）
    
* 方法执行数据观测、记录与回放（参数，返回结果，异常信息等）
    
* 方法调用追踪渲染
    
* 详细信息请参考: https://github.com/oldmanpushcart/greys-anatomy/wiki
    

## （6）sjksjk --commands sjk --help

使用sjk对Java诊断、性能排查、优化工具

* ttop:监控指定jvm进程的各个线程的cpu使用情况
    
* jps: 强化版
    
* hh: jmap -histo强化版
    
* gc: 实时报告垃圾回收信息
    
* 更多信息请参考: https://github.com/aragozin/jvm-tools


