title: mysql允许远程连接
date: '2019-11-13 23:07:22'
updated: '2019-11-13 23:07:22'
tags: [mysql]
permalink: /articles/2019/11/13/1573657642163.html
---
##### 1.本地登陆 赋权
```
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '密码' WITH GRANT OPTION;
 FLUSH PRIVILEGES;
```
##### 2. 修改本地绑定端口
```
/etc/mysql/**mysql.cnf
查找bind 127.0.0.1 注释掉即可
```