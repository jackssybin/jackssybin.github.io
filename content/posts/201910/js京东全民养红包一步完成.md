title: js京东全民养红包一步完成
date: '2019-10-29 14:15:36'
updated: '2019-10-30 10:23:41'
tags: [js]
permalink: /articles/2019/10/29/1572329735795.html
---
![](https://img.hacpai.com/bing/20180403.jpg?imageView2/1/w/960/h/540/interlace/1/q/100) 

## 京东喜迎双十一

这个活动和`天猫`的活动几乎可以说很像了，都是浏览商家店铺获取金币，  
可是这样进度太慢了。于是浏览的大佬的贴子，终于找到可以一键完成养红包的所有任务了。

## 使用步骤
### 一、打开谷歌浏览或者火狐也浏览也行（支持开发者模式），按 F12

进入，切换手机模式如图：  
![TIM截图20191029134216.png](https://img.hacpai.com/file/2019/10/TIM%E6%88%AA%E5%9B%BE20191029134216-0ae9670a.png?imageView2/2/interlace/1/format/webp)

738 x 395 1366 x 732

### 二、进入京东官网

1.登入你的京东账号：[http://www.jd.com](http://www.jd.com)

2.进入活动页面：[https://happy.m.jd.com/babelDiy/GZWVJFLMXBQVEBDQZWMY/XJf8bH6oXDWSgS91daDJzXh9bU7/index.html](https://happy.m.jd.com/babelDiy/GZWVJFLMXBQVEBDQZWMY/XJf8bH6oXDWSgS91daDJzXh9bU7/index.html)

### 三、使用 js 脚本

把脚本复制到 Console 点击回车就可以看见任务在自动完成  
下面是脚本代码：

```
let productList = [], shopList = [], url = "https://api.m.jd.com/client.action";
function autoPost(id,type){
        fetch(`${url}?timestamp=${new Date().getTime()}`,{method: "POST",mode: "cors",credentials: "include",headers:{"Content-Type": "application/x-www-form-urlencoded"},body:`functionId=raisepacket_collectScore&body={"type":${type},"ext":"${id}","appsign":1,"msgsign":2}&client=wh5`})
                .then(function(response){return response.json()})
                .then(function(res){
                        console.log(res.data.biz_msg);
                });
}
 
function start(){
        fetch(`${url}?${new Date().getTime()}`,{method: "POST",mode: "cors",credentials: "include",headers:{"Content-Type": "application/x-www-form-urlencoded"},body:'functionId=raisepacket_getShopAndProductList&body=&client=wh5'})
                .then(function(response){return response.json()})
                .then(function(res){
                        productList = res.data.result.productList;
                        shopList  = res.data.result.shopList;
                        console.log(`获取到任务,商品：${productList.length} 商品：${shopList.length}`);
                        autoProductTask();
                });
}
//逛商品
function autoProductTask(){
        for(let i = 0,leng = productList.length;i<leng;i++){
                (function(index){
                        setTimeout(()=>{
                                let item = productList[index];
                                autoPost(item['id'],4);
                                console.log(`商品总任务数：${leng} 当前任务数：${index + 1}`);
                                if( leng-1 == index){
                                        autoShopTask();
                                }
                        },index*1500)
                })(i)        
        }
}
//逛店铺
function autoShopTask(){
        for(let i = 0,leng = shopList.length;i<leng;i++){
                (function(index){
                        setTimeout(()=>{
                                let item = shopList[index];
                                autoPost(item['id'],2);
                                console.log(`商铺总任务数：${leng} 当前任务数：${index + 1}`);
                                if( leng-1 == index){
                                        autoPlay();
                                }
                        },index*1500)
                })(i)        
        }
}
//好玩互动
function autoPlay(){
        for(let i = 0,leng = 4;i<leng;i++){
                (function(index){
                        setTimeout(()=>{
                                autoPost(0,5);
                                console.log(`好玩互动：${leng} 当前任务数：${index + 1}`);
                                if( leng-1 == index){
                                        autoInteract();
                                }
                        },index*1000)
                })(i)        
        }
}
//视频直播
function autoInteract(){
        for(let i = 0,leng = 4;i<leng;i++){
                (function(index){
                        setTimeout(()=>{
                                autoPost(0,10);
                                console.log(`视频直播：${leng} 当前任务数：${index + 1}`);
                                if( leng-1 == index){
                                        autoShopping();
                                }
                        },index*1000)
                })(i)        
        }
}
//精彩会场
function autoShopping(){
        for(let i = 0,leng = 3;i<leng;i++){
                (function(index){
                        setTimeout(()=>{
                                autoPost(0,3);
                                console.log(`精彩会场：${leng} 当前任务数：${index + 1}`);
                                },
                        index*1000)
                })(i)        
        }
}
start();


```
脚本运行后就会是下面的样子，因为我今天的任务已经完成了，所以显示是完成的：
![image.png](https://img.hacpai.com/file/2019/10/image-ddd20588.png)

 转载：https://www.52pojie.cn/thread-1042796-1-1.html
