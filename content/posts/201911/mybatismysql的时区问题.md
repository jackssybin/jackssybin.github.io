title: mybatis,mysql的时区问题
date: '2019-11-07 17:48:47'
updated: '2019-11-07 17:49:21'
tags: [java, json时间转换]
permalink: /articles/2019/11/07/1573120127531.html
---
#### 1.公司运营装mysql的时候的时区不是固定的，随机的，所以我们要想办法解决这个问题，应该运营的权限控制的很严，不能要他们更改；
首先解决从数据库读取到java，指定我们所需要的时区，只需要在配置文件的mysql链接的时候指定自己所需的文
```
datasource.jdbcUrl=jdbc:mysql://xxx.xx.xx.xx:3306/bms?characterEncoding=UTF-8&useSSL=false&serverTimezone=Asia/Shanghai
```

#### 2.如果我们写接口的时候使用的JsonFormat注解的时候，我们也需要指定想同的时区，否则又会出现时区误差

```
@JsonFormat(pattern = ApplicationConstants.DATE_FORMAT,timezone="GMT+8")
```