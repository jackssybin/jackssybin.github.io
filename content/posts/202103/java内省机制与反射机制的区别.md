title: java内省机制与反射机制的区别
date: '2021-03-29 14:50:16'
updated: '2021-03-29 14:50:16'
tags: [java反射, java内省, reflect, Introspector]
permalink: /articles/2021/03/29/1617000615780.html
---
### 概念上的区别

**反射**是在运行状态把Java类中的各种成分映射成相应的Java类，可以动态的获取所有的属性以及动态调用任意一个方法，强调的是运行状态。
**内省(IntroSpector)** 是Java 语言对 JavaBean（简称VO）类属性、事件的一种缺省处理方法。内省机制是通过反射来实现。例如类User中有属性name，那么必定有getName，setName方法，我们可以通过他们来获取或者设置值。Java提供了一套API来访问某个属性的getter/setter方法，这些API存放在java.beans中。
内省涉及的类

* Introspector
* BeanInfo
* PropertyDescriptor

#### 实现内省的步骤

1. 通过类 Introspector 的 getBeanInfo方法 来获取某个对象的 BeanInfo 信息。
2. 通过 BeanInfo 来获取属性描述器(PropertyDescriptor)。
3. 通过获取的属性描述器就可以获取某个属性对应的 getter/setter 方法。
4. 通过反射机制调用获取到的getter/setter 方法。
5. 

测试User类;

```
/**
 * 实体类
 */
public class User {

    private String name;
    private Integer age;
    private String address;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }
}
```

#### 1、反射操作name属性

```
/**
 * 反射测试类
 */
public class AnnoTest {
    private User user ;

    @Before
    public void init() {
        user = new User() ;
        user.setName("小明") ;
        user.setAge(18) ;
    }

    @Test
    public void getUserNameByAnno() throws NoSuchFieldException, IllegalAccessException {
        System.out.println("修改前的小明的年龄："+user.getAge());
        Field field = user.getClass().getDeclaredField("age");
        //暴力破解
        field.setAccessible(true);
        //设置属性值
        field.set(user, 38);
        //获取属性值
        Integer age = (Integer)field.get(user);
        System.out.println("修改后的小明的年龄："+age);
    }
}
```

#### 2、内省操作name属性

```
/**
 * 内省测试类
 */
public class IntrospectorTest {
    private User user ;

    @Before
    public void init() {
        user = new User() ;
        user.setName("小明") ;
        user.setAge(18) ;
    }

    /**
     * 获取实体类的属性信息
     * @throws Exception
     */
    @Test
    public void getBeanPropertyInfo() throws Exception {
        /**
         * 获取User-BeanInfo对象
         *      1、Introspector类
         *              是一个工具类，提供了一系列取得BeanInfo的方法；
         *      2、BeanInfo接口
         *              对一个JavaBean的描述，可以通过它取得Bean内部的信息；
         *      3、PropertyDescriptor属性描述器类
         *              对一个Bean属性的描述，它提供了一系列对Bean属性进行操作的方法
         */
        BeanInfo userBeanInfo = Introspector.getBeanInfo(User.class) ;
        PropertyDescriptor[] pds = userBeanInfo.getPropertyDescriptors() ;
        for (PropertyDescriptor pd : pds) {
            Method method = pd.getReadMethod() ;
            String methodName = method.getName() ;
            Object result = method.invoke(user) ;
            System.out.println(methodName + "：" + result);
        }
    }

    /**
     * 获取指定属性名称的属性描述器，并对属性进行操作
     * @throws Exception
     */
    @Test
    public void getBeanPropertyByName() throws Exception {
        //获取name属性的属性描述器
        PropertyDescriptor pd = new PropertyDescriptor("age", user.getClass()) ;
        //得到name属性的getter方法
        Method readMethod = pd.getReadMethod() ;
        //执行getter方法，获取返回值，即age属性的值
        Integer result = (Integer) readMethod.invoke(user) ;
        System.out.println("修改前小明的年龄" + "：" + result);
        //得到name属性的setter方法
        Method writeMethod = pd.getWriteMethod() ;
        //执行setter方法，修改age属性的值
        writeMethod.invoke(user, 38) ;
        System.out.println("修改后小明的年龄" + "：" + user.getAge());
    }
}
```


