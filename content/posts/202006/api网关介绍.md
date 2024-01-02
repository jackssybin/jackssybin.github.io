title: api网关介绍
date: '2020-06-14 13:22:54'
updated: '2020-06-20 10:46:06'
tags: [gateway, zuul, 网关]
permalink: /articles/2020/06/14/1592112174081.html
---
![](https://img.hacpai.com/bing/20190106.jpg?imageView2/1/w/960/h/540/interlace/1/q/100) 

## 1.什么是网关
API网关是一个系统的唯一入口。
是众多分布式服务唯一的一个出口。
它做到了物理隔离,内网服务只有通过网关才能暴露到外网被别人访问。
简而言之:网关就是你家的大门

## 2.提供了哪些功能
1. 身份认证(oauth2/jwt)
2. 权限安全(黑白名单/爬虫控制)
3. 流量控制(请求大小/速率)
4. 数据转换(公共请求request/response)
5. 监控/metrics
6. 跨域问题(前后端分离)
7. 灰度发布(金丝雀发布/一部分去老客户端/一部分去新客户端)

## 3.市面上有哪些比较好的开源网关
1. [OpenResty](http://openresty.org/cn/)
2. [kong](https://konghq.com/)
3. [Spring Cloud Zuul/Gateway](https://spring.io/blog/2019/06/18/getting-started-with-spring-cloud-gateway)
4. [Zuul2](https://github.com/Netflix/zuul)

| 网关 |  限流 |  鉴权 |  监控 |  易用性 |  可维护性 |  成熟度 |
| :-- |  :-- |  :-- |  :-- |  :-- |  :-- |  :-- |
| Spring Cloud Gateway |  可以通过IP，用户，集群限流，提供了相应的接口进行扩展 |  普通鉴权、auth2.0 |  Gateway Metrics Filter |  简单易用 |  spring系列可扩展强，易配置 可维护性好 |  spring社区成熟，但gateway资源较少 |
| Zuul2 |  可以通过配置文件配置集群限流和单服务器限流亦可通过filter实现限流扩展 |  filter中实现 |  filter中实现 |  参考资料较少 |  可维护性较差 |  开源不久，资料少 |
| OpenResty |  需要lua开发 |  需要lua开发 |  需要开发 |  简单易用，但是需要进行的lua开发很多 |  可维护性较差，将来需要维护大量lua脚本 |  很成熟资料很多 |
| Kong |  根据秒，分，时，天，月，年，根据用户进行限流。可在原码的基础上进行开发 |  普通鉴权，Key Auth鉴权，HMAC，auth2.0 |  可上报datadog，记录请求数量，请求数据量，应答数据量，接收于发送的时间间隔，状态码数量，kong内运行时间 |  简单易用，api转发通过管理员接口配置，开发需要lua脚本 |  "可维护性较差，将来需要维护大量lua库 |  相对成熟，用户问题汇总，社区，插件开源 |



## 4.如何做一款网关(Spring Cloud Gateway)

1. 第一个网关
pom.xml

```
<dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-gateway</artifactId>
</dependency>
```
Application.java

```
@SpringBootApplication
public class GatewayApplication {

    public static void main(String[] args) {
        SpringApplication.run(GatewayApplication.class, args);
    }
    
    // 等同于在yml文件中的配置
    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes().route(r -> r.path("/test/aa")
                .uri("http://www.baidu.com"))
                .route(r -> r.path("/baidu")
                        .uri("http://www.baidu.com"))
                .route(r -> r.path("/testa/**")
                        .uri("lb://servicea"))
                .build();
    }
}
```


#启动参数 支持的路由方式

```
Loaded RoutePredicateFactory [After]
2020-06-12 11:39:21.811  INFO 3680 --- [           main] o.s.c.g.r.RouteDefinitionRouteLocator    : Loaded RoutePredicateFactory [Before]
2020-06-12 11:39:21.811  INFO 3680 --- [           main] o.s.c.g.r.RouteDefinitionRouteLocator    : Loaded RoutePredicateFactory [Between]
2020-06-12 11:39:21.811  INFO 3680 --- [           main] o.s.c.g.r.RouteDefinitionRouteLocator    : Loaded RoutePredicateFactory [Cookie]
2020-06-12 11:39:21.811  INFO 3680 --- [           main] o.s.c.g.r.RouteDefinitionRouteLocator    : Loaded RoutePredicateFactory [Header]
2020-06-12 11:39:21.812  INFO 3680 --- [           main] o.s.c.g.r.RouteDefinitionRouteLocator    : Loaded RoutePredicateFactory [Host]
2020-06-12 11:39:21.812  INFO 3680 --- [           main] o.s.c.g.r.RouteDefinitionRouteLocator    : Loaded RoutePredicateFactory [Method]
2020-06-12 11:39:21.812  INFO 3680 --- [           main] o.s.c.g.r.RouteDefinitionRouteLocator    : Loaded RoutePredicateFactory [Path]
2020-06-12 11:39:21.812  INFO 3680 --- [           main] o.s.c.g.r.RouteDefinitionRouteLocator    : Loaded RoutePredicateFactory [Query]
2020-06-12 11:39:21.812  INFO 3680 --- [           main] o.s.c.g.r.RouteDefinitionRouteLocator    : Loaded RoutePredicateFactory [ReadBodyPredicateFactory]
2020-06-12 11:39:21.812  INFO 3680 --- [           main] o.s.c.g.r.RouteDefinitionRouteLocator    : Loaded RoutePredicateFactory [RemoteAddr]
2020-06-12 11:39:21.812  INFO 3680 --- [           main] o.s.c.g.r.RouteDefinitionRouteLocator    : Loaded RoutePredicateFactory [Weight]
2020-06-12 11:39:21.812  INFO 3680 --- [           main] o.s.c.g.r.RouteDefinitionRouteLocator    : Loaded RoutePredicateFactory [CloudFoundryRouteService]
```
![路由方式](https://springcloud-oss.oss-cn-shanghai.aliyuncs.com/chapter12/spring-cloud-gateway3.png)



# 开启端点检查

访问url:
http://localhost:9002/actuator/gateway/routes

pom.xml添加
```
 <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
```
#yml 添加配置 端点打开

```
management:
  endpoints:
    web:
      exposure:
        include: "*"
```

# 参考
代码位置:
[https://github.com/jackssybin/springclouditems.git](https://github.com/jackssybin/springclouditems.git)



