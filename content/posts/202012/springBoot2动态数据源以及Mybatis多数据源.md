title: springBoot2动态数据源以及Mybatis多数据源
date: '2020-12-25 09:55:26'
updated: '2020-12-25 09:55:26'
tags: [mybaits-plus, 动态数据源, 切换数据源, springboot2]
permalink: /articles/2020/12/25/1608861326670.html
---
![](https://b3logfile.com/bing/20201008.jpg?imageView2/1/w/960/h/540/interlace/1/q/100)

## 一、前言

由于项目中读写分离，或者分库分表导致数据库连接有很多。这个时候我们常常会切换多数据源进行业务的合并。mybatis-plus 团队新增了dynamic-datasource-spring-boot-starter 用来动态切换数据源。

```
<dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>dynamic-datasource-spring-boot-starter</artifactId>
            <version>3.1.0</version>
        </dependency>
```

## 二、配置

##### 2.1pom配置

```
<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-webflux</artifactId>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid-spring-boot-starter</artifactId>
            <version>1.1.10</version>
        </dependency>
        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-boot-starter</artifactId>
            <version>3.1.0</version>
        </dependency>
        <!-- mybatis plus 代码生成器依赖 -->
        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-generator</artifactId>
            <version>3.1.0</version>
        </dependency>

        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>dynamic-datasource-spring-boot-starter</artifactId>
            <version>3.1.0</version>
        </dependency>
        <!-- 代码生成器模板 -->
        <dependency>
            <groupId>org.freemarker</groupId>
            <artifactId>freemarker</artifactId>
        </dependency>
```

##### 禁用DataSourceAutoConfiguration

如果DataSourceAutoConfiguration不禁用的话，就会报错，多个数据源，无法装配哪一个。在springBoot的主程序入口的注解

```
@SpringBootApplication(exclude = {DruidDataSourceAutoConfigure.class})
```

##### 配置yml

```
spring:
  datasource:
    druid:
      web-stat-filter:
        enabled: false
      stat-view-servlet:
        enabled: false
      filters: stat
      #配置初始化大小/最小/最大
      initial-size: 1
      min-idle: 1
      max-active: 20
      #获取连接等待超时时间
      max-wait: 60000
      #间隔多久进行一次检测，检测需要关闭的空闲连接
      time-between-eviction-runs-millis: 60000
      #一个连接在池中最小生存的时间
      min-evictable-idle-time-millis: 300000
      validation-query: SELECT 'x'
      test-while-idle: true
      test-on-borrow: false
      test-on-return: false
      #打开PSCache，并指定每个连接上PSCache的大小。oracle设为true，mysql设为false。分库分表较多推荐设置为false
      pool-prepared-statements: false
      max-pool-prepared-statement-per-connection-size: 20
    # dynamic-datasource-spring-boot-starter 动态数据源的配置内容
    dynamic:
      primary: master # 设置默认的数据源或者数据源组，默认值即为 master
      strict: false #设置严格模式,默认false不启动. 启动后在未匹配到指定数据源时候回抛出异常,不启动会使用默认数据源.
      datasource:
        # 订单 orders 数据源配置
        master:
          url: jdbc:mysql://127.0.0.1:3306/nprsc?characterEncoding=utf-8&autoReconnect=true&failOverReadOnly=false&useSSL=true
          username: root
          password: root1234
          driver-class-name: com.mysql.cj.jdbc.Driver
        # 用户 users 数据源配置
        db2:
          url: jdbc:mysql://127.0.0.1:3306/test?characterEncoding=utf-8&autoReconnect=true&failOverReadOnly=false&useSSL=true
          username: root
          password: root1234
          driver-class-name: com.mysql.cj.jdbc.Driver
```

##### 使用 **@DS** 切换数据源。

**@DS** 可以注解在方法上和类上，**同时存在方法注解优先于类上注解**。

没有@DS 走默认数据源，（primary: master # 设置默认的数据源或者数据源组，默认值即为 master
）
如果有根据DS的内容走。

```
@GetMapping("/users")
    @ResponseBody
    @DS("db2")
    public String users(){
        System.out.println("hello users =========");
        System.out.println(bzComponentMapper.getProoduct("prd001"));
        return "hello users";
    }

    @GetMapping("/master")
    @ResponseBody
    @DS("master")
    public String master(){
        System.out.println("hello master =========");
        System.out.println(bzComponentMapper.getProoduct("prd001"));
        return "master";
    }
```

官网地址: [https://baomidou.com/guide/dynamic-datasource.html](https://baomidou.com/guide/dynamic-datasource.html)




