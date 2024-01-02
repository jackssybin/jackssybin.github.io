title: Java反射生成对象
date: '2020-11-10 19:08:04'
updated: '2020-11-19 09:47:23'
tags: [java, 反射, 对象创建, 声明方法使用]
permalink: /articles/2020/11/10/1605006483827.html
---
![](https://b3logfile.com/bing/20190327.jpg?imageView2/1/w/960/h/540/interlace/1/q/100)

想要了解反射生成class和创建java对象，首先我们要了解什么是反射？

**一、什么是反射？**

Java反射说的是在运行状态中，对于任何一个类，我们都能够知道这个类有哪些方法和属性。对于任何一个对象，我们都能够对它的方法和属性进行调用。**我们把这种动态获取对象信息和调用对象方法的功能称之为反射机制。**

**二、反射生成Class的三种方式**

**1.第一种方式（利用getClass（）方法）**

```
User user = new User();
Class class= user.getClass();
```

**2.第二种方式（直接对象的.class）**

```
Class cla = User.class
```

****3.第三种方式（Class.forName()）****

```
Class cla = Class.forName("com.jackssy.User");
```

注意：此种方法通过对象的全路径来获取Class的，当对象不存在时，会出现ClassNotFoundException异常。详细的可以看下Class.forName()的底层代码。

**三、反射生成java对象的两种方式**

**1.第一种方式newInstance();**

`调用public``无参构造器 ，若是没有，则会报异常`

`Object o = clazz.newInstance();　`

`没有无参构造函数异常：`

**2.第二种方式：**

有带参数的构造函数的类，先获取到其构造对象，再通过该构造方法类获取实例：

/ /获取构造函数类的对象

Constroctor constroctor = User.class.getConstructor(String.class);

// 使用构造器对象的newInstance方法初始化对象

Object obj = constroctor.newInstance("name");

**四、使用reflectasm调用生成对象调用**
**1. 依赖**

```
<dependency>
            <groupId>com.esotericsoftware</groupId>
            <artifactId>reflectasm</artifactId>
            <version>1.11.9</version>
        </dependency>
```

**2.代码**

```
import com.esotericsoftware.reflectasm.MethodAccess;
import org.junit.Before;
import org.junit.Test;

import java.beans.BeanInfo;
import java.beans.IntrospectionException;
import java.beans.Introspector;
import java.beans.PropertyDescriptor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.math.BigDecimal;

public class TestInvoke {
private long times = 100000000L;//1 亿
//    private long times = 100_000L;
private SimpleBean bean;
private LcProduct lcProduct;
private String formatter = "%s %d times using %d ms";

@Before
public void setUp() throws Exception {
bean = new SimpleBean();
bean.setName("haoyifen");
lcProduct = new LcProduct();
lcProduct.setPrdCode("prdcode12");
lcProduct.setPrdType("prdtype12");
lcProduct.setTaCode("tacode12");
lcProduct.setPrdName("prdname12");
lcProduct.setCurrType("currtype123");
lcProduct.setNav(new BigDecimal("12"));
lcProduct.setTotNav(new BigDecimal("12"));
lcProduct.setInCome(new BigDecimal("12"));
lcProduct.setInComeUnit(new BigDecimal("12"));
lcProduct.setInComeRate(new BigDecimal("12"));

}

//直接通过Java的get方法
@Test
public void directGet() {
long start = System.currentTimeMillis();
for (long i = 0; i < times; i++) {
bean.getName();
}
long end = System.currentTimeMillis();
System.out.println((end-start));
}

//通过高性能的ReflectAsm库进行测试，仅进行一次methodAccess获取
@Test
public void reflectAsmGet() {
MethodAccess methodAccess = MethodAccess.get(SimpleBean.class);
long star = System.currentTimeMillis();
for (long i = 0; i < times; i++) {
methodAccess.invoke(bean, "getName");
}
long end = System.currentTimeMillis();
System.out.println((end - star) / 1000);
}
@Test
public void reflectAsmGetTest() {


MethodAccess methodAccess = MethodAccess.get(SimpleBean.class);
int index = methodAccess.getIndex("getName");

//        clock.start("获取方法");
//        Arrays.stream(methodAccess.getMethodNames()).forEach(xx-> {
//            if(xx.startsWith("get")){
////                System.out.print(xx+" :"+methodAccess.invoke(lcProduct,xx)+" ");;
//                methodAccess.invoke(lcProduct,xx);
//            }
//        });
//        clock.stop();
long start = System.currentTimeMillis();
methodAccess.invoke(bean, index);
for (long i = 0; i < times; i++) {

//            methodAccess.invoke(bean, index);
methodAccess.invoke(bean,"getName");

}
long end = System.currentTimeMillis();
System.out.println((end - start) );
}


//通过Java Class类自带的反射获得Method测试，仅进行一次method获取
@Test
public void javaReflectGet() throws Exception {
    Method getName = SimpleBean.class.getMethod("getName");


//        Arrays.stream(LcProduct.class.getMethods()).forEach(xx->{
//            if(xx.getName().startsWith("get")){
//                try {
//                    xx.invoke(lcProduct);
//                } catch (IllegalAccessException e) {
//                    e.printStackTrace();
//                } catch (InvocationTargetException e) {
//                    e.printStackTrace();
//                }
//            }
//        });


long start = System.currentTimeMillis();
    for (long i = 0; i < times; i++) {
        getName.invoke(bean);
    }
    long end = System.currentTimeMillis();
    System.out.println((end - start) );
}

//使用Java自带的Property属性获取Method测试，仅进行一次method获取
@Test
public void propertyGet() throws IllegalAccessException, NoSuchMethodException, InvocationTargetException, IntrospectionException {
    Method method = null;
    BeanInfo beanInfo = Introspector.getBeanInfo(SimpleBean.class);
    PropertyDescriptor[] propertyDescriptors = beanInfo.getPropertyDescriptors();
    for (PropertyDescriptor propertyDescriptor : propertyDescriptors) {
        if (propertyDescriptor.getName().equals("name")) {
            method = propertyDescriptor.getReadMethod();
            break;
        }
    }
    long start = System.currentTimeMillis();
    for (long i = 0; i < times; i++) {

        method.invoke(bean);
    }
    long end = System.currentTimeMillis();
    System.out.println((end - start) );
}

//BeanUtils的getProperty测试
@Test
public void beanUtilsGet() throws IllegalAccessException, NoSuchMethodException, InvocationTargetException {
    long start = System.currentTimeMillis();
    for (long i = 0; i < times; i++) {


//            BeanUtils.getProperty(bean, "name");
}
long end = System.currentTimeMillis();
System.out.println((end - start) );
}


@Test
public void allTest() throws Exception {
    javaReflectGet();
    reflectAsmGetTest();
    directGet();
}


}

public class SimpleBean {
private String name;
public String getName() {
return name;
}
public void setName(String name) {
this.name = name;
}
}

public class LcProduct {

private Long id;
private String prdCode;
private String prdType;
private String taCode;
private String prdName;
private String currType;

private BigDecimal nav = new BigDecimal(0).setScale(12);
private BigDecimal  totNav= new BigDecimal(0).setScale(12);;
private BigDecimal  inCome= new BigDecimal(0).setScale(12);
private BigDecimal  inComeUnit= new BigDecimal(0).setScale(12);
private BigDecimal  inComeRate= new BigDecimal(0).setScale(12);
private String batchCode;
private Boolean updateFlag;

private LocalDateTime createdAt;
private String createdBy;

private LocalDateTime updatedAt;
private String updatedBy;
}
//省略 getset方法
```

**3.结论**
每种方式执行1亿次运行结果如下：

* get耗时35ms
* 缓存反射耗时223ms
* reflectasm先拿到方法index反射耗时39ms
* reflectasm每次按照方法名查找然后反射耗时350ms
* reflectasm相比通过名称来访问成员，使用索引的方式会更快。如果需要重复地访问同一个成员，那么通过索引来访问该成员效率更高

**4.reflectasm原理为啥这么快**
jdk反射慢原因有三:
1.变长参数方法导致的 Object 数组
2.基本类型的自动装箱、拆箱
3.还有最重要的方法内联
reflectasm快原因:
ReflectASM是一个很小的java类库，主要是通过asm生产类来实现java反射。他的主要代码还是get方法，但是由于get方法源码比较多，就不在博客中贴出来了，大家可以自己点进去看。这里我们给出实现invoke的抽象方法。

```
// Decompiled by Jad v1.5.8g. Copyright 2001 Pavel Kouznetsov.  
// Jad home page: http://www.kpdus.com/jad.html  
// Decompiler options: packimports(3)   
  
package com.johhny.ra;  
  
import com.esotericsoftware.reflectasm.MethodAccess;  
  
// Referenced classes of package com.johhny.ra:  
//            User  
  
public class UserMethodAccess extends MethodAccess  
{  
  
    public UserMethodAccess()  
    {  
    }  
  
    /** 
     * 这个方法是主要是实现了MethodAccess 的抽象方法，来实现反射的功能   
     * @param obj  需要反射的对象 
     * @param i  class.getDeclaredMethods 对应方法的index 
     * @param 参数对象集合 
     * @return 
     */  
    public transient Object invoke(Object obj, int i, Object aobj[])  
    {  
        User user = (User)obj;  
        switch(i)  
        {  
        case 0: // '\0'  
            return user.getName();  
  
        case 1: // '\001'  
            return Integer.valueOf(user.getId());  
  
        case 2: // '\002'  
            user.setName((String)aobj[0]);  
            return null;  
  
        case 3: // '\003'  
            user.setId(((Integer)aobj[0]).intValue());  
            return null;  
        }  
        throw new IllegalArgumentException((new StringBuilder("Method not found: ")).append(i).toString());  
    }  
}
```

由代码可以看出来，实际上ReflectASM就是把类的各个方法缓存起来，然后通过case选择，直接调用，因此速度会快上很多。但是它的get方法同样会消耗很大的时间，因此就算是使用ReflectASM的朋友也记得请在启动的时候就初始化get方法计入缓存

##### 读写字段

通过 FieldAccess 可以读写类的字段：

```
SomeClass someObject = // ...
FieldAccess access = FieldAccess.get(SomeClass.class);
access.set(someObject, "name", "Huey");
String name = (String) access.get(someObject, "name");
assertEquals(name, "Huey");
```

##### 调用方法

通过 MethodAccess 可以调用对象实例的方法：

```
SomeClass someObject = // ...
MethodAccess access = MethodAccess.get(SomeClass.class);
access.invoke(someObject, "setName", "Huey");
String name = (String) access.invoke(someObject, "getName");
assertEquals(name, "Huey");
```

##### 构造实例

通过 ConstructorAccess 可以构造对象实例：

```
ConstructorAccess access = ConstructorAccess.get(SomeClass.class);
SomeClass someObject = access.newInstance();
// do something with someObject.
```

##### 索引

相比通过名称来访问成员，使用索引的方式会更快。如果需要重复地访问同一个成员，那么通过索引来访问该成员效率更高：

```
String[] names = // ...
SomeClass someObject = // ...
MethodAccess access = MethodAccess.get(SomeClass.class);
int addNameIndex = access.getIndex("addName");
for (String name : names) {
    access.invoke(someObject, addNameIndex, name);
}
```

##### 遍历字段

遍历一个类的所有字段：

```
FieldAccess access = FieldAccess.get(SomeClass.class);
for(int i = 0, n = access.getFieldCount(); i < n; i++) {
    access.set(instanceObject, i, valueToPut);              
}
```

