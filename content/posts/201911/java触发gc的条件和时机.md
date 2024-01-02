title: java触发gc的条件和时机
date: '2019-11-22 10:18:33'
updated: '2019-11-22 10:18:33'
tags: [jvm, java, 垃圾回收算法]
permalink: /articles/2019/11/22/1574389113537.html
---
**1.什么时候触发GC**

       (1)程序调用System.gc时可以触发，也不是立即触发，只是发了个通知要触发，时机由jvm自己把握

       (2)系统自身来决定GC触发的时机（根据Eden区和From Space区的内存大小来决定。当内存大小不足时，则会启动GC线程并停止应用线程）

      GC又分为 minor GC 和 Full GC (也称为 Major GC )

      Minor GC触发条件：**当Eden区满时**，触发Minor GC。

      Full GC触发条件：

  a.调用**System.gc时**，系统建议执行Full GC，但是不必然执行

  b.**老年代空间不足**

  c.**方法区空间不足**

  d.通过Minor GC后进入老年代的平均大小大于老年代的可用内存

  e.由Eden区、From Space区向To Space区复制时，对象大小大于To Space可用内存，则把该对象转存到老年代，且老年代的可用内存小于该对象大小

*     Minor GC：

    新生代GC，指发生在新生代的垃圾收集动作，因为Java对象大多都具备朝生熄灭的特点，所以Minor GC十分频繁，回收速度也较快。

*     Major GC：
    老年代GC，指发生在老年代的垃圾收集动作，当出现Major GC时，一般也会伴有至少一次的Minor GC（并非绝对，例如Parallel Scavenge收集器会单独直接触发Major GC的机制）。Major GC的速度一般会比Minor GC慢十倍以上。

*     对象优先在Eden区分配:
    HotSpot JVM把年轻代分为了三部分：1个Eden区和2个Survivor区（分别叫from和to）。默认比例为8：1。大多数情况下，对象优先在Eden区中分配。当Eden区中没有足够空间进行分配时，将会触发一次Minor GC。

*     大对象直接进入老年代：
    所谓的大对象是指，需要大量连续内存空间的Java对象。例如：很长的字符串或者数组。虚拟机提供了一个-XX：PretenureSizeThreshold参数。令大于这个-XX：PretenureSizeThreshold设置值的对象，直接在老年代分配。

*     长期存活的对象将进入老年代：
    虚拟机为了分代收集，对每一个对象定义了一个对象年龄计数器（Age）。如果对象在Eden出生，并且经过一次Minor GC后，仍然存活并且能被Survivor区中每熬过一次Minor GC，年龄就会增加1岁。当年龄增加到默认的15岁时，就会晋升到老年代。

    晋升为老年代的阙值通过参数-XX：MaxTenuringThreshold设置。

*     Full GC的情况：

（1）调用Sytem.GC()

（2）老年代空间不足时

（3）GC担保失败：

    在发生Minor GC之前，JVM会检查老年代最大可用的连续空间是否大于新生代所有对象总空间。如果条件成立，那么Minor GC是安全的。反之，如果不成立，那么要仍然要看HandlePromotionFailure值，是否允许担保失败。如果允许担保失败，那么会继续检查老年代最大可用的连续空间是否大于历次晋升到老年代对象的平均大小。如果大于，则冒险尝试一次Minor GC，如果小于或者不允许担保失败，则要进行一次Full GC。

**2.GC做了什么事**

         主要做了清理对象，整理内存的工作。Java堆分为新生代和老年代，采用了不同的回收方式。