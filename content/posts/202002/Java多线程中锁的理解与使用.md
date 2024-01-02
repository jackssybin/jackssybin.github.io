title: Java多线程中锁的理解与使用
date: '2020-02-19 01:22:31'
updated: '2020-02-19 01:22:31'
tags: [jvm锁, java锁, 锁, 独占锁]
permalink: /articles/2020/02/19/1582046551397.html
---
# 1.简介
锁作为并发共享数据，保证一致性的工具，在JAVA平台有多种实现(如 synchronized 和 ReentrantLock等 ) 。

# 2.Java锁的种类
* 公平锁/非公平锁
* 可重入锁
* 独享锁/共享锁
* 互斥锁/读写锁
* 乐观锁/悲观锁
* 分段锁
* 偏向锁/轻量级锁/重量级锁
* 自旋锁
上面是很多锁的名词，这些分类并不是全是指锁的状态，有的指锁的特性，有的指锁的设计，下面总结的内容是对每个锁的名词进行一定的解释。

**公平锁/非公平锁**

公平锁是指多个线程按照申请锁的顺序来获取锁。
非公平锁是指多个线程获取锁的顺序并不是按照申请锁的顺序，有可能后申请的线程比先申请的线程优先获取锁。有可能，会造成优先级反转或者饥饿现象。
对于Java ReentrantLock而言，通过构造函数指定该锁是否是公平锁，默认是非公平锁。非公平锁的优点在于吞吐量比公平锁大。
对于synchronized而言，也是一种非公平锁。由于其并不像ReentrantLock是通过AQS的来实现线程调度，所以并没有任何办法使其变成公平锁。

**可重入锁**

可重入锁又名递归锁，是指在同一个线程在外层方法获取锁的时候，在进入内层方法会自动获取锁。对于Java ReentrantLock而言, 其名字是Re entrant Lock即是重新进入锁。对于synchronized而言，也是一个可重入锁。可重入锁的一个好处是可一定程度避免死锁。
```
synchronized void setA() throws Exception{
    Thread.sleep(1000);
    setB();
}

synchronized void setB() throws Exception{
    Thread.sleep(1000);
}
```
上面的代码就是一个可重入锁的一个特点，如果不是可重入锁的话，setB可能不会被当前线程执行，可能造成死锁。

**独享锁/共享锁**

独享锁是指该锁一次只能被一个线程所持有；共享锁是指该锁可被多个线程所持有。

对于Java ReentrantLock而言，其是独享锁。但是对于Lock的另一个实现类ReadWriteLock，其读锁是共享锁，其写锁是独享锁。读锁的共享锁可保证并发读是非常高效的，读写、写读 、写写的过程是互斥的。独享锁与共享锁也是通过AQS来实现的，通过实现不同的方法，来实现独享或者共享。对于synchronized而言，当然是独享锁

**互斥锁/读写锁**

上面说到的独享锁/共享锁就是一种广义的说法，互斥锁/读写锁就是具体的实现。互斥锁在Java中的具体实现就是ReentrantLock；读写锁在Java中的具体实现就是ReadWriteLock。

**乐观锁/悲观锁**

乐观锁与悲观锁不是指具体的什么类型的锁，而是指看待并发同步的角度。

悲观锁：总是假设最坏的情况，每次去拿数据的时候都认为别人会修改，所以每次在拿数据的时候都会上锁，这样别人想拿这个数据就会阻塞直到它拿到锁。比如Java里面的同步原语synchronized关键字的实现就是悲观锁。

乐观锁：顾名思义，就是很乐观，每次去拿数据的时候都认为别人不会修改，所以不会上锁，但是在更新的时候会判断一下在此期间别人有没有去更新这个数据，可以使用版本号等机制。乐观锁适用于多读的应用类型，这样可以提高吞吐量，在Java中java.util.concurrent.atomic包下面的原子变量类就是使用了乐观锁的一种实现方式CAS(Compare and Swap 比较并交换)实现的。

**分段锁**

