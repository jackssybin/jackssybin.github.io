title: 关于Mono和Flux的理解
date: '2020-06-18 17:49:51'
updated: '2020-10-18 20:29:41'
tags: [Mono, Flux, Reactor, WebFlux]
permalink: /articles/2020/06/18/1592473791199.html
---
![](https://b3logfile.com/bing/20200406.jpg?imageView2/1/w/960/h/540/interlace/1/q/100) 

# 关于java的响应式编程框架----SpringReactor

## 关于Reactor的介绍

Reactor是Spring中的一个子项目是一个基于java的响应式编程框架，此框架是 Pivotal 公司（开发 Spring 等技术的公司）开发的，实现了 Reactive Programming（反应式编程即响应式编程） 思想，符合 [Reactive Streams 规范](https://link.jianshu.com/?t=http%3A%2F%2Fwww.reactive-streams.org%2F)（Reactive Streams 是由 Netflix、TypeSafe、Pivotal 等公司发起的）的一项技术。其名字有反应堆之意，反映了其背后的强大的性能。

Spring 5 对应的Reactor框架的版本为3.1.0。（由于Spring5实现了很多关于函数式编程的东西，所以jdk版本至少得1.8）

## 关于反应式编程的思想：

反应式编程框架主要采用了观察者模式，而SpringReactor的核心则是对观察者模式的一种衍伸。关于观察者模式的架构中被观察者(Observable)和观察者(Subscriber)处在不同的线程环境中时，由于者各自的工作量不一样，导致它们产生事件和处理事件的速度不一样，这时就出现了两种情况：

1. 被观察者产生事件慢一些，观察者处理事件很快。那么观察者就会等着被观察者发送事件，（好比观察者在等米下锅，程序等待，这没有问题）。
2. 被观察者产生事件的速度很快，而观察者处理很慢。那就出问题了，如果不作处理的话，事件会堆积起来，最终挤爆你的内存，导致程序崩溃。（好比被观察者生产的大米没人吃，堆积最后就会烂掉）。**为了方便下面理解Mono和Flux，也可以理解为Publisher（发布者也可以理解为被观察者）主动推送数据给Subscriber（订阅者也可以叫观察者），如果Publisher发布消息太快，超过了Subscriber的处理速度，如何处理。这时就出现了Backpressure（背压-----指在异步场景中，被观察者发送事件速度远快于观察者的处理速度的情况下，一种告诉上游的被观察者降低发送速度的策略）**

## Reactor的主要类：

在Reactor中，经常使用的类并不多，主要有以下两个：

* Mono 实现了 org.reactivestreams.Publisher 接口，代表0到1个元素的发布者（Publisher）。
* Flux 同样实现了 org.reactivestreams.Publisher 接口，代表0到N个元素的发布者（Subscriber）。

可能会使用到的类：

Scheduler 表示背后驱动反应式流的调度器，通常由各种线程池实现。
![https://upload-images.jianshu.io/upload_images/3108769-5e2b4a9b14536578.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/700](https://www.pianshen.com/images/273/724c74f026bf742c882bb72b0bd58e61.png)
Spring5引入了一个基于Netty而不是Servlet高性能Web框架，但是使用方式和传统的基于Servlet的SrpingMvc并没有什么大的不同。

Web Flux中MVC接口的示例：

![](https://www.pianshen.com/images/800/6adc211aedfb4a2861ba70c231c7c8b0.png)

最大的变化就是返回值从 Foobar 所表示的一个对象变为 Mono<Foobar> （或 Flux<T>）。

# **关于Reactive Streams、Srping Reactor 和 Spring Flux（Web Flux）之间的关系**

**Reactive Streams ****是规范，Reactor 实现了 Reactive Streams。Web Flux 以 Reactor 为基础，实现 Web 领域的反应式编程框架**

# **关于Mono和Flux**

Mono和Flux都是Publisher（发布者）。

其实，对于大部分业务开发人员来说，当编写反应式代码时，我们通常只会接触到 `Publisher` 这个接口，对应到 Reactor 便是 `Mono` 和 `Flux`。对于 `Subscriber` 和 `Subcription` 这两个接口，Reactor 必然也有相应的实现。但是，这些都是 Web Flux 和 Spring Data Reactive 这样的框架用到的。如果不开发中间件，通常开发人员是不会接触到的。

比如，在 Web Flux，你的方法只需返回 Mono 或 Flux 即可。你的代码基本也只和 Mono 或 Flux 打交道。而 Web Flux 则会实现 Subscriber ，onNext 时将业务开发人员编写的 Mono 或 Flux 转换为 HTTP Response 返回给客户端。

# **案例**

Mono 实现了 Publisher 接口，但是通过查看源码，发现它是一个抽象类。Mono 里面有很多 API，关于这些 API 的解释如下：

* empty()：创建一个不包含任何元素，只发布结束消息的序列。
* just()：可以指定序列中包含的全部元素。创建出来的 Mono序列在发布这些元素之后会自动结束。
* justOrEmpty()：从一个 Optional 对象或可能为 null 的对象中创建 Mono。只有 Optional 对象中包含值或对象不为 null 时，Mono 序列才产生对应的元素。
* error(Throwable error)：创建一个只包含错误消息的序列。
* never()：创建一个不包含任何消息通知的序列。
* fromCallable()、fromCompletionStage()、fromFuture()、fromRunnable()和 fromSupplier()：分别从 Callable、CompletionStage、CompletableFuture、Runnable 和 Supplier 中创建 Mono。
* delay(Duration duration)和 delayMillis(long duration)：创建一个 Mono 序列，在指定的延迟时间之后，产生数字 0 作为唯一值。
* create()：通过 create()方法来使用 MonoSink 来创建 Mono。

### API 使用案例如下所示。

```
//empty()：创建一个不包含任何元素，只发布结束消息的序列
Mono.empty().subscribe(System.out::println);
//just()：可以指定序列中包含的全部元素。创建出来的 Mono序列在发布这些元素之后会自动结束。
Mono.just("www.jackssybin.cn").subscribe(System.out::println);
//ustOrEmpty()：从一个 Optional 对象或可能为 null 的对象中创建 Mono。
//只有 Optional 对象中包含值或对象不为 null 时，Mono 序列才产生对应的元素。
Mono.justOrEmpty(null).subscribe(System.out::println);
Mono.justOrEmpty("jackssy").subscribe(System.out::println);
Mono.justOrEmpty(Optional.of("jackssy")).subscribe(System.out::println);
//error(Throwable error)：创建一个只包含错误消息的序列。
Mono.error(new RuntimeException("error")).subscribe(System.out::println, System.err::println);
//never()：创建一个不包含任何消息通知的序列。
Mono.never().subscribe(System.out::println);
//通过 create()方法来使用 MonoSink 来创建 Mono。
Mono.create(sink -> sink.success("jackssy")).subscribe(System.out::println);

//通过fromRunnable创建，并实现异常处理
Mono.fromRunnable(() -> {
    System.out.println("thread run");
    throw new RuntimeException("thread run error");
}).subscribe(System.out::println, System.err::println);
//通过fromCallable创建
Mono.fromCallable(() -> "callable run ").subscribe(System.out::println);
//通过fromSupplier创建
Mono.fromSupplier(() -> "create from supplier").subscribe(System.out::println);

//delay(Duration duration)和 delayMillis(long duration)：创建一个 Mono 序列，在指定的延迟时间之后，产生数字 0 作为唯一值。
long start = System.currentTimeMillis();
Disposable disposable = Mono.delay(Duration.ofSeconds(2)).subscribe(n -> {
    System.out.println("生产数据源："+ n);
    System.out.println("当前线程ID："+ Thread.currentThread().getId() + ",生产到消费耗时："+ (System.currentTimeMillis() - start));
});
System.out.println("主线程"+ Thread.currentThread().getId() + "耗时："+ (System.currentTimeMillis() - start));
while(!disposable.isDisposed()) { }//empty()：创建一个不包含任何元素，只发布结束消息的序列
Mono.empty().subscribe(System.out::println);
//just()：可以指定序列中包含的全部元素。创建出来的 Mono序列在发布这些元素之后会自动结束。
Mono.just("www.xttblog.com").subscribe(System.out::println);
//ustOrEmpty()：从一个 Optional 对象或可能为 null 的对象中创建 Mono。
//只有 Optional 对象中包含值或对象不为 null 时，Mono 序列才产生对应的元素。
Mono.justOrEmpty(null).subscribe(System.out::println);
Mono.justOrEmpty("jackssy").subscribe(System.out::println);
Mono.justOrEmpty(Optional.of("jackssy")).subscribe(System.out::println);
//error(Throwable error)：创建一个只包含错误消息的序列。
Mono.error(new RuntimeException("error")).subscribe(System.out::println, System.err::println);
//never()：创建一个不包含任何消息通知的序列。
Mono.never().subscribe(System.out::println);
//通过 create()方法来使用 MonoSink 来创建 Mono。
Mono.create(sink -> sink.success("jackssy")).subscribe(System.out::println);

//通过fromRunnable创建，并实现异常处理
Mono.fromRunnable(() -> {
    System.out.println("thread run");
    throw new RuntimeException("thread run error");
}).subscribe(System.out::println, System.err::println);
//通过fromCallable创建
Mono.fromCallable(() -> "callable run ").subscribe(System.out::println);
//通过fromSupplier创建
Mono.fromSupplier(() -> "create from supplier").subscribe(System.out::println);

//delay(Duration duration)和 delayMillis(long duration)：创建一个 Mono 序列，在指定的延迟时间之后，产生数字 0 作为唯一值。
long start = System.currentTimeMillis();
Disposable disposable = Mono.delay(Duration.ofSeconds(2)).subscribe(n -> {
    System.out.println("生产数据源："+ n);
    System.out.println("当前线程ID："+ Thread.currentThread().getId() + ",生产到消费耗时："+ (System.currentTimeMillis() - start));
});
System.out.println("主线程"+ Thread.currentThread().getId() + "耗时："+ (System.currentTimeMillis() - start));
while(!disposable.isDisposed()) { }
```

## 用 just 创建数据流

```
Flux.just(520, 996, 997, 1024, 250, 888);
Mono.just(996);
```

## 基于数组创建数据流

```
Integer[] array = new Integer[]{520, 996, 997, 1024, 250, 888};
Flux.fromArray(array);
```

## 基于集合创建数据流

```
Integer[] array = new Integer[]{520, 996, 997, 1024, 250, 888};
List<Integer> list = Arrays.asList(array);
Flux.fromIterable(list);
```

## 基于 Stream 创建数据流

```
Integer[] array = new Integer[]{1, 2, 3, 4, 5, 6};
List<Integer> list = Arrays.asList(array);
Stream<Integer> stream = list.stream();
Flux.fromStream(stream);
```

## Flux 和 Mono 的数据信号

Flux 和 Mono 都可以发出三种数据信号，上文中提到元素值、错误信号和完成信号三者并不是要完全具备的，下面就给出几种情况：

```
// 只有完成信号的空数据流
Flux.just();
Flux.empty();
Mono.empty();
Mono.justOrEmpty(Optional.empty());

// 只有错误信号的数据流
Flux.error(new Exception("some error"));
Mono.error(new Exception("some error"));
```

