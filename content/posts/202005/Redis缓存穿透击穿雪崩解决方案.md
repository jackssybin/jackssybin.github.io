title: Redis缓存穿透/击穿/雪崩解决方案
date: '2020-05-28 16:56:09'
updated: '2020-05-28 16:56:09'
tags: [Redis缓存穿透, 缓存穿透, 缓存击穿, 缓存雪崩]
permalink: /articles/2020/05/28/1590656168798.html
---
### Redis缓存穿透/击穿/雪崩

在平常开发时，我们一般都会引入redis，memcache等这些缓存解决方案来做一些热点数据存储来减轻数据库的压力，相较于数据库的磁盘IO，类似redis这种内存型数据库，内存的IO效率要比磁盘IO效率高几个数量级。但是在真正面对高并发时，如果处理不当redis也会出现一些问题。这里就说一下实际场景中可能会出现的缓存穿透，缓存击穿，缓存雪崩。

* 1. 缓存穿透：比如说，一个用户的基本信息(缓存key为uid)或订单的信息(缓存key为order_id)，缓存或数据库里都没有这个uid或order_id的信息，但是如果有请求要获取这个信息，那么逻辑处理时就会跨过缓存这一层去查数据库，如果这样的请求短时间内非常多可能会压垮数据库。
    
* 2. 缓存击穿：比如说，订单的信息(缓存key为order_id)在缓存中有过期时间，如果在特定的时间这个订单信息在缓存中已经过期但是尚未从数据库查出最新的信息set到缓存上，恰好这个时候大并发请求过来了，那么这些请求的逻辑处理也会跨过缓存直接查询数据库，这个大并发的查询可能会压垮数据库。
    
* 3. 缓存雪崩：上面说到缓存击穿是一个key在特定时间过期，那么如果缓存系统中大量的缓存在同一时间或时间段内过期，这个时候的请求也会跨过缓存直达数据库，数据库压力陡增也可能会压垮数据库。

### 解决方案

1. 缓存穿透解决方案有很多
    

* 设计一个过滤器，常用的是布隆过滤器，移步这里了解更多 [大白话布隆过滤器](https://www.cnblogs.com/CodeBear/p/10911177.html "大白话布隆过滤器")。
    
* 给不存在的key，赋值一个默认的空值，如下代码
    

public function getCache($key) {
        $redis =  Helper::redis(); //redis对象
        $expire_time = 300;
        $result = $redis->get($key);
        if ($result) {
            return $result;
        }else {
            //redis里没查到，去查db
            $db_data = queryDb($key);//模拟查询db,拿到的数据
            if ($db_data) {
                //数据库查到的数据，正常，更新缓存key数据，返回数据
                $redis->set($key, $db_data, $expire_time);
                return $db_data;
            }else {
                //数据库查不到该$key对应的数据，设置一个默认值，更新缓存key数据，返回数据
                $db_data = 'empty data';
                $redis->set($key, $db_data, $expire_time);
                return $db_data;
            }
            //上面的代码，精简一下
            $db_data = $db_data ?: 'empty data';
            $redis->set($key, $db_data, $expire_time);
            return $db_data;          
        }
    }

4. 缓存击穿解决方案多使用 互斥锁，使用mutex。就是在缓存失效的时候，在去数据库查询最新的数据前，上一个锁(同时间的其他获取缓存操作就会被阻塞，这个阻塞只会只会影响很小的一部分请求)，然后再去完成数据查询，缓存更新等操作。
    

public function getCache($key) {
        $redis =  Helper::redis(); //redis对象
        $expire_time = 300;
        $result = $redis->get($key);
        if ($result) {
            return $result;
        }else {
            //redis里没查到，去查db
            $mutex_key = $key . '_mutex';
            //这里假设同时有10个查询的线程，1个线程抢到了这个锁，其他的9个线程就会阻塞或需要等待
            if ($redis->setnx($mutex_key, 1, 60)) {
                //抢到锁的线程，去执行数据查询，更新缓存这些操作
                $db_data = queryDb($key);//模拟查询db,拿到的数据
                $result = $db_data ?: 'empty data';
                $redis->set($key, $result, $expire_time);
                $redis->del($mutex_key);
            }else {
                //没抢到锁的线程，就“稍等”一会啦，然后再获取最新的缓存数据
                sleep(0.01);
                $result = getCache($key);
            }                    
            return $result;          
        }
    }

6. 缓存雪崩的话，短时间的大量数据读写操作极大可能导致数据库垮掉。为了避免出现这种情况，可以在常规的缓存set操作的基础上，在预设的过期时间基础上再额外增加一些时间；也可以单独起一个进程去监控redis中快过期的key,如果有快过期的key，就去重新查询更新。