分段锁其实是一种锁的设计，并不是具体的一种锁，对于ConcurrentHashMap而言，其并发的实现就是通过分段锁的形式来实现高效的并发操作，ConcurrentHashMap中的分段锁称为Segment，它即类似于HashMap（JDK7与JDK8中HashMap的实现）的结构，即内部拥有一个Entry数组，数组中的每个元素又是一个链表；同时又是一个ReentrantLock（Segment继承了ReentrantLock)。当需要put元素的时候，并不是对整个HashMap进行加锁，而是先通过hashcode来知道他要放在那一个分段中，然后对这个分段进行加锁，所以当多线程put的时候，只要不是放在一个分段中，就实现了真正的并行的插入。但是，在统计size的时候，可就是获取HashMap全局信息的时候，就需要获取所有的分段锁才能统计。

分段锁的设计目的是细化锁的粒度，当操作不需要更新整个数组的时候，就仅仅针对数组中的一项进行加锁操作。

**偏向锁/轻量级锁/重量级锁**

这三种锁是指锁的状态，并且是针对synchronized。在Java 5通过引入锁升级的机制来实现高效synchronized。这三种锁的状态是通过对象监视器在对象头中的字段来表明的。

偏向锁是指一段同步代码一直被一个线程所访问，那么该线程会自动获取锁。降低获取锁的代价。

轻量级锁是指当锁是偏向锁的时候，被另一个线程所访问，偏向锁就会升级为轻量级锁，其他线程会通过自旋的形式尝试获取锁，不会阻塞，提高性能。

重量级锁是指当锁为轻量级锁的时候，另一个线程虽然是自旋，但自旋不会一直持续下去，当自旋一定次数的时候，还没有获取到锁，就会进入阻塞，该锁膨胀为重量级锁。重量级锁会让其他申请的线程进入阻塞，性能降低。

**自旋锁**

在Java中，自旋锁是指尝试获取锁的线程不会立即阻塞，而是采用循环的方式去尝试获取锁，这样的好处是减少线程上下文切换的消耗，缺点是循环会消耗CPU。

