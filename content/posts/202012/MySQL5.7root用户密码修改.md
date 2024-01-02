title: MySQL 5.7root用户密码修改
date: '2020-12-16 13:45:23'
updated: '2020-12-16 13:45:23'
tags: [mysql, 更新密码, root密码]
permalink: /articles/2020/12/16/1608097523728.html
---
![](https://b3logfile.com/bing/20180226.jpg?imageView2/1/w/960/h/540/interlace/1/q/100)

在MySQL 5.7 password字段已从mysql.user表中删除，新的字段名是“authenticalion_string”.

选择数据库：use mysql;

更新root的密码：

```
update user set authentication_string=password('新密码') where user='root' and Host='localhost';

flush privileges;
```

