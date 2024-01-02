title: jvm调优(堆溢出和调优参数)
date: '2020-04-13 18:13:34'
updated: '2020-04-22 14:18:24'
tags: [jvm, 调优, 内存溢出, 调优参数]
permalink: /articles/2020/04/13/1586772814684.html
---
![](https://img.hacpai.com/bing/20180830.jpg?imageView2/1/w/960/h/540/interlace/1/q/100)

## 内存溢出和内存泄漏的区别：

内存溢出 out of memory，是指程序在申请内存时，没有足够的内存空间供其使用，出现out of memory；比如申请了一个integer,但给它存了long才能存下的数，那就是内存溢出。

内存泄露 memory leak，是指程序在申请内存后，无法释放已申请的内存空间，一次内存泄露危害可以忽略，但内存泄露堆积后果很严重，无论多少内存,迟早会被占光。

memory leak会最终会导致out of memory

内存溢出就是你要求分配的内存超出了系统能给你的，系统不能满足需求，于是产生溢出。

内存泄漏是指你向系统申请分配内存进行使用(new)，可是使用完了以后却不归还(delete)，结果你申请到的那块内存你自己也不能再访问（也许你把它的地址给弄丢了），而系统也不能再次将它分配给需要的程序。一个盘子用尽各种方法只能装4个果子，你装了5个，结果掉倒地上不能吃了。这就是溢出！比方说栈，栈满时再做进栈必定产生空间溢出，叫上溢，栈空时再做退栈也产生空间溢出，称为下溢。就是分配的内存不足以放下数据项序列,称为内存溢出.

## 全文简短总结，具体内容可以看下文。

### 栈内存溢出(StackOverflowError)：

程序所要求的栈深度过大导致，可以写一个死递归程序触发。

### 堆内存溢出(OutOfMemoryError:java heap space)

* 分清内存溢出还是内存泄漏
* 泄露则看对象如何被 GC Root 引用。
* 溢出则通过 调大 -Xms，-Xmx参数。

### 持久带内存溢出(OutOfMemoryError: PermGen space)

* 持久带中包含方法区，方法区包含常量池
* 因此持久带溢出有可能是运行时常量池溢出，也有可能是方法区中保存的class对象没有被及时回收掉或者class信息占用的内存超过了我们配置
* 用String.intern()触发常量池溢出
* Class对象未被释放，Class对象占用信息过多，有过多的Class对象。可以导致持久带内存溢出

### 无法创建本地线程

总容量不变，堆内存，非堆内存设置过大，会导致能给线程的内存不足。

**以下是详细内容**

# 栈溢出(StackOverflowError)

栈溢出抛出StackOverflowError错误，**出现此种情况是因为方法运行的时候栈的深度超过了虚拟机容许的最大深度所致**。出现这种情况，一般情况下是程序错误所致的，比如写了一个死递归，就有可能造成此种情况。 下面我们通过一段代码来模拟一下此种情况的内存溢出。

```java
import java.util.*;    
import java.lang.*;    
public class OOMTest{     
    public void stackOverFlowMethod(){    
        stackOverFlowMethod();    
    }    
    public static void main(String... args){    
        OOMTest oom = new OOMTest();    
        oom.stackOverFlowMethod();    
    }    
}    

```

运行上面的代码，会抛出如下的异常：

```xml
Exception in thread "main" java.lang.StackOverflowError    
        at OOMTest.stackOverFlowMethod(OOMTest.java:6)   

```

对于栈内存溢出，根据《Java 虚拟机规范》中文版：

> 如果线程请求的栈容量超过栈允许的最大容量的话，Java 虚拟机将抛出一个StackOverflow异常；如果Java虚拟机栈可以动态扩展，并且扩展的动作已经尝试过，但是无法申请到足够的内存去完成扩展，或者在新建立线程的时候没有足够的内存去创建对应的虚拟机栈，那么Java虚拟机将抛出一个OutOfMemory 异常。

# 堆溢出(OutOfMemoryError:java heap space)

堆内存溢出的时候，虚拟机会抛出java.lang.OutOfMemoryError:java heap space,出现此种情况的时候，我们需要根据内存溢出的时候产生的dump文件来具体分析（需要增加-XX:+HeapDumpOnOutOfMemoryErrorjvm启动参数）。**出现此种问题的时候有可能是内存泄露，也有可能是内存溢出了。**

* 如果内存泄露，我们要找出泄露的对象是怎么被GC ROOT引用起来，然后通过引用链来具体分析泄露的原因。
* 如果出现了内存溢出问题，这往往是程序本生需要的内存大于了我们给虚拟机配置的内存，这种情况下，我们可以采用调大-Xmx来解决这种问题。下面我们通过如下的代码来演示一下此种情况的溢出：

```java
import java.util.*;    
import java.lang.*;    
public class OOMTest{    
        public static void main(String... args){    
                List<byte[]> buffer = new ArrayList<byte[]>();    
                buffer.add(new byte[10*1024*1024]);    
        }    

}    

```

我们通过如下的命令运行上面的代码：

```xml
java -verbose:gc -Xmn10M -Xms20M -Xmx20M -XX:+PrintGC OOMTest

```

程序输出如下的信息：

```css
[GC 1180K->366K(19456K), 0.0037311 secs]    
[Full GC 366K->330K(19456K), 0.0098740 secs]    
[Full GC 330K->292K(19456K), 0.0090244 secs]    
Exception in thread "main" java.lang.OutOfMemoryError: Java heap space    
        at OOMTest.main(OOMTest.java:7)    

```

从运行结果可以看出，JVM进行了一次Minor gc和两次的Major gc，从Major gc的输出可以看出，gc以后old区使用率为134K，而字节数组为10M，加起来大于了old generation的空间，所以抛出了异常，如果调整-Xms21M,-Xmx21M,那么就不会触发gc操作也不会出现异常了。

通过上面的实验其实也从侧面验证了一个结论：**对象大于新生代剩余内存的时候，将直接放入老年代，当老年代剩余内存还是无法放下的时候，触发垃圾收集，收集后还是不能放下就会抛出内存溢出异常了。**

# 持久带溢出(OutOfMemoryError: PermGen space)

我们知道Hotspot jvm通过持久带实现了Java虚拟机规范中的方法区，而运行时的常量池就是保存在方法区中的，因此持久带溢出有可能是运行时常量池溢出，也有可能是方法区中保存的class对象没有被及时回收掉或者class信息占用的内存超过了我们配置。  
当持久带溢出的时候抛出java.lang.OutOfMemoryError: PermGen space。可能在如下几种场景下出现：

1. 使用一些应用服务器的热部署的时候，我们就会遇到热部署几次以后发现内存溢出了，这种情况就是因为每次热部署的后，原来的class没有被卸载掉。
2. 如果应用程序本身比较大，涉及的类库比较多，但是我们分配给持久带的内存（通过-XX:PermSize和-XX:MaxPermSize来设置）比较小的时候也可能出现此种问题。
3. 一些第三方框架，比如spring,hibernate都通过字节码生成技术（比如CGLib）来实现一些增强的功能，这种情况可能需要更大的方法区来存储动态生成的Class文件。  
    我们知道Java中字符串常量是放在常量池中的，String.intern()这个方法运行的时候，会检查常量池中是否存和本字符串相等的对象，如果存在直接返回对常量池中对象的引用，不存在的话，先把此字符串加入常量池，然后再返回字符串的引用。那么我们就可以通过String.intern方法来模拟一下运行时常量区的溢出.下面我们通过如下的代码来模拟此种情况：

```java
import java.util.*;    
import java.lang.*;    
public class OOMTest{    
        public static void main(String... args){    
                List<String> list = new ArrayList<String>();    
                while(true){    
                        list.add(UUID.randomUUID().toString().intern());    
                }    
        }        
}    

```

我们通过如下的命令运行上面代码：

```xml
java -verbose:gc -Xmn5M -Xms10M -Xmx10M -XX:MaxPermSize=1M -XX:+PrintGC OOMTest

```

运行后的输入如下图所示:

```css
Exception in thread "main" java.lang.OutOfMemoryError: PermGen space    
        at java.lang.String.intern(Native Method)    
        at OOMTest.main(OOMTest.java:8)   

```

通过上面的代码，我们成功模拟了运行时常量池溢出的情况，从输出中的PermGen space可以看出确实是持久带发生了溢出，这也验证了，我们前面说的Hotspot jvm通过持久带来实现方法区的说法。

# OutOfMemoryError:unable to create native thread

最后我们在来看看java.lang.OutOfMemoryError:unable to create natvie thread这种错误。 出现这种情况的时候，一般是下面两种情况导致的：

1. 程序创建的线程数超过了操作系统的限制。对于Linux系统，我们可以通过ulimit -u来查看此限制。
2. 给虚拟机分配的内存过大，导致创建线程的时候需要的native内存太少。

我们都知道操作系统对每个进程的内存是有限制的，我们启动Jvm,相当于启动了一个进程，假如我们一个进程占用了4G的内存，那么通过下面的公式计算出来的剩余内存就是建立线程栈的时候可以用的内存。*线程栈总可用内存=4G-（-Xmx的值）- （-XX:MaxPermSize的值）- 程序计数器占用的内存*  
通过上面的公式我们可以看出，-Xmx 和 MaxPermSize的值越大，那么留给线程栈可用的空间就越小，在-Xss参数配置的栈容量不变的情况下，可以创建的线程数也就越小。因此如果是因为这种情况导致的unable to create native thread,那么要么我们增大进程所占用的总内存，或者减少-Xmx或者-Xss来达到创建更多线程的目的。

# 参数相关

- ***-XX:+HeapDumpOnOutOfMemoryError***  
参数表示当JVM发生OOM时，自动生成DUMP文件。

- ***-XX:HeapDumpPathr***  
-XX:HeapDumpPath=${目录}参数表示生成DUMP文件的路径，也可以指定文件名称，例如：-XX:HeapDumpPath=${目录}/java_heapdump.hprof。如果不指定文件名，默认为：java_<pid>_<date>_<time>_heapDump.hprof，默认目录为tomcat所在目录下。

- ***-XX:+AggressiveHeap***  
java堆最佳化设置。设置多个参数使长时间运行过的任务使用密集的内存分配。 默认这个选项时关闭的，也就是堆不是最佳化。  
- ***-XX:+AlwaysPreTouch***  
在调用main函数之前，使用所有可用的内存分页。这个选项可以用来测试长时间运行的系统，所有的内存都已被分配。默认这个选项  
是关闭的，也就是不会使用所有的内存分页。  
- ***-XX:+CMSClassUnloadingEnabled***  
当使用CMS垃圾收集器时，允许类卸载。这个选项模式是开启的。为了禁止类卸载，那么可以使用： -XX:-CMSClassUnloadingEnabled  
- ***-XX:CMSExpAvgFactor=percent***  
指定垃圾收集消耗的时间百分比。默认这个数是25%。下面的例子设置成15%：

```
-XX:CMSExpAvgFactor=15
```

* ***-XX:CMSInitiatingOccupancyFraction=percent***  
    设置CMS收集开始的百分比。默认值是-1，任何的负值表示会使用-XX:CMSTriggerRatio选项来定义这个百分比数。  
    下面的例子设置成了20%，表示老年代使用20%后开始垃圾收集；

```
-XX:CMSInitiatingOccupancyFraction=20
```

* ***-XX:+CMSScavengeBeforeRemark***  
    在CMS重新标记之前执行清除操作，默认这个选项是关闭的。
* ***-XX:CMSTriggerRatio=percent***  
    设置由-XX:MinHeapFreeRatio指定值的百分比的值。默认是80%。  
    下面的例子设置成了75%：

```
-XX:CMSTriggerRatio=75
```

* ***-XX:ConcGCThreads=threads***  
    并发GC的线程数量。默认值根据cpu的数量而定。下面的例子把这个值设置为2

```
-XX:ConcGCThreads=2
```

* ***-XX:+DisableExplicitGC***  
    这个选项控制显式GC，也就是调用System.gc()，默认在调用这个方法的时候就会发生gc，如果不允许显式gc，那么调用这个方法的时候，就不会发生gc行为。
* ***-XX:+ExplicitGCInvokesConcurrent***  
    当调用System.gc()的时候， 执行并行gc。默认是不开启的，只有使用-XX:+UseConcMarkSweepGC选项的时候才能开启这个选项。
* ***-XX:+ExplicitGCInvokesConcurrentAndUnloadsClasses***  
    当调用System.gc()的时候， 执行并行gc。并在垃圾回收的周期内卸载类。 只有使用-XX:+UseConcMarkSweepGC选项的时候才能开启这个选项。
* ***-XX:G1HeapRegionSize=size***  
    当使用G1收集器时，设置java堆被分割的大小。这个大小范围在1M到32M之间。下面的例子把这个值设置成了16M。

```
-XX:G1HeapRegionSize=16m
```

* ***-XX:+G1PrintHeapRegions***  
    打印G1收集器收集的区域。默认这个选项是关闭的。
* ***-XX:G1ReservePercent=percent***  
    使用g1收集器时，设置保留java堆大小，防止晋升失败。范围是0到50.默认设置是10%。下面的例子把这个值设置成20%。

```
-XX:G1ReservePercent=20
```

* ***-XX:InitialHeapSize=size***  
    初始化堆大小。
* ***-XX:InitialSurvivorRatio=ratio***  
    设置幸存区的比例。
* ***-XX:InitiatingHeapOccupancyPercent=percent***  
    设置进行垃圾回收的堆占用的百分比。
* ***-XX:MaxGCPauseMillis=time***  
    设置GC最大暂停时间。默认没有最大暂停时间。下面的例子设置最大暂停时间为500毫秒。

```
-XX:MaxGCPauseMillis=500
```

* ***-XX:MaxHeapSize=size***  
    最大堆大小。
* ***-XX:MaxHeapFreeRatio=percent***  
    设置堆垃圾回收后最大空闲空间比例。默认是70%。下面的例子把这个值设置成75.

```
-XX:MaxHeapFreeRatio=75
```

* ***-XX:MaxMetaspaceSize=size***  
    设置最大的本地内存类员工间可用于垃圾回收。默认没有限制。下面的例子把这个值设置成256m

```
-XX:MaxMetaspaceSize=256m
```

* ***-XX:MaxNewSize=size***  
    新生代最大大小。
* ***-XX:MaxTenuringThreshold=threshold***  
    在新生代中对象存活次数(经过Minor GC的次数)后仍然存活，就会晋升到旧生代。
* ***-XX:MetaspaceSize=size***  
    设置类元空间大小。
* ***-XX:MinHeapFreeRatio=percent***  
    堆最小空间百分比。
* ***XX:NewRatio=ratio***  
    设置新生代和老年代的比例。
* ***-XX:NewSize=size***  
    设置年轻代的大小
* ***-XX:ParallelGCThreads=threads***  
    并行收集线程数量。
* ***-XX:+ParallelRefProcEnabled***  
    如果应用有很多的Reference or finalizable objects，那么可以使用-XX:+ParallelRefProcEnabled来减少duration。
* ***-XX:+PrintAdaptiveSizePolicy***  
    打印自适应收集的大小。默认关闭。
* ***-XX:+PrintGC***  
    打印GC信息。
* ***-XX:+PrintGCApplicationConcurrentTime***  
    打印自从上次gc停顿到现在过去了多少时间。
* ***-XX:+PrintGCApplicationStoppedTime***  
    打印gc一共停顿了多长时间。
* ***-XX:+PrintGCDateStamps***  
    打印gc时间戳
* ***-XX:+PrintGCDetails***  
    打印gc详细信息
* ***-XX:+PrintGCTaskTimeStamps***  
    为每个独立的gc线程打印时间戳。
* ***-XX:+PrintGCTimeStamps***  
    打印gc时间戳
* ***-XX:+PrintStringDeduplicationStatistics***  
    打印字符串去重统计信息。
* ***-XX:+PrintTenuringDistribution***  
    打印对各代信息。
* ***-XX:+ScavengeBeforeFullGC***  
    在进行fullGC时先进行YGC。
* ***-XX:StringDeduplicationAgeThreshold=threshold***  
    字符串存活的最小年龄 ，默认是3.
* ***-XX:SurvivorRatio=ratio***  
    幸存代的比例。
* ***-XX:TargetSurvivorRatio=percent***  
    年轻代收集后，幸存代期望的比例值。
* ***-XX:TLABSize=size***  
    设置本地线程收集缓冲区的初始化大小。
* ***-XX:+UseAdaptiveSizePolicy***  
    使用自适应分代大小。
* ***-XX:+UseConcMarkSweepGC***  
    使用cms垃圾回收器。
* ***-XX:+UseG1GC***  
    使用G1垃圾回收器
* ***-XX:+UseGCOverheadLimit***  
    限制GC的运行时间
* ***-XX:+UseParallelGC***  
    使用 Parallel收集器。
* ***-XX:+UseParallelOldGC***  
    使用 ParallelOld垃圾回收器。
* ***-XX:+UseParNewGC***  
    使用ParNew垃圾回收器
* ***-XX:+UseSerialGC***  
    使用 Serial垃圾回收器。
* ***-XX:+UseStringDeduplication***  
    使用字符串去重机制。
* ***-XX:+UseTLAB***  
    年轻代中使用本地线程收集块。



# 参数举例
```
-Xms4g -Xmx4g -XX:PermSize=512M
-XX:+UseG1GC 
-XX:ParallelGCThreads=20
-XX:InitiatingHeapOccupancyPercent=70
-XX:SurvivorRatio=6
-XX:+PrintGCDetails
-XX:+PrintGCDateStamps
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=dump_g1.hrpof
```
  
参考：

* [https://github.com/pzxwhc/MineKnowContainer/issues/25(https://github.com/pzxwhc/MineKnowContainer/issues/25)
* [http://blog.csdn.net/u011983531/article/details/63250882(http://blog.csdn.net/u011983531/article/details/63250882)
[https://www.jianshu.com/p/cd705f88cf2a](https://www.jianshu.com/p/cd705f88cf2a)
[G1总结](https://www.cnblogs.com/wgslucky/p/11764769.html)


