title: SpringBoo2t获取ApplicationContext的3种方式
date: '2020-12-29 08:51:39'
updated: '2020-12-29 08:51:39'
tags: [springboot上下文, springboot获取bean]
permalink: /articles/2020/12/29/1609203099106.html
---
![](https://b3logfile.com/bing/20190412.jpg?imageView2/1/w/960/h/540/interlace/1/q/100)

**ApplicationContext是什么？**

简单来说就是Spring中的容器，可以用来获取容器中的各种bean组件，注册监听事件，加载资源文件等功能。

Application Context获取的几种方式

1 直接使用Autowired注入

```
@Component
public class Book1 {

 @Autowired
 private ApplicationContext applicationContext;

 public void show (){
  System.out.println(applicationContext.getClass());
 }
}
```


2 利用 spring4.3 的新特性

使用spring4.3新特性但是存在一定的局限性，必须满足以下两点：

1. 构造函数只能有一个，如果有多个，就必须有一个无参数的构造函数，此时，spring会调用无参的构造函数
2. 构造函数的参数，必须在spring容器中存在

```
@Component
public class Book2 {

 private ApplicationContext applicationContext;

 public Book2(ApplicationContext applicationContext){
  System.out.println(applicationContext.getClass());
  this.applicationContext=applicationContext;
 }

 public void show (){
  System.out.println(applicationContext.getClass());
 }

}
```

3 实现spring提供的接口 ApplicationContextAware

spring 在bean 初始化后会判断是不是ApplicationContextAware的子类，调用setApplicationContext（）方法， 会将容器中ApplicationContext传入进去

```
@Component
public class Book3 implements ApplicationContextAware {

 private ApplicationContext applicationContext;

 public void show (){
  System.out.println(applicationContext.getClass());
 }

 @Override
 public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
  this.applicationContext = applicationContext;
 }
}
```

结果获取三次：

```
class org.springframework.context.annotation.AnnotationConfigApplicationContext
class org.springframework.context.annotation.AnnotationConfigApplicationContext
class org.springframework.context.annotation.AnnotationConfigApplicationContext
```

