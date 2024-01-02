title: 蚂蚁中间件SOFA
date: '2020-04-11 17:11:19'
updated: '2020-04-16 14:04:14'
tags: [sofa, 蚂蚁中间件, servicemesh, sofaboot]
permalink: /articles/2020/04/11/1586596278773.html
---
![33444943e2761783cd8ab95.webp](https://img.hacpai.com/file/2020/04/33444943e2761783cd8ab95-5716895e.webp)


# 1.Sofa是什么

SOFA 源自于 Service Oriented Fabric Architecture，即面向服务的架构。  
随着 SOFA 的开源，目前 SOFA 的新解释：Scalable Open Financial Architecture

SOFA 是蚂蚁金服自主研发的金融级分布式中间件，包含了构建金融级云原生架构所需的各个组件，包括微服务研发框架，RPC 框架，服务注册中心，分布式定时任务，限流/熔断框架，动态配置推送，分布式链路追踪，Metrics监控度量，分布式高可用消息队列，分布式事务框架，分布式数据库代理层等组件，是一套分布式架构的完整的解决方案，也是在金融场景里锤炼出来的最佳实践。

# 2.为什么要用Sofa

#### Sofa和Spring cloud

* 不同点  
    SOFA中将整个系统拆分为一个个模块(bundle)，SpringCloud将系统拆分为多个微服务(MicroService)，其实意思差不多，各个模块(服务)各司其职，通过JVM/RPC进行调用。 SOFA可以通过JVM/RPC进行服务之间的接口调用，而SpringCloud只能通过RPC/HTTP方式进行调用
    
* Sofa优势  
    SOFA是蚂蚁金服长期发展沉淀下来的一条技术方案，在SpringCloud出现之前，SOFA已经能够在金融云环境下稳定运行了， 并且SOFA是蚂蚁金服自己研发的一套方案，天然集成了RPC、服务路由等功能，能够与蚂蚁内部其它中间件(如zdal、drm、msgbroker等)无缝结合，这一整套技术方案撑起了蚂蚁金服的核心业务， 它更加适合金融云环境，一旦出现问题能够快速定位并解决。
    

更详细的比较可以参考：[Spring Cloud 与 SOFA 对比（知乎）](https://www.zhihu.com/question/273919147)

# 3.Sofa优点

模块化，模块边界清晰，易于维护。  
服务化，服务的注册和依赖都很方便。  
易于扩展，很好的定义扩展点和扩展。

# 4.Sofa功能

#### Sofa

* 服务发布与引用  
    通过 SOFA JVM 服务的发布与引用，解决了隔离 SOFA 模块的通信问题，SOFA 提供了三种方式给开发人员来发布 JVM 服务和引用，分别是： XML 方式、Annotation 方式及编程 API 方式 。
    
* 基于 Velocity 的 Spring 配置  
    SOFA 的 Spring 配置文件基于 Velocity，根据用户的不同配置文件，将初始化不同的 Bean，提升灵活性。
    
* 生命周期管理  
    SOFA 框架包含完整的生命周期管理，应用可以监听 SOFA 应用或者 SOFA 组件的生命周期事件。
    
* Log4j2 支持  
    SOFA 框架支持 Log4j2，实现日志的异步打印。同时，SOFA 框架基于 DRM 实现了动态调整日志级别功能。
    
* SOFA 扩展点  
    SOFA 框架的模块是相互隔离的，SOFA 扩展点允许一个模块对其依赖的模块中定义的组件进行定制化。
    
* 健康检查  
    SOFA框架提供了一套可扩展的健康检查机制，可以帮助应用确定启动完毕后是否健康，是否可以对外提供服务。
    

#### Sofa RPC

* 远程调用  
    基于 TCP 和自有二进制协议的高效的、透明的远程服务调用，支持更加复杂的对象，且提供了更为丰富的调用方式（sync、oneway、callback、future 等）。
    
* 服务发现  
    服务提供者自动注册到服务注册中心；服务消费者从注册中心订阅服务提供者的地址；支持提供者地址变化的自动发现，为服务提供良好的伸缩性。
    
* 集群容错  
    服务调用者在部分服务提供者出现问题时，进行自动容错。
    
* 服务路由与负载均衡
    

如果存在多个可用的服务提供者，服务调用者在本地根据服务端路由和负载均衡算法选择其中一台进行调用。可在内网替代 F5 等硬件负载均衡器，解决了系统单点问题的同时，大大降低了企业成本。

* 良好的扩展接口  
    可以基于各种扩展实现功能。

# 5.Sofa分层

![2.webp](https://img.hacpai.com/file/2020/04/2-4967fa3f.webp)

![3.webp](https://img.hacpai.com/file/2020/04/3-948881fd.webp)


SOFA应用中各个模块之间的Spring Context是完全隔离的，需要拆分的时候直接将模块拆分即可，调用的方式由本地服务改为远程服务就可以了。本地服务可以理解为注册在本地注册中心，服务之间通过JVM调用，拆分后远程服务注册在远程注册中心，服务之间通过RPC调用。

# 6.健康检查

1. 在健康检查之前首先调用各个组件的deployCompletion方法，以及应用的ApplicationStartupCallback方法
2. 健康检查内容
    * 检查Spring上下文是否启动成功
    * 检查用户自定义的检查项
    * 检查所有具有流量出口的组件（SOFA Reference，消息发送端）是否健康；如果失败，每过500ms继续检查20次
        
          
  ![4.webp](https://img.hacpai.com/file/2020/04/4-ab9f194f.webp)
      
      

# 7.Sofa RPC
![5.webp](https://img.hacpai.com/file/2020/04/5-7780bae1.webp)


# 8.SOFABoot 相关
## 8.1 什么是 SOFABoot
[SOFABoot 官网](https://tech.antfin.com/products/SOFABoot)
 [SOFABoot 开源社区](https://github.com/alipay/sofa-boot)
[SOFABoot 文档](https://tech.antfin.com/docs/2/48619)

SOFABoot 是基于 Spring Boot 的开发框架，用于快速、敏捷地开发 Spring 应用程序，特别适合构建微服务系统。SOFABoot 在 Spring Boot 的基础上提供了诸如 Readiness Check、类隔离、日志空间隔离等能力，以解决大规模团队开发云原生微服务系统中会遇到的问题。同时 SOFABoot 也提供了蚂蚁金服金融科技中间件的轻量级集成方案，仅需少量配置即可在 SOFABoot 中使用金融科技中间件。金融科技中间件也可通过相应的 starter 模块单独配置集成到 Spring Boot 工程中。普通 Spring 工程通过 Embedded-SOFA 模式可以方便地集成并使用金融科技中间件。

SOFABoot 基于 Spring Boot 1.4.2 版本开发，使用标准 Spring 接口实现。可将 SOFABoot 理解为 Spring 的一个扩展，构建在 Spring Boot 基础之上提供金融科技中间件解决方案，每一个中间件均是一个可插拔的组件，添加和移除非常方便，同时，利用“约定优先配置”（convention over configuration）的理念完成自动配置，开发者能够更加专注于业务逻辑。

> Spring Boot 是一个非常优秀的开源框架，可以快速、敏捷地开发新一代基于 Spring 框架的应用程序，它并不是用来替代 Spring 的解决方案，而是和 Spring 框架紧密结合，用于提升 Spring 开发者体验的工具。SOFABoot 在 Spring Boot 的基础上进行了能力的增强并提供了蚂蚁中间件的轻量集成，且可与 Spring Boot、Spring 工程无缝集成。

SOFABoot 支持创建 Web 和 Core 两种类型的工程。当使用 SOFABoot 开发一个 Web 程序时，相当于“基于 Spring Boot 的 Web 应用 + 蚂蚁金服中间件” 进行开发；当使用 SOFABoot 开发一个 J2SE 程序（无 Web 页面访问），相当于“基于 Spring Boot 的非 Web 应用（无 servlet 依赖）+ 蚂蚁金服中间件” 进行开发。

## 8.2 功能特性

SOFABoot 框架不仅能实现中间件的集成管理、自动配置以及调用链路监控及治理，支持 Embedded-SOFA 模式、多类型的部署模式，还具有应用日志和中间件日志的隔离能力，并拥有一套完整的技术栈。

### 集成管理和自动配置

只需添加相应中间件的 starter 模块，SOFABoot 会自动导入所需的依赖并完成必要的配置。

### Embedded-SOFA 模式

提供 Embedded-SOFA 模式，以便于在 Spring 编程环境下使用蚂蚁金服金融科技中间件。

### 调用链路监控及治理

集成日志跟踪工具 Tracer，提供统一的中间件日志埋点和上下文 ID，将上下游系统的调用关系串联起来。

### 多类型的部署模式

既支持直接运行可执行的 fat JAR 文件，也支持部署至各种 servlet 容器中（如 Tomcat、Jetty、Undertow 等）。

### 应用日志和中间件日志的隔离能力

各中间件日志均面向 SLF4J 接口进行编程，日志实现依赖于具体的应用配置，且支持日志隔离。

### 完整的技术栈

拥有一套完整的技术栈，能自动解决后续的依赖下载、应用部署、健康检查、运维监控等问题。开发人员集成框架后，只需专心编写业务代码。

## 8.3 产品优势


## 基于 SpringBoot 并兼容开源生态

可与 Spring Boot、Spring 工程无缝集成，降低用户的迁移成本。

## 原生云工程结构

满足原生云应用的十二个因素，具备快速开发，持续交付和部署服务，弹性扩展，故障隔离、自动恢复等特点。

## 集成全套金融级中间件

提供各种默认配置，引入依赖无需额外部署，只需引入所需中间件的 Starter 就能直接使用所需的中间件。

## 统一易用的编程接口

每一个蚂蚁金服金融科技中间件都是独立可插拔的组件，对集成的金融科技中间件提供统一易用的编程接口，节约开发时间，和后期维护的成本。

## 遵循 OpenTracing 埋点

提供平台无关、厂商无关的 API，使得开发人员能够方便的添加（或更换）追踪系统的实现，跟踪分布式系统内各组件的调用情况等。

## 多维度应用度量

提供多种度量维度实时监测应用程序的性能，能帮助更好的了解当前应用程序或者服务在线上的各种性能状态。

## 8.4 基础术语


| 术语 |  英文 |  说明 |
| :-- |  :-- |  :-- |
| Dubbo |  Dubbo |  Dubbo 是一个分布式服务框架，致力于提供高性能和透明化的 RPC 远程服务调用方案，是阿里巴巴 SOA 服务化治理方案的核心框架，每天为 2,000+ 个服务提供 3,000,000,000+ 次访问量支持，并被广泛应用于阿里巴巴集团的各成员站点。 |
| Embedded-SOFA |  Embedded-SOFA |  支持在 Spring 编程环境下使用蚂蚁金服金融科技中间件。 |
| Fat JAR |  Fat JAR |  Fat JAR 是一种可执行的 JAR 包（Executable JAR），包含编译后的类及代码运行所需依赖 jar 的存档，可以使用 `java-jar` 命令运行该应用程序。Fat JAR 和普通的 JAR 不同在于它包含了依赖的 JAR 包。 |
| Gradle |  Gradle |  ApacheGradle 是一个基于 Apache Ant 和 Apache Maven 概念的项目自动化构建工具。它使用一种基于 Groovy 的特定领域语言（DSL）来声明项目设置，抛弃了基于 XML 的各种繁琐配置。 |
| Jetty |  Jetty |  Jetty 是一个开源的 Java servlet 容器，它为基于 Java 的 Web 容器，例如 JSP 和 servlet，提供运行环境。 |
| Log4j |  Log4j |  Apache Log4j，即 log for Java（Java 的日志)，是 Apache 的一个开源项目，可以控制日志信息输送的目的地，也可以控制每一条日志的输出格式，通过定义每一条日志信息的级别，能够更加细致地控制日志的生成过程。 |
| Log4j 2 |  Log4j 2 |  Log4j 2 是 Log4j 的升级版。 |
| Logback |  Logback |  Logback 是一个开源日志组件。SOFABoot 默认使用 SLF4J + Logback 日志框架。 |
| Maven |  Maven |  Apache Maven 是一个项目管理和构建自动化工具，为开发者提供了一套完整的构建生命周期框架，开发团队几乎不用花多少时间就能够自动完成工程的基础构建配置。 |
| RpcId |  RpcId |  RpcId 代表了本次请求在整个调用链路中的位置，比如 A 系统在处理一个请求的过程中依次调用了 B，C，D 三个系统，那么这三次调用的 RpcId 分别是：0.1，0.2，0.3。如果 B 系统继续调用了 E，F 两个系统，那么这两次调用的 RpcId 分别是：0.1.1，0.1.2。 |
| SOFA |  SOFA |  Scalable Open Financial Architecture，简称 SOFA，是蚂蚁金服自主研发的金融级分布式中间件框架。 |
| SOFABoot |  SOFABoot |  基于 Spring Boot 的中间件轻量集成方案，与标准的 Spring Boot 工程无缝集成，集成了蚂蚁金服全套金融级中间件。 |
| SOFALite |  SOFALite |  基于 Spring 的中间件集成框架，可与标准的 Spring 工程无缝集成。 |
| SOFAREST |  SOFAREST |  SOFAREST 是一种基于 JAX-RS（Java API for RESTful Web Services）标准的 SOA（Service-Oriented Architecture）解决方案。 |
| SOFARPC |  SOFARPC |  SOFARPC 提供应用之间的点对点服务调用功能。 |
| Spring Boot |  Spring Boot |  Spring Boot 是一种用于简化 Spring 应用的初始搭建以及开发过程的框架，该框架使用了特定的方式来进行配置，从而使开发人员不再需要定义样板式的配置。 |
| Spring Cloud |  Spring Cloud |  Spring Cloud 是一系列框架的集合，利用 Spring Boot 简化了分布式系统基础设施的开发，如服务发现注册、配置中心、消息总线、负载均衡、断路器、数据监控等，都可以用 Spring Boot 的开发风格做到一键启动和部署。 |
| Starter |  Starter |  Spring Boot/SOFABoot 的启动器，可快速接入内嵌的功能模块。 |
| Tengine |  Tengine |  由淘宝网发起的 Web 服务器项目。它在 Nginx 的基础上，针对大访问量网站的需求，添加了很多高级功能和特性。 |
| Tomcat |  Tomcat |  主要是作为 Java servlet/JSP 容器，也有许多传统 Web 服务器的性能。 |
| TraceId |  TraceId |  TraceId 指的是 Tracer 中代表唯一一次请求的 ID，此 ID 一般由集群中第一个处理请求的系统产生。 |
| Tracer |  Tracer |  标识整个请求链，即一些列 Span 的组合。其自身的 ID 将贯穿整个调用链，其中的每个 Span 都必须携带这个 traceId，因此 traceId 将在整个调用链中传递。 |
| 定时任务 |  Scheduling Task |  定时任务服务为业务系统提供统一通用的任务调度服务，提供定时任务的管理监控平台。 |
| 动态配置 |  Dynamic Configuration |  微服务的模块之一，是一个配置管理框架，可以在分布式环境下，动态管理应用集群配置参数。 |
| 分布式链路跟踪 |  Distributed System Tracing |  分布式链路跟踪是一款实时监控并管理企业应用性能和故障的云服务。 |
| 分布式事务 |  Distributed Transaction-eXtended |  蚂蚁金服自主研发的金融级分布式事务中间件，用来保障在大规模分布式环境下业务活动的最终一致性。 |
| 数据访问代理 |  Database Proxy |  蚂蚁金服自主研发的金融级分布式数据库中间件，用于解决海量请求下数据访问的瓶颈及数据库的容灾问题，提供水平拆分、平滑扩缩容、读写分离的在线分布式数据库服务。 |
| 微服务 |  Microservices |  主要提供分布式应用常用解决方案，包含 RPC 服务、定时任务调度服务、动态配置等。 |
| 消息队列 |  Message Queue |  消息代理组件，主要应用于分布式系统或组件之间的消息通讯。 |


引用:[https://www.jianshu.com/p/e3dca8d5e9ee](https://www.jianshu.com/p/e3dca8d5e9ee)
