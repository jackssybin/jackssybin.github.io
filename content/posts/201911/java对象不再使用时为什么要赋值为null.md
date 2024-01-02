title: java对象不再使用时，为什么要赋值为 null
date: '2019-11-19 14:59:17'
updated: '2019-11-19 14:59:17'
tags: [jvm, java, 垃圾回收算法]
permalink: /articles/2019/11/19/1574146757419.html
---
#### 1.示例代码
我们来看看一段非常简单的代码：
jvm配置参数：
```
-verbose:gc -XX:+PrintGC 
```

```
public static void main(String[] args) {  
if (true) {  
	byte[] placeHolder = new byte[64 * 1024 * 1024];  
	System.out.println(placeHolder.length / 1024);  
}  
	System.gc();  
}
```
我们在if中实例化了一个数组placeHolder，然后在if的作用域外通过System.gc();手动触发了GC，其用意是回收placeHolder，因为placeHolder已经无法访问到了。来看看输出：
```
65536
[GC (System.gc())  73404K->67241K(251392K), 0.0013637 secs]
[Full GC (System.gc())  67241K->67073K(251392K), 0.0064233 secs]
```
本次GC后，内存占用从67241K降到了67073K。意思其实是说GC没有将placeHolder回收掉
，如果把不使用的对象 置为null之后。如下
```
public static void main(String[] args) {  
if (true) {  
	byte[] placeHolder = new byte[64 * 1024 * 1024];  
	System.out.println(placeHolder.length / 1024);  
	placeHolder = null; //只有这句有变化
}  
	System.gc();  
}
```
输出结果：
```
65536
[GC (System.gc())  73404K->67166K(251392K), 0.0017978 secs]
[Full GC (System.gc())  67166K->1537K(251392K), 0.0069982 secs]
```
这次GC后内存占用下降到了1537K，即placeHolder被成功回收了！
对比两段代码，仅仅将placeHolder赋值为null就解决了GC的问题。神奇啊。确实。

#### 为什么呢？

**运行时栈（局部变量表）**
	
典型的运行时栈：
如果你了解过编译原理，或者程序执行的底层机制，你会知道方法在执行的时候，方法里的变量（局部变量）都是分配在栈上的；当然，对于Java来说，new出来的对象是在堆中，但栈中也会有这个对象的指针，和int一样。
比如对于下面这段代码
```
public static void main(String[] args) {  
	int a = 1;  
	int b = 2;  
	int c = a + b;  
}
```
其运行时栈的状态可以理解成：

| 索引（slot） |  变量 |
| --- |  --- |
| 1 |  a |
| 2 |  b |
| 3 |  c |
“索引”表示变量在栈中的序号，根据方法内代码执行的先后顺序，变量被按顺序放在栈中。
  
再比如：
```
public static void main(String[] args) {  
	if (true) {  
		int a = 1;  
		int b = 2;  
		int c = a + b;  
	}  
	int d = 4;  
}
```
这时运行时栈就是：

| 索引（slot） |  变量 |
| --- |  --- |
| 1 |  a |
| 2 |  b |
| 3 |  c |
| 4 |  d |

其实仔细想想上面这个例子的运行时栈是有优化空间的。

**Java的栈优化**
上面的例子，main()方法运行时占用了4个栈索引空间，但实际上不需要占用这么多。当if执行完后，变量a、b和c都不可能再访问到了，所以它们占用的1～3的栈索引是可以“回收”掉的，比如像这样：

| 索引 （slot）|  变量 |
| --- |  --- |
| 1 |  a |
| 2 |  b |
| 3 |  c |
| 1（3之前的被回收掉了） |  d |
变量d重用了变量a的栈索引，这样就节约了内存空间。
**提醒：**
上面的“运行时栈”和“索引”是为方便引入而故意发明的词，实际上在JVM中，它们的名字分别叫做“局部变量表”和“Slot”。而且局部变量表在编译时即已确定，不需要等到“运行时”。

**GC如何做的内存回收**
如何确定对象可以被回收？
如何确定对象是存活的？
**可达性分析算法：栈中引用的对象。也就是说，只要堆中的这个对象，在栈中还存在引用，就会被认定是存活的**。

**JVM的“bug”**
我们再来回头看看最开始的例子：
```
public class NullSample {
    public static void main(String[] args) {
        if (true) {
            byte[] placeHolder = new byte[64 * 1024 * 1024];
            System.out.println(placeHolder.length / 1024);
            placeHolder=null;
        }

        System.gc();
    }
}
``````
用javac 生成class文件，然后通过javap命令对字节码进行反汇编：
```
javac -g NullSample.java 
```
用javap反编译
```
javap -c -l NullSample.class
```
输出内容很长，我们只关心LocalVariableTable: 部分
```
   LocalVariableTable:
      Start  Length  Slot  Name   Signature
          5      14     1 placeHolder   [B
          0      23     0  args   [Ljava/lang/String;

```
栈中第一个索引是方法传入参数args，其类型为String[]；
第二个索引是placeHolder，其类型为byte[]。

联系前面的内容，我们推断placeHolder没有被回收的原因：System.gc();
**触发GC时，main()方法的运行时栈中，还存在有对args和placeHolder的引用，GC判断这两个对象都是存活的，不进行回收**。也就是说，代码在离开if后，虽然已经离开了placeHolder的作用域，***但在此之后，没有任何对运行时栈的读写***，placeHolder所在的索引还没有被其他变量重用，所以GC判断其为存活。

为了验证这一推断，我们在System.gc();之前再声明一个变量，按照之前提到的“Java的栈优化”，这个变量会重用placeHolder的索引。

```
public class NullSample {
    public static void main(String[] args) {
        if (true) {
            byte[] placeHolder = new byte[64 * 1024 * 1024];
            System.out.println(placeHolder.length / 1024);
        }
        int replacer = 1;
        System.gc();
    }
}

``````

看看其运行时栈：
```
  LocalVariableTable:
      Start  Length  Slot  Name   Signature
          0      23     0  args   [Ljava/lang/String;
          5      12     1 placeHolder   [B
         19       4     1 replacer   I
```
不出所料，replacer重用了placeHolder的索引。来看看GC情况：
```
65536
[GC (System.gc())  73404K->67230K(251392K), 0.0016969 secs]
[Full GC (System.gc())  67230K->1537K(251392K), 0.0071926 secs]
```
placeHolder被成功回收了！我们的推断也被验证了。

 
再从运行时栈来看，加上int replacer = 1;和将placeHolder赋值为null起到了同样的作用：断开堆中placeHolder和栈的联系，让GC判断placeHolder已经死亡。

 
现在算是理清了“不使用的对象应手动赋值为null“的原理了，一切根源都是来自于JVM的一个“bug”：**代码离开变量作用域时，并不会自动切断其与堆的联系**。为什么这个“bug”一直存在？你不觉得出现这种情况的概率太小了么？算是一个tradeoff了。
