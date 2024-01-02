title: Mysql-Limit 优化和数据重复
date: '2020-05-28 16:10:08'
updated: '2020-05-28 16:10:08'
tags: [mysql, orderby, 排序, limit]
permalink: /articles/2020/05/28/1590653407979.html
---
![](https://img.hacpai.com/bing/20200301.jpg?imageView2/1/w/960/h/540/interlace/1/q/100)

# limit 查询导出优化
## 耗时本质

mysql大数据量使用limit分页，随着页码的增大，查询效率越低下。
**1.当一个表数据有几百万的数据的时候成了问题！**

如 select * from table limit 0,10 这个没有问题 当 limit 200000,10 的时候数据读取就很慢

原因本质： 
1）limit语句的查询时间与起始记录（offset）的位置成正比 
2）mysql的limit语句是很方便，但是对记录很多:百万，千万级别的表并不适合直接使用。

例如： limit10000,20的意思扫描满足条件的10020行，扔掉前面的10000行，返回最后的20行，问题就在这里。 ​ LIMIT 2000000, 30 扫描了200万+ 30行，怪不得慢的都堵死了，甚至会导致磁盘io 100%消耗。 ​ 但是: limit 30 这样的语句仅仅扫描30行。
## 优化手段

干掉或者利用 limit offset,size 中的offset

不是直接使用limit，而是首先获取到offset的id然后直接使用limit size来获取数据
## 对limit分页问题的性能优化方法

利用表的覆盖索引来加速分页查询

覆盖索引:

就是select 的数据列只用从索引中就能获得，不必读取数据行。mysql 可以利用索引返回select列表中的字段，而不必根据索引再次读取数据文件，换句话说：**查询列要被所创建的索引覆盖**

因为利用索引查找有优化算法，且数据就在查询索引上面，不用再去找相关的数据地址了，这样节省了很多时间。另外Mysql中也有相关的索引缓存，在并发高的时候利用缓存就效果更好了。在我们的例子中，我们知道id字段是主键，自然就包含了默认的主键索引。

这次我们之间查询最后一页的数据（利用覆盖索引，只包含id列），如下：
```
#覆盖索引只包含id列 的时间显著优于 select * 不言而喻
select * from order_table where company_id = 1 and mark =0 order by id desc limit 200000 ,20;
select id from order_table where company_id = 1 and mark =0 order by id desc limit 200000 ,20;
```
那么如果我们也要查询所有列，有两种方法，一种是id>=的形式，另一种就是利用join，看下实际情况：
```
#两者用的都是一个原理嘛，所以效果也差不多
SELECT * FROM xxx WHERE ID > =(select id from xxx limit 1000000, 1) limit 20;
SELECT * FROM xxx a JOIN (select id from xxx limit 1000000, 20) b ON a.ID = b.id;
```

**2.order by + limit 在什么情况下会出现分页数据重复**
排序离不开算法，在关系型数据库中，往往会存在多种排序算法。通过 MySQL 的源码和官方文档介绍可以得知，它的排序规律可以总结如下：

当 order by 不能使用索引进行排序时，将使用排序算法进行排序；若排序内容能全部放入内存，则仅在内存中使用快速排序；若排序内容不能全部放入内存，则分批次将排好序的内容放入文件，然后将多个文件进行归并排序；若排序中包含 limit 语句，则使用堆排序优化排序过程。

其他如：PG，MariaDB，AliSQL，SQL Server 等排序算法方面差别不大。

根据上面的总结，当你的 order by limit 分页出现数据重复。比如，一个用户表，当使用 limit 5 后出现一个张三。再使用 limit 5,10 的时候，张三又出现了。注意，这两个张三是同一个人，id 是相同的。在这种情况下，你的 order by 肯定是没有使用索引的。因为使用了索引，就会进行索引排序。

根据官方文档显示，可以得出。上面的 SQL 使用了堆排序。因为，排序字段 没索引，所以没走索引排序；其二我们使用了 limit，所以最终使用了堆排序。而了解算法的朋友都知道，堆排序是不稳定的。

### 3.那么如何解决 order by limit 分页数据重复问题呢？方法有多种，我这里列举最常用的两种方法。

第一种就是，在排序中加上唯一值，比如主键 id，这样由于 id 是唯一的，就能确保参与排序的 key 值不相同。

第二种就是   避免使用堆排序，让 order by 根据索引来排序。说白了，就是 order by 后面的字段要有索引。