# 3.锁的使用
## 3.1 预备知识
### 3.1.1 AQS
AbstractQueuedSynchronized 抽象的队列式的同步器，AQS定义了一套多线程访问共享资源的同步器框架，许多同步类实现都依赖于它，如常用的ReentrantLock/Semaphore/CountDownLatch…
![null](http://images2015.cnblogs.com/blog/721070/201705/721070-20170504110246211-10684485.png)

AQS维护了一个volatile int state（代表共享资源）和一个FIFO线程等待队列（多线程争用资源被阻塞时会进入此队列）。state的访问方式有三种:
```
getState()  
setState() 
compareAndSetState()
```
AQS定义两种资源共享方式：Exclusive（独占，只有一个线程能执行，如ReentrantLock）和Share（共享，多个线程可同时执行，如Semaphore/CountDownLatch）。

不同的自定义同步器争用共享资源的方式也不同。自定义同步器在实现时只需要实现共享资源state的获取与释放方式即可，至于具体线程等待队列的维护（如获取资源失败入队/唤醒出队等），AQS已经在顶层实现好了。自定义同步器实现时主要实现以下几种方法：
```
isHeldExclusively()：该线程是否正在独占资源。只有用到condition才需要去实现它。
tryAcquire(int)：独占方式。尝试获取资源，成功则返回true，失败则返回false。
tryRelease(int)：独占方式。尝试释放资源，成功则返回true，失败则返回false。
tryAcquireShared(int)：共享方式。尝试获取资源。负数表示失败；0表示成功，但没有剩余可用资源；正数表示成功，且有剩余资源。
tryReleaseShared(int)：共享方式。尝试释放资源，如果释放后允许唤醒后续等待结点返回true，否则返回false
```
以ReentrantLock为例，state初始化为0，表示未锁定状态。A线程lock()时，会调用tryAcquire()独占该锁并将state+1。此后，其他线程再tryAcquire()时就会失败，直到A线程unlock()到state=0（即释放锁）为止，其它线程才有机会获取该锁。当然，释放锁之前，A线程自己是可以重复获取此锁的（state会累加），这就是可重入的概念。但要注意，获取多少次就要释放多么次，这样才能保证state是能回到零态的。

再以CountDownLatch以例，任务分为N个子线程去执行，state也初始化为N（注意N要与线程个数一致）。这N个子线程是并行执行的，每个子线程执行完后countDown()一次，state会CAS减1。等到所有子线程都执行完后(即state=0)，会unpark()主调用线程，然后主调用线程就会从await()函数返回，继续后余动作。

一般来说，自定义同步器要么是独占方法，要么是共享方式，他们也只需实现tryAcquire-tryRelease、tryAcquireShared-tryReleaseShared中的一种即可。但AQS也支持自定义同步器同时实现独占和共享两种方式，如ReentrantReadWriteLock。

## 3.2 CAS
CAS(Compare and Swap 比较并交换)是乐观锁技术，当多个线程尝试使用CAS同时更新同一个变量时，只有其中一个线程能更新变量的值，而其它线程都失败，失败的线程并不会被挂起，而是被告知这次竞争中失败，并可以再次尝试。　　　

CAS操作中包含三个操作数——需要读写的内存位置(V)、进行比较的预期原值(A)和拟写入的新值(B)。如果内存位置V的值与预期原值A相匹配，那么处理器会自动将该位置值更新为新值B，否则处理器不做任何操作。无论哪种情况，它都会在CAS 指令之前返回该位置的值（在CAS的一些特殊情况下将仅返回CAS是否成功，而不提取当前值）。CAS有效地说明了“ 我认为位置V应该包含值A；如果包含该值，则将 B放到这个位置；否则，不要更改该位置，只告诉我这个位置现在的值即可”。这其实和乐观锁的冲突检查 + 数据更新的原理是一样的。

JAVA对CAS的支持：

在JDK1.5中新增java.util.concurrent包就是建立在CAS之上的。相对于对于synchronized 这种阻塞算法，CAS是非阻塞算法的一种常见实现。所以java.util.concurrent在性能上有了很大的提升。

以java.util.concurrent包中的AtomicInteger为例，看一下在不使用锁的情况下是如何保证线程安全的。主要理解 getAndIncrement方法，该方法的作用相当于 ++i 操作。

```
public class AtomicInteger extends Number implements java.io.Serializable {  
    private volatile int value; 

    public final int get() {  
        return value;  
    }  

    public final int getAndIncrement() {  
        for (;;) {  
            int current = get();  
            int next = current + 1;  
            if (compareAndSet(current, next))  
                return current;  
        }  
    }  

    public final boolean compareAndSet(int expect, int update) {  
        return unsafe.compareAndSwapInt(this, valueOffset, expect, update);  
    }  
}
```
## 4.实战

### 4.1 synchronized

synchronized可重入锁验证
```
//import java.util.concurrent.locks.ReentrantLock;

public class Test implements Runnable{

    //private ReentrantLock reentrantLock = new ReentrantLock();

    public synchronized void get(){
        System.out.println("2 enter thread name-->" + Thread.currentThread().getName());
        //reentrantLock.lock();
        System.out.println("3 get thread name-->" + Thread.currentThread().getName());
        set();
        //reentrantLock.unlock();
        System.out.println("5 leave run thread name-->" + Thread.currentThread().getName());
    }

    public synchronized void set(){
        //reentrantLock.lock();
        System.out.println("4 set thread name-->" + Thread.currentThread().getName());
        //reentrantLock.unlock();
    }

    @Override
    public void run() {
        System.out.println("1 run thread name-->" + Thread.currentThread().getName());
        get();
    }

    public static void main(String[] args){
        Test test = new Test();
        for(int i = 0; i < 10; i++){
            new Thread(test, "thread-" + i).start();
        }
    }
}

```
结果
```
1 run thread name-->thread-0
1 run thread name-->thread-4
1 run thread name-->thread-1
1 run thread name-->thread-8
1 run thread name-->thread-5
2 enter thread name-->thread-0
1 run thread name-->thread-9
3 get thread name-->thread-0
1 run thread name-->thread-2
1 run thread name-->thread-3
4 set thread name-->thread-0
1 run thread name-->thread-6
5 leave run thread name-->thread-0
1 run thread name-->thread-7
2 enter thread name-->thread-6
3 get thread name-->thread-6
4 set thread name-->thread-6
5 leave run thread name-->thread-6
2 enter thread name-->thread-3
3 get thread name-->thread-3
4 set thread name-->thread-3
5 leave run thread name-->thread-3
2 enter thread name-->thread-2
3 get thread name-->thread-2
4 set thread name-->thread-2
5 leave run thread name-->thread-2
2 enter thread name-->thread-9
3 get thread name-->thread-9
4 set thread name-->thread-9
5 leave run thread name-->thread-9
2 enter thread name-->thread-5
3 get thread name-->thread-5
4 set thread name-->thread-5
5 leave run thread name-->thread-5
2 enter thread name-->thread-8
3 get thread name-->thread-8
4 set thread name-->thread-8
5 leave run thread name-->thread-8
2 enter thread name-->thread-1
3 get thread name-->thread-1
4 set thread name-->thread-1
5 leave run thread name-->thread-1
2 enter thread name-->thread-4
3 get thread name-->thread-4
4 set thread name-->thread-4
5 leave run thread name-->thread-4
2 enter thread name-->thread-7
3 get thread name-->thread-7
4 set thread name-->thread-7
5 leave run thread name-->thread-7

```
get()方法中顺利进入了set()方法，说明synchronized的确是可重入锁。分析打印Log，thread-0先进入get方法体，这个时候thread-3、thread-2、thread-1等待进入，但当thread-0离开时，thread-4却先进入了方法体，没有按照thread-3、thread-2、thread-1的顺序进入get方法体，说明sychronized的确是非公平锁。而且在一个线程进入get方法体后，其他线程只能等待，无法同时进入，验证了synchronized是独占锁。

### 4.2 ReentrantLock
ReentrantLock既可以构造公平锁又可以构造非公平锁，默认为非公平锁，将上面的代码改为用ReentrantLock实现，再次运行。
```
import java.util.concurrent.locks.ReentrantLock;

public class Test implements Runnable{

    private ReentrantLock reentrantLock = new ReentrantLock();

    public void get(){
        System.out.println("2 enter thread name-->" + Thread.currentThread().getName());
        reentrantLock.lock();
        System.out.println("3 get thread name-->" + Thread.currentThread().getName());
        set();
        reentrantLock.unlock();
        System.out.println("5 leave run thread name-->" + Thread.currentThread().getName());
    }

    public void set(){
        reentrantLock.lock();
        System.out.println("4 set thread name-->" + Thread.currentThread().getName());
        reentrantLock.unlock();
    }

    @Override
    public void run() {
        System.out.println("1 run thread name-->" + Thread.currentThread().getName());
        get();
    }

    public static void main(String[] args){
        Test test = new Test();
        for(int i = 0; i < 10; i++){
            new Thread(test, "thread-" + i).start();
        }
    }
}
```
结果:
```
1 run thread name-->thread-0
2 enter thread name-->thread-0
3 get thread name-->thread-0
4 set thread name-->thread-0
1 run thread name-->thread-1
2 enter thread name-->thread-1
1 run thread name-->thread-2
2 enter thread name-->thread-2
1 run thread name-->thread-3
2 enter thread name-->thread-3
5 leave run thread name-->thread-0
3 get thread name-->thread-2
4 set thread name-->thread-2
5 leave run thread name-->thread-2
3 get thread name-->thread-1
4 set thread name-->thread-1
5 leave run thread name-->thread-1
3 get thread name-->thread-3
4 set thread name-->thread-3
5 leave run thread name-->thread-3
1 run thread name-->thread-4
1 run thread name-->thread-5
2 enter thread name-->thread-5
3 get thread name-->thread-5
4 set thread name-->thread-5
5 leave run thread name-->thread-5
1 run thread name-->thread-6
2 enter thread name-->thread-6
3 get thread name-->thread-6
4 set thread name-->thread-6
5 leave run thread name-->thread-6
2 enter thread name-->thread-4
3 get thread name-->thread-4
4 set thread name-->thread-4
5 leave run thread name-->thread-4
1 run thread name-->thread-7
2 enter thread name-->thread-7
3 get thread name-->thread-7
4 set thread name-->thread-7
5 leave run thread name-->thread-7
1 run thread name-->thread-8
2 enter thread name-->thread-8
3 get thread name-->thread-8
4 set thread name-->thread-8
1 run thread name-->thread-9
2 enter thread name-->thread-9
3 get thread name-->thread-9
4 set thread name-->thread-9
5 leave run thread name-->thread-9
5 leave run thread name-->thread-8
```
的确如其名，可重入锁，当然默认的确是非公平锁。thread-0持有锁期间，thread-1、thread-2、thread-3等待拥有锁，当thread-0释放锁时thread-2先获取到锁，并非按照先后顺序获取锁的。

将其构造为公平锁，看看运行结果是否符合预期。查看源码构造公平锁很简单，只要在构造器传入boolean值true即可。

```
 /**
     * Creates an instance of {@code ReentrantLock} with the
     * given fairness policy.
     *
     * @param fair {@code true} if this lock should use a fair ordering policy
     */
    public ReentrantLock(boolean fair) {
        sync = fair ? new FairSync() : new NonfairSync();
    }
```
修改上面例程的代码构造方法为：
```
ReentrantLock reentrantLock = new ReentrantLock(true);
```
如果使用了IntelliJ IDEA IDE可以看到在true前面还有个fair提示。
```
import java.util.concurrent.locks.ReentrantLock;

public class Test implements Runnable{

    private ReentrantLock reentrantLock = new ReentrantLock(true);

    public void get(){
        System.out.println("2 enter thread name-->" + Thread.currentThread().getName());
        reentrantLock.lock();
        System.out.println("3 get thread name-->" + Thread.currentThread().getName());
        set();
        reentrantLock.unlock();
        System.out.println("5 leave run thread name-->" + Thread.currentThread().getName());
    }

    public void set(){
        reentrantLock.lock();
        System.out.println("4 set thread name-->" + Thread.currentThread().getName());
        reentrantLock.unlock();
    }

    @Override
    public void run() {
        System.out.println("1 run thread name-->" + Thread.currentThread().getName());
        get();
    }

    public static void main(String[] args){
        Test test = new Test();
        for(int i = 0; i < 10; i++){
            new Thread(test, "thread-" + i).start();
        }
    }
}
```
结果：
```
1 run thread name-->thread-1
1 run thread name-->thread-0
2 enter thread name-->thread-0
3 get thread name-->thread-0
4 set thread name-->thread-0
1 run thread name-->thread-2
5 leave run thread name-->thread-0
2 enter thread name-->thread-1
3 get thread name-->thread-1
4 set thread name-->thread-1
2 enter thread name-->thread-2
1 run thread name-->thread-3
5 leave run thread name-->thread-1
2 enter thread name-->thread-3
3 get thread name-->thread-2
4 set thread name-->thread-2
1 run thread name-->thread-7
2 enter thread name-->thread-7
1 run thread name-->thread-5
5 leave run thread name-->thread-2
2 enter thread name-->thread-5
3 get thread name-->thread-3
4 set thread name-->thread-3
5 leave run thread name-->thread-3
3 get thread name-->thread-7
4 set thread name-->thread-7
5 leave run thread name-->thread-7
3 get thread name-->thread-5
4 set thread name-->thread-5
5 leave run thread name-->thread-5
1 run thread name-->thread-8
2 enter thread name-->thread-8
3 get thread name-->thread-8
1 run thread name-->thread-9
2 enter thread name-->thread-9
4 set thread name-->thread-8
3 get thread name-->thread-9
4 set thread name-->thread-9
5 leave run thread name-->thread-9
5 leave run thread name-->thread-8
1 run thread name-->thread-4
2 enter thread name-->thread-4
3 get thread name-->thread-4
4 set thread name-->thread-4
5 leave run thread name-->thread-4
1 run thread name-->thread-6
2 enter thread name-->thread-6
3 get thread name-->thread-6
4 set thread name-->thread-6
5 leave run thread name-->thread-6

```
公平锁在多个线程想要同时获取锁的时候，会发现再排队，按照先来后到的顺序进行。

### 4.3 ReentrantReadWriteLock
读写锁的性能都会比排它锁要好，因为大多数场景读是多于写的。在读多于写的情况下，读写锁能够提供比排它锁更好的并发性和吞吐量。Java并发包提供读写锁的实现是ReentrantReadWriteLock。

| 特性 | 说明 | 
| --- | --- |
|公平性选择  |支持非公平(默认)和公平的锁获取方式，吞吐量还是非公平优于公平  |  
|重进入  |该锁支持重进入，以读写线程为例：读线程在获取了读锁之后，能够再次获取读锁。而写线程在获取了  写锁之后能够再次获取写锁，同时也可以获取读锁|  
| 锁降级 | 遵循获取写锁、获取读锁再释放写锁的次序，写锁能够降级成为读锁 |
	
	
```
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class Test {

    public static void main(String[] args){
        for(int i = 0; i < 10; i++){
            new Thread(new Runnable() {

                @Override
                public void run() {
                    Cache.put("key", new String(Thread.currentThread().getName() + " joke"));
                }
            }, "threadW-"+ i).start();
            new Thread(new Runnable() {

                @Override
                public void run() {
                    System.out.println(Cache.get("key"));
                }
            }, "threadR-"+ i).start();
            new Thread(new Runnable() {

                @Override
                public void run() {
                    Cache.clear();
                }
            }, "threadC-"+ i).start();
        }

    }
}

class Cache {
    static Map<String, Object> map = new HashMap<String, Object>();
    static ReentrantReadWriteLock rwl = new ReentrantReadWriteLock();
    static Lock r = rwl.readLock();
    static Lock w = rwl.writeLock();
    // 获取一个key对应的value
    public static final Object get(String key) {
        r.lock();
        try {
            System.out.println("get " + Thread.currentThread().getName());
            return map.get(key);
        } finally {
            r.unlock();
        }
    }
    // 设置key对应的value，并返回旧有的value
    public static final Object put(String key, Object value) {
        w.lock();
        try {
            System.out.println("put " + Thread.currentThread().getName());
            return map.put(key, value);
        } finally {
            w.unlock();
        }
    }
    // 清空所有的内容
    public static final void clear() {
        w.lock();
        try {
            System.out.println("clear " + Thread.currentThread().getName());
            map.clear();
        } finally {
            w.unlock();
        }
    }
}
```	
运行结果
```
clear threadC-0
get threadR-2
null
put threadW-2
get threadR-0
threadW-2 joke
get threadR-3
threadW-2 joke
clear threadC-1
put threadW-3
clear threadC-3
clear threadC-2
get threadR-1
null
put threadW-1
put threadW-0
put threadW-4
get threadR-4
threadW-4 joke
clear threadC-4
get threadR-5
null
put threadW-5
put threadW-6
get threadR-6
threadW-6 joke
get threadR-7
threadW-6 joke
put threadW-7
clear threadC-6
put threadW-8
get threadR-8
threadW-8 joke
clear threadC-8
get threadR-9
null
clear threadC-5
clear threadC-9
clear threadC-7
put threadW-9

```
可看到普通HashMap在多线程中数据可见性正常。


链接:[https://blog.csdn.net/tyyj90/article/details/78236053](https://blog.csdn.net/tyyj90/article/details/78236053)	


