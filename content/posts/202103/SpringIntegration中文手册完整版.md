title: Spring Integration 中文手册（完整版）
date: '2021-03-16 20:30:40'
updated: '2021-03-16 20:34:04'
tags: [rabbitmq, activemq, springBatch]
permalink: /articles/2021/03/16/1615897840354.html
---
![](https://b3logfile.com/bing/20180721.jpg?imageView2/1/w/960/h/540/interlace/1/q/100)

# 1. Spring Integration 中文手册

*Spring Integration 对 Spring 编程模型进行了扩展，使得后者能够支持著名的“[企业集成模式](https://www.oschina.net/action/GoToLink?url=http%3A%2F%2Fwww.eaipatterns.com%2F)”。通过SI（Spring Integration）可以在基于Spring的应用中引入轻量级的“消息驱动模式”，并且支持“通过声明式的适配器”与外部系统进行集成。这些“适配器”相较于Spring对于“remoting（远程调用）”、“messaging（事件消息）”、“scheduling（任务调度）”方面的支持，提供了更高层次的一种抽象。SI的首要目标是：为“构建企业集成方案、维护系统间通信”提供一种**简单模型**，应用该模型所产出的代码是**可维护、可测试的**。*

# 2. Spring Integration 概览

## 2.1 背景

IoC——“控制反转”，是Spring Framework的一个关键特性。这种IoC，从广义上来说，意味着Spring Framework将负责代表被其上下文所管理的各种组件，而组件本身却由于被减轻了部分职责而简单化了。例如：“依赖注入”使得组件摆脱了定位与创建自身依赖的职责。再比如：“面向切面编程”则通过可复用切面的透明织入，使得业务与横切交叉点解耦，使得业务组件避免了被普遍的耦合横切，做到了更好的模块化。在上述各种情况下，最终结果都是：系统更容易被测试、理解、维护和扩展。

此外，Spring Framework及相关工具包为构建企业应用提供了一个无所不包的编程模型。开发者受益于这个模型的一致性。尤其是该模型以公认的最佳实践为基础，使得开发者受益匪浅，比如“面向接口编程”，“尽量使用聚合而不是继承”等等。来自Spring的简化抽象与强大类库，不仅增强了系统的可测试性和可移植性，同时也大大提高了开发者的生产力。

Spring Integration秉承了与前文所述相同的目标和原则。它将Spring的编程模型拓展到了消息领域，在Spring现有的企业集成支持基础上构建了更高次的抽象。在它所支持的消息驱动架构中，“控制反转”被应用于运行期的关键连接处，例如：在何时特定的业务逻辑应该执行，以及响应结果应该被发送到何处。它提供了消息路由和消息转换方面的支持，所以不同的传输协议和不同的数据格式都能在不影响易测试性的前提下被集成。换句话说，消息和集成点都被框架所处理，所以业务组件能很好地与基础设施隔离，从而使得开发者能够从复杂的集成工作中解脱出来。

作为Spring编程模型的扩展，Spring Integration提供了多种配置方式可供选择，包括注解、基于命名空间的XML、通用Bean元素的XML，当然也可以直接使用底层API。底层的API都均是基于“精心定义的策略接口”与“保证了非侵入性的代理适配器”。Spring Integration的设计启发于“Spring中的普遍模式”与“企业集成模式”间强烈的共鸣。“企业集成模式”是由Gregor Hohpe和Bobby Woolf在《企业集成模式》一书中提出的，该书由Addison Wesley出版社于2004年出版。读过此书的开发者应该能更快地适应Spring Integration的概念和术语。

## 2.2 目标与原则

Spring Integration 面向如下目标：

* 提供一个简单的模型来实现复杂的企业集成解决方案
* 为基于Spring的应用提供异步、消息驱动方面的基础支持
* 让现有的Spring用户可以更容易、直观的掌握，并让更多的用户去使用

Spring Integration 遵循以下原则：

* 组件间应该是模块化、松耦合的，且可测试的
* 框架应该保证分离“业务逻辑”和“集成逻辑”
* 扩展点本质上应该是抽象的，而且限定在一个清晰的边界内，进而提升可复用性和可移植性

## 2.3 主要组件

从垂直的视角来看，“分层架构”会更有利于关键点的剥离，各层间通过基于接口的契约来确保松耦合。基于Spring的应用就是如此设计的典型。Spring Framework与相关工具包从全栈范围为企业应用提供了一个遵从最佳实践强大基础。“消息驱动架构”则为我们带来了一个“横向的视角”。正如“分层架构”是一种极通用、极抽象的范式一样，消息系统非常符合同样抽象的“管道-过滤器”模型。“过滤器”代表任何能够产出和（或）消费消息的组件。“管道”则负责在过滤器间传输消息。所以在管道的作用下，各“过滤器”组件间保持松耦合。有必要指出的是，这两个高级范式（分层架构与消息驱动架构）并非互斥。支持“管道”的消息基础设施应当被封装在相应的垂直“层”中，且该层对外的契约被定义为接口。同样地，“过滤器”往往被安排于“应用服务层”之上的（业务）层中进行管理，并且与底层服务的交互方式与它类无异。

### 2.3.1 消息

在Spring Integration中，“消息”是对任何Java对象的一种通用包装，这种包装将会给Java对象附着一些元信息以供消息框架处理。一条“消息”由“消息体”（payload）和“消息头”（header）组成。消息体可以是任何类型，消息头一般用于保存一些必要信息，比如id、时间戳、过期时间和返回地址等。消息头也可以用来在不同的传输协议之间传递参数。比如，当需要包装一个文件来创建一个消息时，可以将文件名保存于消息头中，以供下游的消息组件读取使用。再比如，如果一个消息的内容会最终被Mail适配器发出，那么各种属性值（to、from、cc、subject等）可被上游的消息组件保存在消息头中。开发者可以利用消息头来保存任意的键值对。

![消息结构示意图](http://static.oschina.net/uploads/space/2015/0322/223850_R9Qy_2321188.jpg)

### 2.3.2 消息通道

“消息通道”对应着“管道-过滤器”架构中的“管道角色”。消息生产者发送消息到通道，消息消费者从通道接收消息。从而，消息通道解耦了消息组件，同时也为消息拦截和监控提供了便利的切入点。

![消息通道图](http://static.oschina.net/uploads/space/2015/0322/223916_9OKQ_2321188.jpg)

一个消息通道可以是“点对点”意义的，或者也可以是“发布-订阅”意义的。

* 如果是点对点模式的通道，发布到通道中的每个消息，最多只有一个消费者可以接收。
* 如果是发布-订阅模式的通道，则会尝试广播消息给其所有的订阅者。

Spring Integration对这两种模式均提供支持。

鉴于“点对点模式”和“发布订阅模式”提供了两种关于“最终有多少消息消费者接收消息”的选择，此处还有另外一项重要考虑：通道是否应该缓存消息？在Spring Integration中，轮询通道（Pollable Channels）具备缓存消息能力。缓存的优势在于它能够调节接入消息流量，从而避免消息消费者负荷过载。然而，正如其名称所示，这也会引入了一些复杂性，只有配置了轮询器后，消息消费者才能从这个通道中接收消息。而另一方面，订阅通道（Subscribable Channel）要求连接它的消费者依从简单的消息驱动模式。Spring Integration中还有多种通道的可用实现，将在第3.2章节“消息通道实现”中详细讨论。

### 2.3.2 消息终端

Spring Integration的主要目标之一是通过“控制反转”来简化企业集成解决方案的开发。这意味着你应该不需要直接实现消息消费者和生产者，更不需要构建消息或者在消息通道上调用发送与接收操作。相反地，你只需要关注于你基于普通对象（POJO）实现的特定领域模型。然后，通过声明式配置，你可以“连接”业务领域代码到Spring Integration提供的消息基础设施。而负责这些连接的组件就是“消息终端”。这并不是说你必须直接性地连接现有应用。任何真实的企业集成解决方案，都需要一些用于集成相关的逻辑代码，例如路由选择和协议转换。其中暗含的要点就是：实现集成逻辑和业务逻辑的分离。类比来说，作为Web应用中的MVC模式，其目标应该是提供一个简单而专用的层，转换接入的请求到服务层调用，然后再转换服务层响应到请求端。下一节将概述处理这些响应的各种消息终端类型，且在以后的章节中，将为你展示如何使用Spring Integration的声明式配置来保证非侵入性的效果。

## 2.4 各种消息终端简介

“消息终端”对应着“管道-过滤器”架构中的“过滤器”角色。就像前文提到的，消息终端的的主要作用在于“连接”业务领域代码到Spring Integration提供的消息基础设施，当然前提是使用非侵入的方式。换句话说，应用代码应该完全不会知晓消息对象或者消息通道的存在。这类似于MVC模式中控制器角色的处理范式，例如：

* “消息端点处理消息”就像“控制器处理HTTP请求”。
* "消息终端被映射到消息通道"就像“控制器被映射到URL Pattern”

上述两个例子中存在相同的目标：隔离“业务应用代码”与“基础设置”。《企业应用集成》一书中详细地讨论了这其中涉及的各种概念与模式。本文只概括地描述Spring Integration支持的主要消息终端类型和作用。本章节内的详细描述将提供代码与配置样例。

### 2.4.1 转换器（Transformer）

“消息转换器”的作用在于“转换消息的内容或结构，返回翻转换后的消息”。可能最为常见的转换器应用方式就是将消息体（Message Payload）从一种格式转换为另一种格式（例如从XML文档转换成java.lang.String字符串）。同样地，转换器也可以被用于添加、删除和修改消息头（Message Header）中的值。

### 2.4.2 过滤器（Filter）

“消息过滤器”可用来限定消息能否被传送到输出通道上。这里仅需要依据一个布尔测试来做判定。该布尔测试检查的范围诸如：“消息是否包含特定类型的消息体”，“检查消息中的某个属性值”，“消息是否包含某个消息头”，等等。如果消息通过检查就会被发送到输出通道，否则，消息将被丢弃（或者更加严格地说，应当抛出异常）。消息过滤器通常结合“发布-订阅通道”一起使用，“发布-订阅通道”会使得多个消费者接收到同样的消息，而基于一定的过滤条件设置过滤器则可以减少所需处理的消息数量。

> 注意：前段提到的“消息过滤器”与“管道-过滤器”架构中的‘过滤器’并非一致的概念。“消息过滤器”是指限制消息通过的消息处理装置，而“管道-过滤器”中的‘过滤器’是泛指所有处理消息的消息处理装置。

### 2.4.3 路由器（Router）

“消息路由器”负责确定消息的下一步传送将由哪些通道接收。通常，路由决策都是基于消息内容和（或）消息头中可用的元数据来完成的。消息路由常常代替静态的配置，作为一种动态地、运行时确定输出通道的装置，接入到“服务激活器”或者其他能够响应消息的装置。另外，针对前文所述的消息多播的场景，相对于被动的“消息过滤器”，“消息路由器”提供了一种主动的控制方式，来确定多个消息订阅者中的消息接收范围。

![消息路由器示意图](http://static.oschina.net/uploads/space/2015/0323/172825_iYGd_2321188.jpg)

### 2.4.4 消息分解器（Splitter）

“消息分解器”是另外一种类型的消息终端，它从对应输入通道中接收消息，然后把接收到的一个消息分解成多个消息，最终把它们发送到对应输出通道上。典型应用场景就是把一个“复合消息”分解成包含原消息各子部分的一组“子消息”。

### 2.4.5 消息聚合器（Aggregator）

“消息聚合器”基本上就是“消息分解器”的反模式。它也是一种消息终端类型，接收多条消息，然后把他们合并成一条消息。事实上，聚合器通常出现在消息管道线路中的下游位置，且相对该组件的上游位置往往会存在“消息分解器”。从技术上来说，聚合器往往比分解器更复杂，因为它需要维护状态（也就是维护正被聚合的消息），确定被聚合的整组消息何时可用，以及必要地话，还要处理超时的状况。更进一步地，在超时的情况下，聚合器还要明确是仍然发送残缺消息，或是丢弃它们。对此，Spring Integration提供了可配置的超时处理策略。

### 2.4.6 服务激活器（Service Activitor）

“服务激活器”是一种将“服务实例”连接到“消息系统”的通用终端。对于该类型的终端，配置输入通道是必须的。而且，若被调用的服务方法具有返回值，那么此情况下或需要配置输出通道。

> 注意：输出通道的配置是可选的。因为每则消息在消息头中可能会提供它自身的“返回地址”(Return Address)信息。这个规则同样适用于其他的消费终端。

服务激活器会调用指定服务对象上的操作，来处理请求消息。该过程中会抽取请求消息的消息体并作必要的转换（若方法参数非消息类型参数）。每当服务方法产生返回值，这个返回值同样地会作出必要的转换，而成为一条响应消息（若方法返回值非消息类型）。响应消息将会被发送到输出通道上；若没有配置输出通道，且消息的“返回地址”可用，那么该响应将会被发送到返回地址指定的通道上。

![服务激活器示意图](http://static.oschina.net/uploads/space/2015/0323/173009_YRjT_2321188.jpg)

### 2.4.7 通道适配器（Channel Adapter）

“通道适配器”是一种连接消息通道到“其他系统”或是“传输端口”的消息终端。通道适配器分为“接入”或者“接出”两种。通常通道适配器被用来映射消息到其他任何发送/接收系统所需的对象或资源上（比如：文件、HTTP请求，JMS消息等等）。依赖于传输端口的情况下，通道适配器也可以填充或是抽取消息头中的值。Spring Integration提供了一些通道适配器，以后的章节中会讲述它们。

![通道适配器-source](http://static.oschina.net/uploads/space/2015/0323/173045_17jf_2321188.jpg)

*接入型通道适配器连接源系统到消息系统中*

![通道适配器-target](http://static.oschina.net/uploads/space/2015/0323/173125_WtFa_2321188.jpg)

*接出型通道适配器连接消息系统到目标系统中*

## 2.5 关于配置

贯穿本篇文档，都利用了XML命名空间的支持，来声明Spring Integration消息流中的各种元素。这背后由一系列命名空间解析器给予支撑，这些解析器自动生成了实现了特定组件功能的Bean定义。

当Spring Integration的名字空间元素被第一次解析时，框架将会自动声明若干bean，这些bean会被用来支撑运行时环境（比如：任务调度器、隐式通道构造器，等等）。

从4.0版本开始，当使用注解类，添加@EnableIntegration注解时，以上这些支撑bean也同样被创建。这样会利于使用纯Java配置来声明一个简单的Spring Integration消息流。另外，当存一个“父上下文”和多个“子上下文”时@EnableIntegration注解可以使得Spring Integration组件仅需声明一次。

## 2.6 编程实践

通常的建议是：务必使用POJOs（plain old java objects），不到万不得已之时不要在自己的代码中引入框架依赖。

如果你确实已经在自己的类中引用了框架，那么下面的建议可供参考：

* 如果实现了“ApplicationContextAware”接口，那么不要在setApplicationContext()方法中使用ApplicationContext对象；在这个方法里仅保存该引用，延迟对该对象的使用。
* 如果实现了“InitializingBean”接口或者使用@PostConstruct注解了方法，那么不要从这种初始化方法中发送任何消息出去，因为这些方法执行时应用上下文尚没有完成初始化，此时发送消息很可能会失败。如果需要在启动时刻发送消息，那么实现“ApplicationListener”接口，等待“ContextRefreshedEvent”事件发生时即可。或者，另外一种方式是，实现“SmartLifecycle”接口，将bean置于晚期阶段，然后在send()方法中发送消息。

# 3.消息通道

## 3.1 消息通道

尽管“消息”扮演着数据封装的关键角色，但别忘了解耦“消息生产者”和“消息消费者”的是“消息通道”。

### 3.1.1 消息通道的接口

Spring Integration中顶层的<code>MessageChannel</code>接口被定义为如下所示：

```java
public interface MessageChannel {
    boolean send(Message message);
    boolean send(Message message, long timeout);
}
```

当发送一条消息时，若发送成功则返回<code>true</code>；如果发送超时或者异常中断，则返回<code>false</code>。

取决于消息通道是否缓存消息（如概述章节所述），存在两种子类型的接口：

* 可缓存消息的轮询（pollable）通道接口
* 不缓存消息的订阅（subscribable）通道接口

#### 3.1.1.1 PollableChannel

以下是<code>PollableChannel</code>的定义：

```java
public interface PollableChannel extends MessageChannel {
    Message<?> receive();
    Message<?> receive(long timeout);
}
```

与<code>send()</code>方法类似，当接收消息时，若超时或者异常中断，将返回<code>null</code>。

#### 3.1.1.2 SubscribableChannel

实现<code>SubscribableChannel</code>基本接口的通道会直接发送消息到订阅他们的消息处理器。所以，他们都不涉及供轮询的接收方法，取而代之的是管理订阅者的相关方法：

```java
public interface SubscribableChannel extends MessageChannel {
    boolean subscribe(MessageHandler handler);
    boolean unsubscribe(MessageHandler handler);
}
```

### 3.1.2 消息通道的实现

Spring Integration提供了许多不同类型的消息通道实现，以下是关于其中各种的概要描述。

#### 3.1.2.1 PublishSubscribeChannel

<code>PublishSubscribeChannel</code>会广播消息到所有它的订阅者（消息处理器）。与通常只会被单一端点处理的“文档”型消息恰恰相反，这主要应用于发送“事件”型消息的场景。需要注意的是：<code>PublishSubscribeChannel</code>只能发送消息。当它的<code>send()</code>方法被调用时，它直接将消息广播给它的订阅者。而正由于此，消息消费者不能够自己轮询消息（通道没有实现<code>PollableChannel</code>接口，所以并不存在<code>receive()</code>方法）。此种情形下，所有的订阅者本身必须是<code>MessageHandler</code>，所有订阅者的<code>handleMessage(Message)</code>方法会被依次触发。

> MessageHandler接口的相关说明在下文中会涉及。

在3.0版本之前，调用<code>PublishSubscribeChannel</code>的<code>send()</code>方法，在不存在订阅者的情况下，会返回<code>false</code>。当结合消息模板（MessageTemplate）使用的时候会抛出<code>MessageDeliveryException</code>类型异常。从3.0版本以后（包括3.0），可以为通道设置“最少订阅者数量”（minSubscribers）属性，只要存在不少于该属性值的订阅者，那么就不会导致由于缺少订阅者而出错（该属性可以设置为0）。

#### 3.1.2.2 QueueChannel

<code>QueueChannel</code>实现内部包装了一个队列。不同于<code>PublishSubscribeChannel</code>，<code>QueueChannel</code>有着“点对点”的语义。换句话讲，即使通道拥有多个消费者，发送到该通道上的消息也只能被其中的一个消费者获得。它提供了一个无参构造器和一个可以通过参数指定容量的构造器。（无参构造器其实是指定了无限容量——容量大小为<code>Integer.MAX_VALUE</code>）

```java
public QueueChannel();
public QueueChannel(int capacity);
```

当通道尚未达到它的容量上限时，它会将消息保存在它内部的队列里，此时对<code>send()</code>方法的调用将即刻返回，即使处理消息的接收者尚未就绪。如果队列达到了容量上限，那么消息发送者将会被阻塞直到释放出可用的空间。或者，如果对发送操作设置了超时时间，那么阻塞状态将会持续到空间释放或者超出设定时限。同理，对于接收方来讲，若队列中存有可用消息，那么对<code>recieve()</code>方法的调用也将即刻返回；但是如果队列是空的，那么对<code>recieve()</code>方法的调用将会被阻塞直到有新的消息出现或者等待超时。无论在何种情况下，如果传入一个值为“0”超时参数，那么都将强制方法立即返回。需要注意的是：调用无参的<code>send()</code>与<code>recieve()</code>方法，都可能会导致永久阻塞（永远都没有出现可用队列空间或者可用消息）。

#### 3.1.2.3 PriorityChannel

不同于<code>QueueChannel</code>强制暗含了“先进先出”（FIFO）的顺序，<code>PriorityChannel</code>实现了基于优先级的消息进出顺序。默认在消息头部，以‘property’属性的消息头属性值来确定优先级。不过，用户可以定义自己的优先级判定逻辑：<code>PriorityChannel</code>的构造器能够接受一个<code>Comparator< Message< ?>></code>类型的比较器参数。

#### 3.1.2.4 RendezvousChannel

<code>RendezvousChannel</code>所具备的功能开启了一种“手把手交付”的场景，在这种场景下消息发送者（接收者）将会一直阻塞，直到通道的另一端有消息接收者（发送者）接收（发送）消息。实质上，这种实现有点类似于基于容量为0的同步队列的<code>QueueChannel</code>。以上所述适用于消息发送者与消息接收者工作于不同线程，但又不便于使用异步队列交换消息的情况。换句话说，使用<code>RandezvousChannel</code>的情况下，消息发送者至少明确知道消息已被消息接收者收到。而若使用<code>QueueChannel</code>，消息只是被存放于队列中，至于何时被接收、最终是否被接收，就不得而知了。

> 提示： 需要记住的是：所有基于队列的消息通道都默认将消息存储于内存中。当有持久化需求时，可以选择为"queue"元素设置"message-store"属性，通过该属性引用一个带有持久化功能的<code>MessageStore</code>实现。或者，也可以选择使用一个带有持久化代理的通道实现，例如基于JMS的通道或者通道适配器。关于这些内容后续会有更详细的介绍。

<code>RendezvousChannel</code>同样适用于“请求-响应”式操作。消息发送者可以创建一个临时的、匿名的<code>RendezvousChannel</code>实例，然后创建消息时将该通道设置为消息的返回地址（通过<code>replyChannel</code>属性头）；将消息发送出去之后，消息发送者可以适机（立即或者延时一段时间）调用通道的<code>recieve()</code>方法，进而等待响应消息。

#### 3.1.2.5 DirectChannel

<code>DirectChannel</code>有着“点对点”的语义，但是它却比上述任何基于队列实现的通道都更相似于<code>PublishSubscribeChannel</code>。它实现了<code>SubscribableChannel</code>接口而不是<code>PollableChannel</code>接口，所以它是将消息直接发送给订阅者的。但是，作为一种“点对点”通道，不同于一般的<code>PublishSubscribeChannel</code>实现的是，它仅将一条消息发送与一个订阅者，而非广播给所有订阅者。

除了提供这种最简单的点对点通道模式以外，它最重要的特性在于：它可以使得消息“发送”与“接收”这两端的处理操作在同一个线程中执行。举例来说，如果某消息处理器订阅了一个“DirectChannel”，那么向该通道发送一条消息，将会导致直接在发送者的线程里触发消息处理器的<code>handleMessage(Message)</code>方法。

提供此种通道实现的关键动机在于“受益于使用消息通道带来的抽象与松耦合的同时，也能够支持事务特性”。如果<code>send()</code>方法本身是在事务作用域范围内，那么消息处理器的执行结果（比如，是否成功更新一条数据库记录）将会影响到事务执行的最终结果（“提交”或是“回滚”）。

> 提示： 由于<code>DirectChannel</code>是最简单的一种通道，不需要诸如“调度”、“轮询器线程管理”等方面的任何附加配置，所以在Spring Integration中，该类型通道被认作为默认的消息通道。通常的实践经验是，在应用中先统统定义成缺省通道，然后再考虑其中哪些需要提供消息缓存或者输入限制功能，最后再将这些有特殊需求的通道修改为基于队列的<code>PollableChannels</code>类型实现。同样地，对于广播消息的需求，也应该进行修改，使用<code>PublishSubscribeChannel</code>而非<code>DirectChannel</code>。

<code>DirectChannel</code>内部委托“消息分发器”（Message Dispatcher）来调用订阅它的消息处理器。“消息分发器”的行为遵循了其内部设定的负载均衡策略，该策略可以通过<code>load-balancer</code>或者<code>load-balancer-ref</code>属性进行设置。当有多个消息订阅者订阅了同一个消息通道，那么该通道的“消息分发器”会通过负载均衡策略确定每条消息将由具体哪一个订阅者接收处理。为了方便使用，目前为<code>load-balancer</code>属性内置提供了：“round-robin”与“none”（不激活负载均衡）两种策略。当然也可以提供自定义的<code>LoadBalancingStrategy</code>实现，然后通过<code>load-balancer-ref</code>属性进行设置。

```xml
<int:channel id="lbRefChannel">
  <int:dispatcher load-balancer-ref="lb"/>
</int:channel>

<bean id="lb" class="foo.bar.SampleLoadBalancingStrategy"/>
```

注意：<code>load-balancer</code>属性与<code>load-balancer-ref</code>属性是互斥的。

“负载均衡”选项同样也可以结合“故障转移”（Failover）选项一起使用。如果<code>failover</code>值为<code>true</code>（默认为true），那么当消息分发器遇到消息接收异常时将会接着尝试再向下一个处理器发送消息。故障转移的顺序由消息处理器确定（可选），如果消息处理器未给出该顺序，那么将遵从初始时的订阅顺序。

如果某种特定的需求场景要求分发器总是先调用某一个处理器，然后按照一种固定的顺序完成故障转移，那么只要别设置任何负载均衡策略即可。换句话说，即使分发器并没有设置任何负载均衡策略，它仍然能够支持故障转移。

> 提示： 需要记住的是：“负载均衡”与“故障转移”只有在消息订阅者的数量大于1的时候才有效。

#### 3.1.2.6 ExecutorChannel

<code>ExecutorChannel</code>是一种“点对点”的通道，它像<code>DirectChannel</code>一样支持消息分发器的配置（负载均衡策略与故障转移属性）。这两种分发消息的通道类型间最显著的区别在于：<code>ExecutorChannel</code>委托<code>TaskExecutor</code>实例来执行消息的分发工作。这不仅意味着<code>send()</code>方法不会再被阻塞，而且同时也意味着：消息处理器的调用不再发生在发送者的线程中。正因如此，横跨消息发送者与接受者之间的事务也不会再受到支持。

> 提示： 也存在有偶然的因素会导致发送者阻塞。比如，使用了设有类似<code>ThreadPoolExecutor.CallerRunsPolicy</code>“拒绝策略”的<code>TaskExecutor</code>时,发送者线程将会在线程池耗尽时，自己直接执行消息处理器中的方法。这种情况的出现是不可预测的。

#### 3.1.2.7 Scoped Channel

Spring Integration 1.0版本曾经提供了一种<code>ThreadLocalChannel</code>实现，但是在2.0版本时就被遗弃了。目前，存在一种更为通用的方式来处理类似的需求，那就是为通道添加<code>scope</code>属性。该属性的值可以是上下文中任何一个可用<code>Scope</code>的名字。例如，在Web环境中存在一些可用的<code>Scope</code>，以及任何注册在在上下文中自定义<code>Scope</code>。以下所示为设置了基于ThreadLocal的scope的通道示例，这个例子里也包括了<code>Scope</code>自身的注册。

```xml
<int:channel id="threadScopedChannel" scope="thread">
     <int:queue />
</int:channel>
<bean class="org.springframework.beans.factory.config.CustomScopeConfigurer">
    <property name="scopes">
        <map>
          <entry key="thread" value="org.springframework.context.support.SimpleThreadScope" />
        </map>
    </property>
</bean>
```

上例中的通道同样委托了内部的队列，但不同的是该通道被限定在当前线程中，所以消息队列的内容也处于当前线程内。发送消息的线程可以从通道中接收之前发送的消息，但其它线程却无法访问这些消息。尽管<code>thread-scoped</code>的通道极少被用到，但是当需要在单一线程中使用<code>DirectChannel</code>类型的通道同时又要将响应消息发送至一个“最终”通道中时，此种类型的通道可以起到作用。如果“最终”通道被限定在线程作用域，原始的发送者线程就可以从通道中收集响应结果。

### 3.1.3 通道拦截器

消息驱动架构的优势之一就在于能够以一种普遍通用的且非侵入的方式来捕获到系统中所传输消息中有意义的信息。由于消息都是通过通道来传递的，那么正是通道提供了切入<code>send</code>与<code>receive</code>操作的机会。<code>ChannelInterceptor</code>策略接口为每种操作提供了切入方法：

```java
public interface ChannelInterceptor {
    Message<?> preSend(Message<?> message, MessageChannel channel);
    void postSend(Message<?> message, MessageChannel channel, boolean sent);
    void afterSendCompletion(Message<?> message, MessageChannel channel, boolean sent, Exception ex);
    boolean preReceive(MessageChannel channel);
    Message<?> postReceive(Message<?> message, MessageChannel channel);
    void afterReceiveCompletion(Message<?> message, MessageChannel channel, Exception ex);
}
```

可以通过以下调用将拦截器实现注册到通道中：

```java
channel.addInterceptor(someChannelInterceptor);
```

<code>ChannelInterceptor</code>接口中返回<code>Message</code>实例的方法可被用于进行消息转换，或者如果返回<code>null</code>将会阻断消息下一步的处理操作（当然，任何方法都可以抛出<code>RuntimeException</code>异常也将阻断消息处理）。还有，如果<code>preReceive</code>方法返回<code>false</code>也会阻断消息流。

> 提示: 需要记住的是：仅有<code>PollableChannels</code>才有<code>receive()</code>方法，<code>SubscribableChannel</code>类型的通道是没有此方法的。所以，<code>preReceive(..)</code>方法与<code>postReceive(..)</code>方法仅当作用于<code>PollableChannel</code>时才有效。

Spring Integration还提供了“窃听模式”（Wire Tap）的实现。其实质就是在不改变原消息流的前提下，将消息（副本）发送到另外一个通道的拦截器。这对于调试和监控来说是极其有用的。后续会有专门关于“窃听模式”的专题章节。

由于通常并不需要实现拦截器的所有方法，Spring Integration提供了<code>ChannelInterceptorAdapter</code>类，该类实现了<code>ChannelInterceptor</code>接口，并默认覆写了其中所有方法（对于返回值<code>void</code>的方法做空实现；对于返回值为<code>Message</code>对象的方法则直接将传入消息原样返回；对于返回<code>boolean</code>值的方法则统统返回<code>true</code>）。如此以来，继承<code>ChannelInterceptorAdapter</code>仅实现需要实现的方法较直接实现<code>ChannelInterceptor</code>更为简单方便，比如下面的例子：

```java
public class CountingChannelInterceptor extends ChannelInterceptorAdapter {

    private final AtomicInteger sendCount = new AtomicInteger();

    @Override
    public Message<?> preSend(Message<?> message, MessageChannel channel) {
        sendCount.incrementAndGet();
        return message;
    }
}
```

> 提示： 拦截器中的方法调用顺序取决于拦截器所作用于的具体通道类型。首先，如上所述，仅有基于队列实现的通道才会有对<code>receive()</code>方法的拦截。另外，对<code>send()</code>方法与<code>receive()</code>方法的拦截顺序取决于发送线程与接收线程的时间顺序。比如，如果接收者已经阻塞等待消息的情况下，那么拦截方法的顺序可能是：<code>preSend</code> <code>preReceive</code> <code>postReceive</code> <code>postSend</code>。但是，如果接收者在发送者已经将消息发送到队列上并已返回的情况下再去查询消息的话，那么拦截方法的执行顺序就可能变为：<code>preSend</code> <code>postSend</code> <code>preReceive</code> <code>postReceive</code>。综上看来，由于存在上述不确定性，所以程序逻辑不应该依赖拦截方法的执行顺序。

从Spring Integration 4.1版本开始（依赖于Spring Framework4.1或更高版本），<code>ChannelInterceptor</code>提供了两个新方法——<code>afterSendCompletion()</code>与<code>afterReceiveCompletion()</code>。不管在发送或者接收过程中产生任何异常,它们都分别会在<code>send()</code>与<code>receive()</code>方法之后被调用，如此便于能够进行一些资源回收操作。

### 3.1.4 消息模板工具（MessagingTemplate）

Spring Integration为应用提供了一套非侵入性的消息组件基础设置。可是，总会有一些情况下，让你不得不在应用代码中直接调用到消息系统。为了更方便的应对这种状况，SpringIntegration提供了<code>MessagingTemplate</code>来支持关于消息通道的各种操作，包括发送请求与等待响应的场景等。例如：

```java
MessagingTemplate template = new MessagingTemplate();
Message reply = template.sendAndReceive(someChannel, new GenericMessage("test"));
```

模板还可以支持以下多种类型的方法：

```java
public boolean send(final MessageChannel channel, final Message<?> message) { ... }
public Message<?> sendAndReceive(final MessageChannel channel, final Message<?> request) { .. }
public Message<?> receive(final PollableChannel<?> channel) { ... }
```

### 3.1.5 配置消息通道

使用<code>< channel/></code>元素声明可以创建一个消息通道实例：

```xml
<int:channel id="exampleChannel"/>
```

缺省的通道类型是“点对点”的。若要创建一个“发布订阅”类型的通道，可以使用<code>< publish-subscribe-channel/></code>元素：

```xml
<int:publish-subscribe-channel id="exampleChannel"/>
```

当<code>< channel/></code>元素不包含任何子元素时，将会创建一个<code>DirectChannel</code>实例（<code>SubscribableChannel</code>接口类型实现）。

不过，为<code>< channel/></code>元素提供<code>< queue/></code>子元素则将会创建具备轮询能力的通道类型。更多的例子在下文展开。

#### 3.1.5.1 DirectChannel 配置

如上所述， <code>DirectChannel</code>作为默认通道类型，配置方式如下：

```xml
<int:channel id="directChannel"/>
```

缺省情况下，通道设置了“round-robin”负载均衡器，并且“failover”属性被设置为使能状态。改变以上配置可以通过添加<code>< dispatcher /></code>子元素和设置对应属性来完成：

```xml
<int:channel id="failFastChannel">
    <int:dispatcher failover="false"/>
</channel>

<int:channel id="channelWithFixedOrderSequenceFailover">
    <int:dispatcher load-balancer="none"/>
</int:channel>
```

#### 3.1.5.2 Datatype Channel 配置

存在这么一种可能性，就是说消息消费者仅能处理特定类型的消息内容，所以要求你必须能够保证消息内容类型为预期类型。使用“消息过滤器”或者基于内容类型的“消息路由器”都可以满足上述需求。但是，使用“Datatype Channel”模式是一种更简单的应对方案。创建仅能接受某种特定内容类型消息的Datatype Channel的方法如下所示，为<code>< channel></code>元素的<code>datatype</code>属性设置全限定类型名称即可。

```xml
<int:channel id="numberChannel" datatype="java.lang.Number"/>
```

需注意的是，在上个例子中，“numberChannel”会接受<code>java.lang.Integer</code>或者<code>java.lang.Double</code>类型的消息，因为通道所进行的类型比较是基于Java类型系统的。多类型的设置可以通过逗号分隔的列表来表示：

```xml
<int:channel id="stringOrNumberChannel" datatype="java.lang.String,java.lang.Number"/>
```

如果消息类型不在可接受范围内又会怎样呢？这取决于当前上下文中是否定义了名字为“integrationConversionService”并且实现了Spring<code>ConversionService</code>的bean。若没有，那么将会抛出异常；反之，将会使用“integrationConversionService”bean定义试图将消息内容转换为目标类型。

你甚至可以注册自定义的转换器（ConversionService）。比方说，如果你直接使用上文中定义的“numberChannel”进行下列操作：

```java
MessageChannel inChannel = context.getBean("numberChannel", MessageChannel.class);
inChannel.send(new GenericMessage<String>("5"));
```

不出意料地这将会导致抛出异常，错误日志如下：

```log
Exception in thread "main" org.springframework.integration.MessageDeliveryException:
Channel 'numberChannel'
expected one of the following datataypes [class java.lang.Number],
but received [class java.lang.String]
```

不过，如果我们实现一个转换器将字符串类型转为整形，如下：

```java
public static class StringToIntegerConverter implements Converter<String, Integer> {
    public Integer convert(String source) {
        return Integer.parseInt(source);
    }
}
```

然后将该转换器注册为Spring Integration的“Conversion Service”，如下：

```xml
<int:converter ref="strToInt"/>
<bean id="strToInt" class="org.springframework.integration.util.Demo.StringToIntegerConverter"/>
```

当解析<code>converter</code>元素时，就会创建一个“integrationConversionService”命名的bean。在这个bean的作用下，可以将消息中字符串类型的内容转换为整数类型。

#### 3.1.5.3 QueueChannel 配置

使用带有<code>< queue /></code>子元素的<code>< channel /></code>元素可以创建一个<code>QueueChannel</code>，同时也可以设定通道的容量大小：

```xml
<int:channel id="queueChannel">
    <queue capacity="25"/>
</int:channel>
```

> 提示： 如果没有设置容量大小属性，那么通道的容量将默认为无限。为了避免类似与<code>OutOfMemoryErrors</code>的错误，建议为通道设置容量上限属性。

**Persistent QueueChannel 配置**

由于<code>QueueChannel</code>默认在内存中缓存消息，所以若发生系统故障可能会导致消息丢失。为了避免此类风险，可以使用带有持久化实现机制的<code>QueueChannel</code>。当队列通道收到消息后，它会把消息置于一个称为MessageStore的对象中。当消息被查询时，会被从MessageStore中移除掉。

缺省情况下，MessageStore是基于内存的实现，但是Spring Integration也同样提供了持久化的store，比如<code>JdbcMesssageStore</code>。

可以仿照下面的例子来为任何类型的<code>QueueChannel</code>设置<col>message-store</col>属性：

```xml
<int:channel id="dbBackedChannel">
    <int:queue message-store="channelStore"/>
</int:channel>

<bean id="channelStore" class="o.s.i.jdbc.store.JdbcChannelMessageStore">
    <property name="dataSource" ref="dataSource"/>
    <property name="channelMessageStoreQueryProvider" ref="queryProvider"/>
</bean>
```

Spring Integration 中的 JDBC 模块提供了各种流行数据库相应的数据库支撑表定义脚本。脚本位于“spring-integration-jdbc”模块的<code>org.springframework.integration.jdbc.store.channel</code>包中。

> 注意： 这里有一个比较重要的特性是，对于任何事务性的持久化store来说（比如JdbcChannelMessageStore），只要消息查询者配置了事务支持，那么消息只有在整个事务成功提交后才会被从store中永久移除；反之，若事务回滚，消息并不会被丢失。

随着与各种“NoSQL”数据库相关的Spring项目提供底层支持，将来会出现越来越多的“MessageStore”。当然，你也可以实现<code>MessageGroupStore</code>接口，进而使用自定义的“MessageStore”来满足个性化的需求。

另外一项可以在<code>QueueChannel</code>通道类型环境下自定义的配置选项为<code>< int:queue></code>子元素。此处可以引用任何<code>java.util.Queue</code>的实现类型。

#### 3.1.5.4 PublishSubscribeChannel 配置

使用<code>< publish-subscribe-channel/ ></code>元素可以创建<code>PublishSubscribeChannel</code>类型通道。 当时用该通道时，同时也可以为“消息发布”定义<code>task-executor</code>（如果不设置该属性的话，发布发布消息的操作将会在在发送者的线程中执行）。

```xml
<int:publish-subscribe-channel id="pubsubChannel" task-executor="someExecutor"/>
```

如果在<code>PublishSubscribeChannel</code>的下游消息流中定义了<code>Resequencer</code>或者<code>Aggregator</code>，那么你可以为通道设置<code>apply-sequence</code>属性。如此将意味着通道将为发布的消息设置<code>sequence-size</code>与<code>sequence-number</code>以及“相关性的ID值”的消息头属性。比如，如果通道有5个订阅者，那么<code>sequence-size</code>属性将被设置为5，被发布的消息将依次具有范围1至5的<code>sequence-number</code>头部属性值。

```xml
<int:publish-subscribe-channel id="pubsubChannel" apply-sequence="true"/>
```

> 注意： 默认情况下，<code>apply-sequence</code>属性值为<code>false</code>，这样<code>PublishSubscribeChannel</code>将为每个订阅者发送一模一样的消息。当该属性为<code>true</code>时，由于Spring Integration遵循“消息不变性”，所以通道将创建新的消息实例，这些新的实例都共同引用了原消息体，但各自具有新的消息头。

#### 3.1.5.5 ExecutorChannel 配置

若要创建<code>ExecutorChannel</code>，添加一个带有<code>task-executor</code>属性的<code>dispatcher</code>子元素即可。<code>task-executor</code>属性可以引用上下文中定义的任何<code>TaskExecutor</code>。如上文所述，<code>ExecutorChannel</code>的使用将会导致消息发送者与消息接收者之间的事务约定无效，因为它将两端的处理逻辑分隔在了两个线程中。

```xml
<int:channel id="executorChannel">
    <int:dispatcher task-executor="someExecutor"/>
</int:channel>
```

> 注意： 属性<code>load-balancer</code>与<code>failover</code>同样都还是可用的，属性性质与前文的<code>DirectChannle</code>一致：

```xml
<int:channel id="executorChannelWithoutFailover">
    <int:dispatcher task-executor="someExecutor" failover="false"/>
</int:channel>
```

#### 3.1.5.6 PriorityChannel 配置

使用<code>< priority-queue/ ></code>子元素可以创建一个<code>PriorityChannel</code>。

```xml
<int:channel id="priorityChannel">
    <int:priority-queue capacity="20"/>
</int:channel>
```

缺省地，通道将会参照消息头部的<code>priority</code>属性来确定消息的优先级。但是，也可以引用一个自定义的优先级<code>Comparator</code>来判定消息优先级。下例中展示了一个支持类型过滤与设定了通道容量的例子：

```xml
<int:channel id="priorityChannel" datatype="example.Widget">
    <int:priority-queue comparator="widgetComparator" capacity="10"/>
</int:channel>
```

从4.0版本开始，优先级通道支持设置<code>message-store</code>选项（这种情况下不知道设置自定义优先级判定器）。消息Store必须是<code>PriorityCapableChannelMessageStore</code>类型。当前<code>PriorityCapableChannelMessageStore</code>能够支持Redis、JDBC以及MongoDB。

#### 3.1.5.7 RendezvousChannel 配置

当<code>channel</code>元素附有<code>< rendezvous-queue ></code>子元素时，将会创建<code>RendezvousChannel</code>实例。<code>RendezvousChannel</code>不接受关于通道队列容量大小的设置，因为它实质上包含了一个容量大小为0的直接交付的队列。

```xml
<int:channel id="rendezvousChannel"/>
    <int:rendezvous-queue/>
</int:channel>
```

#### 3.1.5.8 Scoped Channel 配置

Scoped Channel 的配置方式如下：

```xml
<int:channel id="threadLocalChannel" scope="thread"/>
```

#### 3.1.5.9 Channel Interceptor 配置

为<code>< channel ></code>元素设置<code>< interceptors ></code>子元素，将为消息通道设置拦截器。如下：

```xml
<int:channel id="exampleChannel">
    <int:interceptors>
        <ref bean="trafficMonitoringInterceptor"/>
    </int:interceptors>
</int:channel>
```

一个拦截器实现可以被多个通道共用。

#### 3.1.5.10 全局的消息通道拦截器配置

通道拦截器提供了一种简单明了的手段来横切每个消息通道的行为。如果需要对一批通道进行普遍的横切，那么一个挨一个地重复同样的配置显然缺乏效率。为了更有效率地应对上述情况，Spring Integration提供了“全局拦截器”的概念。例如下面的配置：

```xml
<int:channel-interceptor pattern="input*, bar*, foo" order="3">
    <bean class="foo.barSampleInterceptor"/>
</int:channel-interceptor>
```

或者：

```xml
<int:channel-interceptor ref="myInterceptor" pattern="input*, bar*, foo" order="3"/>
<bean id="myInterceptor" class="foo.barSampleInterceptor"/>
```

使用<code>< channel-interceptor/ ></code>元素将能够定义一个全局的拦截器，作用于与<code>pattern</code>属性匹配的所有通道。上例中的全局拦截器将作用于名称为“foo”以及所有以“bar”和“input”名称开头的通道。<code>order</code>属性设置了拦截器的作用顺序，如果通道上被设置了多个拦截器的话。比如所下面的例子展示了“input”通道自身已被定义了局部的拦截器：

```xml
<int:channel id="inputChannel"> 
  <int:interceptors>
    <int:wire-tap channel="logger"/> 
  </int:interceptors>
</int:channel>
```

那么通道上被设置的所有拦截器（局部本地设置的以及全局设置的）究竟会按照什么顺序来发挥作用呢？目前的实现提供了一项非常简单的机制：拦截器的<code>order</code>属性值将会确定其执行顺序，该值越小那么对应拦截器的顺序将会越靠前。

> 提示： <code>order</code>属性值默认为‘0’；<code>pattern</code>属性值默认为‘*’。

#### 3.1.5.11 监听模式

正如上文中所提到的，Spring Integration提供了开箱即用的“监听模式”拦截器。可以在任何通道的<code>< interceptors/ ></code>元素中配置消息监听路由。这样的配置对于程序调式来说是非常适用的，也可以配合Spring Integration中的日志通道适配器来使用。比如下例所示：

```xml
<int:channel id="in">
    <int:interceptors>
        <int:wire-tap channel="logger"/>
    </int:interceptors>
</int:channel>

<int:logging-channel-adapter id="logger" level="DEBUG"/>
```

> 提示 通过使用SpEL表达式为<code>logging-channel-adapter</code>设置<code>expression</code>属性，可以过滤消息内部的具体内容，比如消息头部中的属性或者是消息体中的具体某项内容。另外，也可以直接设置<code>log-full-message</code>属性为<code>true</code>，就可以令日志记录包括所有的消息内容（该值默认为<code>false</code>，仅有消息体会被记录）。

**关于监听模式进一步说明**

大部分人可能想当然地认为消息监听路由自然是异步的。可事实并非如此，Spring Integration中确定某个消息操作是否异步（或者同步）的关键角色在于“消息通道”。不同的通道类型会使得消息处理遵循不同的方式，这也是将将消息通道抽象化的优势之一。自从Spring Integration框架创建之初，消息通道一直就被强调为框架中的“一等公民”。它不仅仅只是一个内部的、隐含的对“企业集成模式”的实现，并且更重要地，它是对于用户完全开放、可按需配置的消息部件。

所以，消息监听路由仅仅负责以下三项工作：

* 拦截进入通道的消息
* 抓取消息
* 将消息发送到另外的监听通道上

那么，关于被路由监听得到的消息究竟是同步的还是异步的呢？这取决与监听通道本身的配置。

最后需要指出的一点是，一般的实践中，诸如监听路由性质的工作，应当尽量不要产生阻塞。所以，为此通常应该选用异步效果的消息通道。当然，也有一些个别原因使得我们必须考虑同步消息，比如说，我们为了审计而必须保证消息监听路由被包含在事务边界以内。

#### 3.1.5.11 全局消息监听路由的配置

正如配置全局消息通道拦截器一样，也可以配置全局的消息监听路由。如下：

```xml
<int:wire-tap pattern="input*, bar*, foo" order="3" channel="wiretapChannel"/>
```

### 3.1.6 其它特殊的通道

在Spring Integration名字空间有效的情况下，在应用上下文中存在两种特殊的通道：

* <code>nullChannel</code>
* <code>errorChannel</code>

<code>nullChannel</code>的含义就像“/dev/null”一样。“nullChannel”这个名称，在上下文中是保留字，可以直接使用。而<code>errorChannel</code>则是专门用来投递出错消息，在框架内部被用来传递出错消息，而且它可以被自定配置重写覆盖。

## 3.2 轮询器 (轮询型消费者）

当消息终端连接到消息通道上并被初始化后产生的实例对象类型为下述两者之一：

* PollingConsumer：轮询型消费者
* EventDrivenConsumer：事件驱动型消费者

到底是二者中的哪一种取决于消息终端连接的通道类型。如果连接的通道是<code>org.springframework.integration.core.SubscribableChannel</code>接口实现，那么将会生成<code>EventDrivenConsumer</code>类型的消费者实例；相对应地，如果连接的通道是<code>org.springframework.integration.core.PollableChannel</code>接口的实现，那么将会生成<code>PollingConsumer</code>类型的消费者实例。

轮询型消费者是通过主动地查询来获取消息而不是被动地依靠“事件驱动”的方式。

关于轮询消费者更多的理论，可以参照《EIP》中的论述：[http://www.enterpriseintegrationpatterns.com/PollingConsumer.html](https://www.oschina.net/action/GoToLink?url=http%3A%2F%2Fwww.enterpriseintegrationpatterns.com%2FPollingConsumer.html)

更进一步地，Spring Integration中提供了轮询消费者模式的另一种变体模式。在使用“接入通道适配器”（Inbound Channel Adapter）的情况下，这些适配器通常会使用<code>SourcePollingChannelAdapter</code>进行封装。例如，当需要从一个远程FTP服务器收取消息时， “FTP Inbound Channel Adapter”会被配置一个轮询器来周期性地查询消息。

这意味着轮询器既可以被用于“接入消息”（inbound）也可以被用于“接出消息”（outbond）的场景。以下列举了一些场景例子：

* 轮询外部的系统，比如FTP Servers, Databases 或者 Web Services
* 轮询内部的通道
* 轮询内部的服务，比如某些Java Class中的某些方法

本小节仅仅是概要地介绍了轮询型消费者，以及它们与消息通道间的相互作用。更详细的内容会在下文相应章节继续展开。

## 3.3 通道适配器

通道适配器（Channel Adapter）是一种可以将（单独一个）消息发送者或者消息接收者与消息通道建立连接的消息终端。Spring Integration提供了许多开箱即用的消息通道适配器来支持多种类型的传输端口，比如JMS、File、HTTP、Web Service、Mail，等等（后续将有专门介绍该部分内容的章节）。本小节内容重点介绍一种简单却又广泛被应用的“方法调用”通道适配器。该类适配器可适用于“接入”（Inbound）消息与“接出”（Outbound）消息两种场景，并且都可以通过XML名字空间来进行配置。

### 3.3.1 配置通道适配器

<code>inbound-channel-adapter</code>元素可以调用某个Spring（上下文中）对象上的任何方法，并且将方法的返回值转换为“消息”后发送到对应的消息通道上。一旦适配器被激活，那么适配器的轮询器将开始工作，试图从消息源中收取消息。轮询器的执行策略将按照配置中设定的<code>TaskScheduler</code>来进行。通道适配器以及适配器的轮询器和轮询策略的配置样例如下所示：

```xml
<int:inbound-channel-adapter ref="source1" method="method1" channel="channel1">
    <int:poller fixed-rate="5000"/>
</int:inbound-channel-adapter>

<int:inbound-channel-adapter ref="source2" method="method2" channel="channel2">
    <int:poller cron="30 * 9-17 * * MON-FRI"/>
</int:channel-adapter>
```

> 提示： 如果没有为通道适配器配置轮询器，那么必须在全局上下文中注册一个缺省的轮询器。

> > **关于轮询器的配置的重点说明：** 对于一般用于从消息源中轮询消息的轮询器来说（比如调用某个生成消息内容的服务方法），其配置样例如下：

```xml
<int:poller max-messages-per-poll="1" fixed-rate="1000"/>
<int:poller max-messages-per-poll="10" fixed-rate="1000"/>
```

上例中第一种配置里，由于<code>max-messages-per-poll</code>属性设置为1，所以每次轮询会激发轮询任务执行一次；而第二种配置里，则每次轮询会激发轮询任务执行10次，或者终止于10次以内返回<code>null</code>的情形。在这两种配置里，轮询激发会每隔1秒钟间歇发生一次（<code>fixed-rate="1000"</code>）。

```xml
<int:poller fixed-rate="1000"/>
```

如果像上例一样，不设置<code>max-messages-per-poll</code>属性。那么这意味着每次轮询激发，都会一直执行轮询任务直到被轮询的方法调用返回<code>null</code>。其实，这是<code>max-messages-per-poll</code>属性值设置为“-1”的效果（默认值即为“-1”）。

```xml
<int:poller max-messages-per-poll="-1" fixed-rate="1000"/>
```

### 3.3.2 配置消息接出通道适配器（ Outbound Channel Adapter）

<code>outbound-channel-adapter</code>元素将创建一个消息通道，该通道会把通道内的消息内容作为参数来调用指定的POJO消费者方法。配置方法如如下例所示：

```xml
<int:outbound-channel-adapter channel="channel1" ref="target" method="handle"/>
<beans:bean id="target" class="org.Foo"/>
```

如果被适配的是<code>PollableChannel</code>通道类型，那么需要提供一个关于轮询器配置的子元素，如下：

```xml
<int:outbound-channel-adapter channel="channel2" ref="target" method="handle">
    <int:poller fixed-rate="3000"/>
</int:outbound-channel-adapter>

<beans:bean id="target" class="org.Foo"/>
```

当然，POJO消费者也可以定义在<code>< outbound-channel-adapter ></code>内部:

```xml
<int:outbound-channel-adapter channel="channel" method="handle">
    <beans:bean class="org.Foo"/>
</int:outbound-channel-adapter>
```

> 提示： 不允许同时使用“引用属性”与“内部定义”的方式来设置POJO消费者。

任何通道适配器都可以不设置<code>channel</code>引用，这种情况下会隐含创建一个<code>DirectChannel</code>类型的实例。并且该实例的名称取自相应通道适配器的<code>id</code>属性，也由于此方面的原因，该种情况下，通道适配器的<code>id</code>属性是必须设置的。

### 3.3.3 通道适配器中的表达式与脚本

正如Spring Integration中的其它组件一样，<code>< inbound-channel-adapter ></code> 与 <code>< outbound-channel-adapter ></code> 同样支持SpEL表达式赋值。另外，从3.0版本开始，可以支持设置<code>< script ></code>子元素。关于该部分内容的详细说明将会在后续相应章节开展。

## 3.4 消息桥接

### 3.4.1 消息桥接简介

“消息桥接”是一种能够在两个消息通道或者通道适配器之间建立连接的居间消息终端。比如说，你可能会想到将一个<code>PollableChannel</code>与一个<code>SubscribableChannel</code>连接起来，这样就可以使得订阅终端享用到任何轮询功能配置了。使用“消息桥接”就可以达到如此目的。

使用消息桥接在两个通道之间设置一个中间轮询器，可以起到限制消息的流速。因为轮询器的触发速率与<code>maxMessagesPerPoll</code>属性将会强制限制消息的吞吐速率。

另外一种关于消息桥接的合理用法是连接两种不同的系统。如果这两个系统间不需要格式转换的话，直接使用消息桥接会更有效率。

### 3.4.2 桥接配置

使用<code>< bridge ></code>元素将创建一个消息桥接。被连接的消息通道通过元素中的<code>input-channel</code>与<code>output-channel</code>属性来进行设置，如下例所示：

```xml
<int:bridge input-channel="input" output-channel="output"/>
```

连接<code>PollableChannel</code>与<code>SubscribableChannel</code>的桥接配置如下所示：（该配置中桥接同样起到限速器的作用）

```xml
<int:bridge input-channel="pollable" output-channel="subscribable">
     <int:poller max-messages-per-poll="10" fixed-rate="5000"/>
 </int:bridge>
```

桥接通道适配器也同样简单。下面的例子中，展示连接名为“stdin”与“stdout”两适配器的情况（这两种适配器是Spring Integration的“stream”名字空间提供的）：

```xml
<int-stream:stdin-channel-adapter id="stdin"/>

<int-stream:stdout-channel-adapter id="stdout"/>

<int:bridge id="echo" input-channel="stdin" output-channel="stdout"/>
```

> 提示： 如果桥接的<code>output-channel</code>属性没有被设置，那么将参照流经消息的<code>reply-channel</code>属性值来传递消息。若获取<code>reply-channel</code>未果，那么将会导致抛出异常。

转载：[https://my.oschina.net/yumg/blog/387701](https://my.oschina.net/yumg/blog/387701)

