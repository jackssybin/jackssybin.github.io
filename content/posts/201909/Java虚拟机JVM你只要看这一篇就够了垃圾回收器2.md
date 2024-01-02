title: Java虚拟机（JVM）你只要看这一篇就够了！垃圾回收器（2）
date: '2019-09-09 21:33:18'
updated: '2020-11-13 10:18:40'
tags: [待分类, java, 垃圾回收算法, jvm]
permalink: /articles/2019/09/17/1568733889287.html
---
![](https://b3logfile.com/bing/20180723.jpg?imageView2/1/w/960/h/540/interlace/1/q/100)

### 2.5 垃圾回收器

```
收集算法是内存回收的理论，而垃圾回收器是内存回收的实践。
```

![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvMTVmYjc1NDc2MmZmNWRmM2Y3ZjYzZTVjMjZkNGQzYWU_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)
说明：如果两个收集器之间存在连线说明他们之间可以搭配使用。
2.5.1 Serial 收集器

```
这是一个单线程收集器。意味着它只会使用一个 CPU 或一条收集线程去完成收集工作，并且在进行垃圾回收时必须暂停其它所有的工作线程直到收集结束。
```

![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvYjE4NDk0YjFlNTQ4NTFiYmJkMmVlNTI3NjBjYzM3NTQ_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)
2.5.2 ParNew 收集器

```
可以认为是 Serial 收集器的多线程版本。
```

![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvMTU0NjVmYjJlMTdjYjVkNjY1YzI1YmI5OGFjZmVhOTM_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)

并行：Parallel

```
指多条垃圾收集线程并行工作，此时用户线程处于等待状态
```

并发：Concurrent

```
指用户线程和垃圾回收线程同时执行(不一定是并行，有可能是交叉执行)，用户进程在运行，而垃圾回收线程在另一个 CPU 上运行。
```

2.5.3 Parallel Scavenge 收集器

```
这是一个新生代收集器，也是使用复制算法实现，同时也是并行的多线程收集器。
```

CMS 等收集器的关注点是尽可能地缩短垃圾收集时用户线程所停顿的时间，而 Parallel Scavenge 收集器的目的是达到一个可控制的吞吐量(Throughput = 运行用户代码时间 / (运行用户代码时间 + 垃圾收集时间))。

作为一个吞吐量优先的收集器，虚拟机会根据当前系统的运行情况收集性能监控信息，动态调整停顿时间。这就是 GC 的自适应调整策略(GC Ergonomics)。
2.5.4 Serial Old 收集器

```
收集器的老年代版本，单线程，使用 `标记 —— 整理`。
```

![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvYjE4NDk0YjFlNTQ4NTFiYmJkMmVlNTI3NjBjYzM3NTQ_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)

2.5.5 Parallel Old 收集器

```
Parallel Old 是 Parallel Scavenge 收集器的老年代版本。多线程，使用 `标记 —— 整理`
```

![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvMjU2NDEzNjZiNDNkOTcxMzEwYTBhN2NlZGU0ZTQwNmE_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)

2.5.6 CMS 收集器

```
CMS (Concurrent Mark Sweep) 收集器是一种以获取最短回收停顿时间为目标的收集器。基于 `标记 —— 清除` 算法实现。
```

运作步骤:

1. 初始标记(CMS initial mark)：标记 GC Roots 能直接关联到的对象
2. 并发标记(CMS concurrent mark)：进行 GC Roots Tracing
3. 重新标记(CMS remark)：修正并发标记期间的变动部分
4. 并发清除(CMS concurrent sweep)
   ![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvNmY0ZDY4MzY0NGExNTQ1MzdiM2UyM2Q2MGQ0OWMwNzQ_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)
   缺点：对 CPU 资源敏感、无法收集浮动垃圾、`标记 —— 清除` 算法带来的空间碎片
   2.5.7 G1 收集器

```
面向服务端的垃圾回收器。
```

优点：并行与并发、分代收集、空间整合、可预测停顿。
运作步骤:

1. 初始标记(Initial Marking)
2. 并发标记(Concurrent Marking)
3. 最终标记(Final Marking)
4. 筛选回收(Live Data Counting and Evacuation)
   ![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvNDBhNTc1OTMxYjI1NGE4ZjQwYmI1NDNjMjRlOGZhZGY_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)

### 2.6 内存分配与回收策略

2.6.1 对象优先在 Eden 分配

```
对象主要分配在新生代的 Eden 区上，如果启动了本地线程分配缓冲区，将线程优先在 (TLAB) 上分配。少数情况会直接分配在老年代中
```

一般来说 Java 堆的内存模型如下图所示：
![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvOTcxMDE4MDMxNWQzNTc1NmI2OGU5YzVkYWY0NGQ2ZTU_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)
新生代 GC (Minor GC)

```
发生在新生代的垃圾回收动作，频繁，速度快。
```

老年代 GC (Major GC / Full GC)

```
发生在老年代的垃圾回收动作，出现了 Major GC 经常会伴随至少一次 Minor GC(非绝对)。Major GC 的速度一般会比 Minor GC 慢十倍以上。
```

2.6.2 大对象直接进入老年代

2.6.3 长期存活的对象将进入老年代

2.6.4 动态对象年龄判定

2.6.5 空间分配担保

## 3. Java 内存模型与线程

![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvMjBhOTk2ODc0NmFmYTJhZmRlNGIzNzE2YmFiZjU1Y2U_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)

### 3.1 Java 内存模型

```
屏蔽掉各种硬件和操作系统的内存访问差异。
```

![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvOGY5ODMzMGRjOGFmNGNlOGNmNTM5N2EwMTMzMDhlYzI_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)
3.1.1 主内存和工作内存之间的交互
|操作	  |作用对象	|解释
|lock	        |主内存	  |把一个变量标识为一条线程独占的状态
|unlock |主内存	  |把一个处于锁定状态的变量释放出来，释放后才可被其他线程锁定
|read	  |主内存	  |把一个变量的值从主内存传输到线程工作内存中，以便 load 操作使用
|load	  |工作内存	|把 read 操作从主内存中得到的变量值放入工作内存中
|use    |工作内存	|把工作内存中一个变量的值传递给执行引擎，每当虚拟机遇到一个需要使用到变量值的字节码指令时将会执行这个操作
|assign |工作内存	|把一个从执行引擎接收到的值赋接收到的值赋给工作内存的变量，每当虚拟机遇到一个给变量赋值的字节码指令时执行这个操作
|store	|工作内存	|把工作内存中的一个变量的值传送到主内存中，以便 write 操作
|write	|工作内存	|把 store 操作从工作内存中得到的变量的值放入主内存的变量中

3.1.2 对于 volatile 型变量的特殊规则

```
关键字 volatile 是 Java 虚拟机提供的最轻量级的同步机制。
```

一个变量被定义为 volatile 的特性：
保证此变量对所有线程的可见性。但是操作并非原子操作，并发情况下不安全。

```
如果不符合 `运算结果并不依赖变量当前值，或者能够确保只有单一的线程修改变量的值` 和 `变量不需要与其他的状态变量共同参与不变约束` 就要通过加锁(使用 synchronize 或 java.util.concurrent 中的原子类)来保证原子性。
```

禁止指令重排序优化。

```
通过插入内存屏障保证一致性。
```

3.1.3 对于 long 和 double 型变量的特殊规则

```
Java 要求对于主内存和工作内存之间的八个操作都是原子性的，但是对于 64 位的数据类型，有一条宽松的规定：允许虚拟机将没有被 volatile 修饰的 64 位数据的读写操作划分为两次 32 位的操作来进行，即允许虚拟机实现选择可以不保证 64 位数据类型的 load、store、read 和 write 这 4 个操作的原子性。这就是 long 和 double 的非原子性协定。
```

3.1.4 原子性、可见性与有序性

```
回顾下并发下应该注意操作的那些特性是什么，同时加深理解。
```

* 原子性(Atomicity)

```
由 Java 内存模型来直接保证的原子性变量操作包括 read、load、assign、use、store 和 write。大致可以认为基本数据类型的操作是原子性的。同时 lock 和 unlock 可以保证更大范围操作的原子性。而 synchronize 同步块操作的原子性是用更高层次的字节码指令 monitorenter 和 monitorexit 来隐式操作的。
```

* 可见性(Visibility)

```
是指当一个线程修改了共享变量的值，其他线程也能够立即得知这个通知。主要操作细节就是修改值后将值同步至主内存(volatile 值使用前都会从主内存刷新)，除了 volatile 还有 synchronize 和 final 可以保证可见性。同步块的可见性是由“对一个变量执行 unlock 操作之前，必须先把此变量同步会主内存中( store、write 操作)”这条规则获得。而 final 可见性是指：被 final 修饰的字段在构造器中一旦完成，并且构造器没有把 “this” 的引用传递出去( this 引用逃逸是一件很危险的事情，其他线程有可能通过这个引用访问到“初始化了一半”的对象)，那在其他线程中就能看见 final 字段的值。
```

* 有序性(Ordering)

```
如果在被线程内观察，所有操作都是有序的；如果在一个线程中观察另一个线程，所有操作都是无序的。前半句指“线程内表现为串行的语义”，后半句是指“指令重排”现象和“工作内存与主内存同步延迟”现象。Java 语言通过 volatile 和 synchronize 两个关键字来保证线程之间操作的有序性。volatile 自身就禁止指令重排，而 synchronize 则是由“一个变量在同一时刻指允许一条线程对其进行 lock 操作”这条规则获得，这条规则决定了持有同一个锁的两个同步块只能串行的进入。
```

3.1.5 先行发生原则

```
也就是 happens-before 原则。这个原则是判断数据是否存在竞争、线程是否安全的主要依据。先行发生是 Java 内存模型中定义的两项操作之间的偏序关系。
```

天然的先行发生关系
![image.png](https://img.hacpai.com/file/2019/09/image-ec4dcdba.png)

### 3.2 Java 与线程

3.2.1 线程的实现
使用内核线程实现

```
直接由操作系统内核支持的线程，这种线程由内核完成切换。程序一般不会直接去使用内核线程，而是去使用内核线程的一种高级接口 —— 轻量级进程(LWP)，轻量级进程就是我们通常意义上所讲的线程，每个轻量级进程都有一个内核级线程支持。
```

![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvNGMwYTk1OTQ1ZTdjN2E1MmVmNmNjYmE0YWJiNzNkNDM_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)
使用用户线程实现

```
广义上来说，只要不是内核线程就可以认为是用户线程，因此可以认为轻量级进程也属于用户线程。狭义上说是完全建立在用户空间的线程库上的并且内核系统不可感知的。
```

![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvZDE1YjY5NDgyNTIyMTAxMDRkOWNjY2YxODJkYjU4MjU_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)
使用用户线程夹加轻量级进程混合实现
![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvZjE2MmMwYmUwMGU0NzI5NTIyZmNlNDhkMjA5ODk5MTM_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)

**Java 线程实现**

```
平台不同实现方式不同，可以认为是一条 Java 线程映射到一条轻量级进程。
```

3.2.2 Java 线程调度
协同式线程调度

```
线程执行时间由线程自身控制，实现简单，切换线程自己可知，所以基本没有线程同步问题。坏处是执行时间不可控，容易阻塞
```

抢占式线程调度

```
每个线程由系统来分配执行时间。
```

3.2.3 状态转换
五种状态：

* 新建(new)

```
创建后尚未启动的线程。
```

* 运行(Runable)

```
Runable 包括了操作系统线程状态中的 Running 和 Ready，也就是出于此状态的线程有可能正在执行，也有可能正在等待 CPU 为他分配时间。
```

* 无限期等待(Waiting)

```
出于这种状态的线程不会被 CPU 分配时间，它们要等其他线程显示的唤醒。
```

以下方法会然线程进入无限期等待状态：
1.没有设置 Timeout 参数的 Object.wait() 方法。
2.没有设置 Timeout 参数的 Thread.join() 方法。
3.LookSupport.park() 方法。

* 限期等待(Timed Waiting)

处于这种状态的线程也不会分配时间，不过无需等待配其他线程显示地唤醒，在一定时间后他们会由系统自动```
以下方法会让线程进入限期等待状态：
1.Thread.sleep() 方法。
2.设置了 Timeout 参数的 Object.wait() 方法。
3.设置了 Timeout 参数的 Thread.join() 方法。
4.LockSupport.parkNanos() 方法。
5.LockSupport.parkUntil() 方法。

* 阻塞(Blocked)

```
线程被阻塞了，“阻塞状态”和“等待状态”的区别是：“阻塞状态”在等待着获取一个排他锁，这个时间将在另外一个线程放弃这个锁的时候发生；而“等待状态”则是在等待一段时间，或者唤醒动作的发生。在程序等待进入同步区域的时候，线程将进入这种状态。
```

* 结束(Terminated)

```
已终止线程的线程状态。
```

![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvNmFmOGVlNThhNTU0YWYzMmFjOTI0NGQ2NDY5MjFiYzc_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)

## 5. 虚拟机类加载机制

```
虚拟机把描述类的数据从 Class 文件加载到内存，并对数据进行校验、装换解析和初始化，最终形成可以被虚拟机直接使用的 Java 类型
```

### 5.1 类加载时机

类的生命周期( 7 个阶段)
![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvMjdhYzg3ZjQzOTJmMGFiOTllNGM2NWMyM2NjNzE5NDU_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)
其中加载、验证、准备、初始化和卸载这五个阶段的顺序是确定的。解析阶段可以在初始化之后再开始(运行时绑定或动态绑定或晚期绑定)。

以下五种情况必须对类进行初始化(而加载、验证、准备自然需要在此之前完成)：

1. 遇到 new、getstatic、putstatic 或 invokestatic 这 4 条字节码指令时没初始化触发初始化。使用场景：使用 new 关键字实例化对象、读取一个类的静态字段(被 final 修饰、已在编译期把结果放入常量池的静态字段除外)、调用一个类的静态方法。
2. 使用 java.lang.reflect 包的方法对类进行反射调用的时候。
3. 初始化一个类的时候，如果发现其父类还没有进行初始化，则需先触发其父类的初始化。
4. 当虚拟机启动时，用户需指定一个要加载的主类(包含 main() 方法的那个类)，虚拟机会先初始化这个主类。
5. 当使用 JDK 1.7 的动态语言支持时，如果一个 java.lang.invoke.MethodHandle 实例最后的解析结果 REF_getStatic、REF_putStatic、REF_invokeStatic 的方法句柄，并且这个方法句柄所对应的类没有进行过初始化，则需先触发其初始化。
   前面的五种方式是对一个类的主动引用，除此之外，所有引用类的方法都不会触发初始化，佳作被动引用。举几个例子~

```
public class SuperClass {
    static {
        System.out.println("SuperClass init!");
    }
    public static int value = 1127;
}
 
public class SubClass extends SuperClass {
    static {
        System.out.println("SubClass init!");
    }
}
 
public class ConstClass {
    static {
        System.out.println("ConstClass init!");
    }
    public static final String HELLOWORLD = "hello world!"
}
 
public class NotInitialization {
    public static void main(String[] args) {
        System.out.println(SubClass.value);
        /**
         *  output : SuperClass init!
         * 
         * 通过子类引用父类的静态对象不会导致子类的初始化
         * 只有直接定义这个字段的类才会被初始化
         */
 
        SuperClass[] sca = new SuperClass[10];
        /**
         *  output : 
         * 
         * 通过数组定义来引用类不会触发此类的初始化
         * 虚拟机在运行时动态创建了一个数组类
         */
 
        System.out.println(ConstClass.HELLOWORLD);
        /**
         *  output : 
         * 
         * 常量在编译阶段会存入调用类的常量池当中，本质上并没有直接引用到定义类常量的类，
         * 因此不会触发定义常量的类的初始化。
         * “hello world” 在编译期常量传播优化时已经存储到 NotInitialization 常量池中了。
         */
    }
}
```

5.2 类的加载过程
5.2.1 加载

1. 通过一个类的全限定名来获取定义次类的二进制流(ZIP 包、网络、运算生成、JSP 生成、数据库读取)。
2. 将这个字节流所代表的静态存储结构转化为方法区的运行时数据结构。
3. 在内存中生成一个代表这个类的 java.lang.Class 对象，作为方法去这个类的各种数据的访问入口。

数组类的特殊性：数组类本身不通过类加载器创建，它是由 Java 虚拟机直接创建的。但数组类与类加载器仍然有很密切的关系，因为数组类的元素类型最终是要靠类加载器去创建的，数组创建过程如下：

1. 如果数组的组件类型是引用类型，那就递归采用类加载加载。
2. 如果数组的组件类型不是引用类型，Java 虚拟机会把数组标记为引导类加载器关联。
3. 数组类的可见性与他的组件类型的可见性一致，如果组件类型不是引用类型，那数组类的可见性将默认为 public。

内存中实例的 java.lang.Class 对象存在方法区中。作为程序访问方法区中这些类型数据的外部接口。
加载阶段与连接阶段的部分内容是交叉进行的，但是开始时间保持先后顺序。

5.2.2 验证

```
是连接的第一步，确保 Class 文件的字节流中包含的信息符合当前虚拟机要求。
```

文件格式验证

1. 是否以魔数 0xCAFEBABE 开头
2. 主、次版本号是否在当前虚拟机处理范围之内
3. 常量池的常量是否有不被支持常量的类型（检查常量 tag 标志）
4. 指向常量的各种索引值中是否有指向不存在的常量或不符合类型的常量
5. CONSTANT_Utf8_info 型的常量中是否有不符合 UTF8 编码的数据
6. Class 文件中各个部分集文件本身是否有被删除的附加的其他信息

只有通过这个阶段的验证后，字节流才会进入内存的方法区进行存储，所以后面 3 个验证阶段全部是基于方法区的存储结构进行的，不再直接操作字节流。

元数据验证

1. 这个类是否有父类（除 java.lang.Object 之外）
2. 这个类的父类是否继承了不允许被继承的类（final 修饰的类）
3. 如果这个类不是抽象类，是否实现了其父类或接口之中要求实现的所有方法
4. 类中的字段、方法是否与父类产生矛盾（覆盖父类 final 字段、出现不符合规范的重载）

这一阶段主要是对类的元数据信息进行语义校验，保证不存在不符合 Java 语言规范的元数据信息。

字节码验证

1. 保证任意时刻操作数栈的数据类型与指令代码序列都鞥配合工作（不会出现按照 long 类型读一个 int 型数据）
2. 保证跳转指令不会跳转到方法体以外的字节码指令上
3. 保证方法体中的类型转换是有效的（子类对象赋值给父类数据类型是安全的，反过来不合法的）

这是整个验证过程中最复杂的一个阶段，主要目的是通过数据流和控制流分析，确定程序语义是合法的、符合逻辑的。这个阶段对类的方法体进行校验分析，保证校验类的方法在运行时不会做出危害虚拟机安全的事件。

符号引用验证

1. 符号引用中通过字符创描述的全限定名是否能找到对应的类
2. 在指定类中是否存在符方法的字段描述符以及简单名称所描述的方法和字段
3. 符号引用中的类、字段、方法的访问性（private、protected、public、default）是否可被当前类访问

最后一个阶段的校验发生在迅疾将符号引用转化为直接引用的时候，这个转化动作将在连接的第三阶段——解析阶段中发生。符号引用验证可以看做是对类自身以外（常量池中的各种符号引用）的信息进行匹配性校验，还有以上提及的内容。
符号引用的目的是确保解析动作能正常执行，如果无法通过符号引用验证将抛出一个 java.lang.IncompatibleClass.ChangeError 异常的子类。如 java.lang.IllegalAccessError、java.lang.NoSuchFieldError、java.lang.NoSuchMethodError 等。

5.2.3 准备

```
这个阶段正式为类分配内存并设置类变量初始值，内存在方法去中分配(含 static 修饰的变量不含实例变量)。
```

public static int value = 1127;
这句代码在初始值设置之后为 0，因为这时候尚未开始执行任何 Java 方法。而把 value 赋值为 1127 的 putstatic 指令是程序被编译后，存放于 clinit() 方法中，所以初始化阶段才会对 value 进行赋值

基本数据类型的零值
![image.png](https://img.hacpai.com/file/2019/09/image-9cc98613.png)

特殊情况：如果类字段的字段属性表中存在 ConstantValue 属性，在准备阶段虚拟机就会根据 ConstantValue 的设置将 value 赋值为 1127。

5.2.4 解析

```
这个阶段是虚拟机将常量池内的符号引用替换为直接引用的过程。
```

1. 符号引用
   符号引用以一组符号来描述所引用的目标，符号可以使任何形式的字面量。
2. 直接引用
   直接引用可以使直接指向目标的指针、相对偏移量或是一个能间接定位到目标的句柄。直接引用和迅疾的内存布局实现有关

解析动作主要针对类或接口、字段、类方法、接口方法、方法类型、方法句柄和调用点限定符 7 类符号引用进行，分别对应于常量池的 7 中常量类型。

5.2.5 初始化

```
前面过程都是以虚拟机主导，而初始化阶段开始执行类中的 Java 代码。
```

5.3 类加载器

```
通过一个类的全限定名来获取描述此类的二进制字节流。
```

5.3.1 双亲委派模型

```
> 从 Java 虚拟机角度讲，只存在两种类加载器：一种是启动类加载器（C++ 实现，是虚拟机的一部分）；另一种是其他所有类的加载器（Java 实现，独立于虚拟机外部且全继承自 java.lang.ClassLoader）
```

1. 启动类加载器
   加载 lib 下或被 -Xbootclasspath 路径下的类
2. 扩展类加载器
   加载 lib/ext 或者被 java.ext.dirs 系统变量所指定的路径下的类
3. 引用程序类加载器
   ClassLoader负责，加载用户路径上所指定的类库。

![null](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAxNy85LzQvYzQyNzA0NzNjNDJjNGE1ZDE0ZWI0NzRjOGQ5NTcwZWI_aW1hZ2VWaWV3Mi8wL3cvMTI4MC9oLzk2MC9mb3JtYXQvd2VicC9pZ25vcmUtZXJyb3IvMQ)
除顶层启动类加载器之外，其他都有自己的父类加载器。
工作过程：如果一个类加载器收到一个类加载的请求，它首先不会自己加载，而是把这个请求委派给父类加载器。只有父类无法完成时子类才会尝试加载。

5.3.2 破坏双亲委派模

```
keyword：线程上下文加载器(Thread Context ClassLoader)
```

### 6.内存溢出场景：

场景1： 动态扩容引起的空间震荡
场景2： 显示GC的去与留
场景3： MetaSpace区OOM
场景4： 过早晋升
场景5： CMS old Gc 频繁
场景6： 单次CMS old Gc 耗时长
场景7： 内存碎片 &收集器退化
场景8： 对外内存OOM
场景9： JNI引发的GC问题

### 6.1具体原因

src/share/vm/gc/shared/gcCause.cpp 中。

```
const char* GCCause::to_string(GCCause::Cause cause) {
  switch (cause) {
    case _java_lang_system_gc:
      return "System.gc()";

    case _full_gc_alot:
      return "FullGCAlot";

    case _scavenge_alot:
      return "ScavengeAlot";

    case _allocation_profiler:
      return "Allocation Profiler";

    case _jvmti_force_gc:
      return "JvmtiEnv ForceGarbageCollection";

    case _gc_locker:
      return "GCLocker Initiated GC";

    case _heap_inspection:
      return "Heap Inspection Initiated GC";

    case _heap_dump:
      return "Heap Dump Initiated GC";

    case _wb_young_gc:
      return "WhiteBox Initiated Young GC";

    case _wb_conc_mark:
      return "WhiteBox Initiated Concurrent Mark";

    case _wb_full_gc:
      return "WhiteBox Initiated Full GC";

    case _no_gc:
      return "No GC";

    case _allocation_failure:
      return "Allocation Failure";

    case _tenured_generation_full:
      return "Tenured Generation Full";

    case _metadata_GC_threshold:
      return "Metadata GC Threshold";

    case _metadata_GC_clear_soft_refs:
      return "Metadata GC Clear Soft References";

    case _cms_generation_full:
      return "CMS Generation Full";

    case _cms_initial_mark:
      return "CMS Initial Mark";

    case _cms_final_remark:
      return "CMS Final Remark";

    case _cms_concurrent_mark:
      return "CMS Concurrent Mark";

    case _old_generation_expanded_on_last_scavenge:
      return "Old Generation Expanded On Last Scavenge";

    case _old_generation_too_full_to_scavenge:
      return "Old Generation Too Full To Scavenge";

    case _adaptive_size_policy:
      return "Ergonomics";

    case _g1_inc_collection_pause:
      return "G1 Evacuation Pause";

    case _g1_humongous_allocation:
      return "G1 Humongous Allocation";

    case _dcmd_gc_run:
      return "Diagnostic Command";

    case _last_gc_cause:
      return "ILLEGAL VALUE - last gc cause - ILLEGAL VALUE";

    default:
      return "unknown GCCause";
  }
  ShouldNotReachHere();
}
```

![e6e17aa22e4ab36fa857dd769042c24c.png](https://b3logfile.com/file/2020/11/e6e17aa22e4ab36fa857dd769042c24c-fb46497e.png)



参考：https://blog.csdn.net/luanlouis/article/details/39892027
参考：https://blog.csdn.net/qq_41701956/article/details/81664921

