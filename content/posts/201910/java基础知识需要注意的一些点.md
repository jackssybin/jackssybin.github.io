title: java基础知识需要注意的一些点
date: '2019-10-16 18:07:07'
updated: '2019-10-21 18:04:27'
tags: [java, 面试]
permalink: /articles/2019/10/16/1571220427190.html
---
![](https://img.hacpai.com/bing/20191009.jpg?imageView2/1/w/960/h/540/interlace/1/q/100) 

### 1.看看Integer 你注意到了没
```
  @Test
    public void testInteger() {
        System.out.println(("----- testInteger method test ------"));
        Integer a =128;
        Integer b =128;
        System.out.println(a.equals(b));
        System.out.println(a==b);

        Integer c =127;
        Integer d =127;
        System.out.println(c.equals(d));
        System.out.println(c==d);
    }
``````
结果：
```
true
false
true
true
```
*为什么？*
Integer类型当正整数小于128时是在内存栈中创建值的，并将对象指向这个值，
 这样当比较两个栈引用时因为是同一地址引用两者则相等。
 当大于127时将会调用new Integer()，
 两个整数对象地址引用不相等了。
这就是为什么当值为128时不相等，当值为100时相等了。


###  2.看看 变量传值的问题

```
	 @Test
	public void testCheck() {
        System.out.println(("----- testCheck method test ------"));
        int total=0;
        paramCheck(total);
        System.out.println(total);

        String totalStr="";
        paramCheck(totalStr);
        System.out.println(totalStr);

        User user =new User("张三",12);
        paramCheck(user);
        System.out.println(user);

        java.util.Map map = new HashMap();
        paramCheck(map);
        System.out.println(map);

        java.util.List list = new ArrayList();
        paramCheck(list);
        System.out.println(list);
    }

private static void paramCheck(int total){

        if(total<1){
            total+=1;
        }
    }

    private static void paramCheck(String total){
        total="paramCheck";
    }

    private static void paramCheck(User user){
        user.setName("paramCheck");
    }

    private static void paramCheck(java.util.Map user){
        user.put("paramCheck","1");
    }

    private static void paramCheck(java.util.List user){
        user.add("paramCheck");
    }
`````````
结果：
```
----- testCheck method test ------
0
""
User(id=null, name=paramCheck, age=12, email=null, createDate=null)
{paramCheck=1}
[paramCheck]
```
为什么？
```
将一个基础类型变量作为形参传递赋值并不会改变参数原有的值，
但是如果将一个对象作为参数传递改变属性，对象的属性值就会随着改变。
因此total的值仍然为0
```
### 3.看看 数组转list的问题
```
@Test
    public void testArray() {
        System.out.println(("----- testArray method test ------"));
        String[] array =new String[]{"张三","李四","王五"};
        List<String> list= Arrays.asList(array);
        list.add("孙六");
        System.out.println(list.size());
    }
``````
结果：
```
java.lang.UnsupportedOperationException
	at java.util.AbstractList.add(AbstractList.java:148)
	at java.util.AbstractList.add(AbstractList.java:108)
	at com.jackssy.boot.JFullStack.test.base.IntegerTest.testArray(IntegerTest.java:84)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.junit.runners.model.FrameworkMethod$1.runReflectiveCall(FrameworkMethod.java:50)
	at org.junit.internal.runners.model.ReflectiveCallable.run(ReflectiveCallable.java:12)
	at org.junit.runners.model.FrameworkMethod.invokeExplosively(FrameworkMethod.java:47)
	at org.junit.internal.runners.statements.InvokeMethod.evaluate(InvokeMethod.java:17)
	at org.junit.runners.ParentRunner.runLeaf(ParentRunner.java:325)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:78)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:57)
	at org.junit.runners.ParentRunner$3.run(ParentRunner.java:290)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:71)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:288)
	at org.junit.runners.ParentRunner.access$000(ParentRunner.java:58)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:268)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:363)
	at org.junit.runner.JUnitCore.run(JUnitCore.java:137)
	at com.intellij.junit4.JUnit4IdeaTestRunner.startRunnerWithArgs(JUnit4IdeaTestRunner.java:68)
	at com.intellij.rt.execution.junit.IdeaTestRunner$Repeater.startRunnerWithArgs(IdeaTestRunner.java:47)
	at com.intellij.rt.execution.junit.JUnitStarter.prepareStreamsAndStart(JUnitStarter.java:242)
	at com.intellij.rt.execution.junit.JUnitStarter.main(JUnitStarter.java:70)
```
**为什么？**
因为将数组转换的列表其实不是我们经常使用的arrayList，
但只是数组中内部定义的一种数据结构类型，本质还是原数组而并非列表，
因此当向列表添加元素就会出现错误，这道题上当的兄弟不少吧。
使用iterator 去比较去删除，不会报错，其实用list.remove 删除list 数据也减少了的，如果把异常捕获的话，还是可以看到list的size变少了的，可以试试下面的代码
```
 @Test

    public void testListRemove() {
        System.out.println(("----- testListRemove method test ------"));
        String removeName="张三";
        List<String> list = new ArrayList();
        list.add(removeName);
        list.add("李四");
        list.add("王五");
        try {
            for(String name :list){
                if(removeName.equals(name)){
                    list.remove(name);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println("before:"+list.size());

        Iterator iterator =list.iterator();
        while(iterator.hasNext()){
            if(iterator.next().equals(removeName)){
                iterator.remove();
                System.out.println("清除对象");
            }
        }
        System.out.println("after:"+list.size());
    }
``````

### 4.试试 创建目录的
```
  @Test
    public void testMkdir() {
        System.out.println(("----- testMkdir method test ------"));
        String path ="d:/data22/testcreate";
        new File(path).mkdir();
        new File(path).mkdirs();
    }
``````
结果:
自己试一下把。
mkdirs()可以建立多级文件夹，
而mkdir()只会建立一级的文件夹。 这个主要依靠java底层调用操作系统的实现

###  5.试试 float 精度问题
```
@Test
    public void testFloat() {
        System.out.println(("----- testFloat method test ------"));
        Float totalMoney=100.6f;
        Float ownMoney=100~~~~.5f;
        Float leftMoney=totalMoney-ownMoney;
        System.out.println("剩余："+leftMoney);
    }
``````
结果
```
----- testFloat method test ------
剩余：0.099998474
```
为什么？
两个float类型数据相减会丢失精度，尾部带着常常的一串数字。
如果实际场景要做计算我给你两个思路：
第一可以用bigdecimal来计算，
第二先将单位做成整数再做除法。

###  6.试试Integer.Max_value 的问题
```
 public static final int END_NUMBER=Integer.MAX_VALUE;
 public static final int START_NUMBER=Integer.MAX_VALUE-2;
    @Test
    public void testMax() {
        System.out.println(("----- testMax method test ------"));
        int count=0;
        for(int i=START_NUMBER ;i<=END_NUMBER ;i++){
            count++;
        }
        System.out.println(count);
    }
``````
结果：一直再转啊转。然后debug发现，数据i 再最大值加1之后变成负数了。所以一直转。
Integer.MAX_VALUE加上1以后的数值是个坑


