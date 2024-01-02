title: MySQL Transaction--RR事务隔离级别下加锁测试
date: '2021-06-08 09:47:41'
updated: '2022-11-09 13:20:44'
tags: [mysql, 死锁, 间隙锁, 加锁]
permalink: /articles/2021/06/08/1623116860957.html
---
![](https://b3logfile.com/bing/20201210.jpg?imageView2/1/w/960/h/540/interlace/1/q/100)

==============================================================================

按照非索引列更新

在可重复读的事务隔离级别下，在非索引列上进行更新和删除会对所有数据行进行加锁，阻止其他会话对边进行任何数据的增删改操作。

如果更新或删除条件为c3=4且c3列上没有索引则：

1. 不允许其他会话插入任意记录，因为所有记录的主键索引上存在X排他锁，无法申请插入意向X锁（lock_mode X insert intention waiting Record lock）
2. 不允许其他会话删除任意记录，因为所有记录的主键索引上存在X排他锁
3. 不允许其他会话更新任意记录。因为所有记录的主键索引上存在X排他锁

##=========================================##
测试数据：
CREATE TABLE `tb4001` (
`id` bigint(20) NOT NULL AUTO_INCREMENT,
`c1` int(11) DEFAULT NULL,
`c2` varchar(200) DEFAULT NULL,
`c3` int(11) DEFAULT NULL,
PRIMARY KEY (`id`),
KEY `idx_c1` (`c1`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

insert into tb4001(c1,c2,c3) values(2,2,2);
insert into tb4001(c1,c2,c3) values(4,4,4);
insert into tb4001(c1,c2,c3) values(7,7,7);
insert into tb4001(c1,c2,c3) values(8,8,8);

##=========================================##
##测试1：在没有索引的列上更新
##事务隔离级别：RR
会话1：
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
update tb4001 set c2=777 where c3=7;

##=========================================##
会话2:
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;

insert into tb4001(c1,c2,c3) values(9,9,9);

##执行结果：会话2被阻塞
使用SHOW ENGINE INNODB STATUS \G查看阻塞发生时的锁信息
------- TRX HAS BEEN WAITING 13 SEC FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 75 page no 3 n bits 80 index PRIMARY of table `test1`.`tb4001` trx id 10573 lock_mode X insert intention waiting Record lock, heap no 1 PHYSICAL RECORD: n_fields 1; compact format; info bits 0
0: len 8; hex 73757072656d756d; asc supremum;;

---

---TRANSACTION 10571, ACTIVE 404 sec
2 lock struct(s), heap size 1136, 5 row lock(s), undo log entries 1
MySQL thread id 52, OS thread handle 140674621650688, query id 1201 127.0.0.1 admin

##=========================================##
会话2:
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;

update tb4001 set c2=888 where c3=8;

##执行结果：会话2被阻塞
使用SHOW ENGINE INNODB STATUS \G查看阻塞发生时的锁信息
------- TRX HAS BEEN WAITING 5 SEC FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 75 page no 3 n bits 80 index PRIMARY of table `test1`.`tb4001` trx id 10573 lock_mode X waiting
Record lock, heap no 2 PHYSICAL RECORD: n_fields 6; compact format; info bits 0
0: len 8; hex 8000000000000001; asc         ;;
1: len 6; hex 00000000293c; asc     )<;;
2: len 7; hex b90000001c0110; asc        ;;
3: len 4; hex 80000002; asc     ;;
4: len 1; hex 32; asc 2;;
5: len 4; hex 80000002; asc     ;;

---

---TRANSACTION 10571, ACTIVE 681 sec
2 lock struct(s), heap size 1136, 5 row lock(s), undo log entries 1
MySQL thread id 52, OS thread handle 140674621650688, query id 1201 127.0.0.1 admin

##=========================================##
会话2:
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;

delete from  tb4001 where c3=8;
##执行结果：会话2被阻塞
使用SHOW ENGINE INNODB STATUS \G查看阻塞发生时的锁信息
------- TRX HAS BEEN WAITING 4 SEC FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 75 page no 3 n bits 80 index PRIMARY of table `test1`.`tb4001` trx id 10573 lock_mode X waiting
Record lock, heap no 2 PHYSICAL RECORD: n_fields 6; compact format; info bits 0
0: len 8; hex 8000000000000001; asc         ;;
1: len 6; hex 00000000293c; asc     )<;;
2: len 7; hex b90000001c0110; asc        ;;
3: len 4; hex 80000002; asc     ;;
4: len 1; hex 32; asc 2;;
5: len 4; hex 80000002; asc     ;;

---

---TRANSACTION 10571, ACTIVE 790 sec
2 lock struct(s), heap size 1136, 5 row lock(s), undo log entries 1
MySQL thread id 52, OS thread handle 140674621650688, query id 1201 127.0.0.1 admin
View Code

==============================================================================

按照非唯一索引更新

在可重复读的事务隔离级别下，按照非主键非唯一索引进行更新和删除，会对满足条件的行加行锁+满足条件的区域加gap锁
如果更新或删除条件为c1=4且c1列上有非唯一索引则：

1. 允许其他会话插入c1<>4的记录，但不允许插入c1=4的记录
2. 允许其他会话更新c1<>4的记录，但不允许将记录更新为c1=4的记录
3. 允许其他会话删除c1<>4的记录。
4. 允许插入\删除\修改在c1列索引上与c1=4相邻的记录，虽然操作会影响gap锁的边界值。

##=========================================##
测试数据：
CREATE TABLE `tb4001` (
`id` bigint(20) NOT NULL AUTO_INCREMENT,
`c1` int(11) DEFAULT NULL,
`c2` varchar(200) DEFAULT NULL,
`c3` int(11) DEFAULT NULL,
PRIMARY KEY (`id`),
KEY `idx_c1` (`c1`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

insert into tb4001(c1,c2,c3) values(2,2,2);
insert into tb4001(c1,c2,c3) values(4,4,4);
insert into tb4001(c1,c2,c3) values(7,7,7);
insert into tb4001(c1,c2,c3) values(8,8,8);

##=========================================##
##测试1：在没有索引的列上更新
##事务隔离级别：RR
会话1：
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
update tb4001 set c2=777 where c1=7;

##=========================================##
会话2:
begin;
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
insert into tb4001(c1,c2,c3) values(9,9,9);

会话2未被阻塞成功执行

##=========================================##
会话2:
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
insert into tb4001(c1,c2,c3) values(7,7,7);

##执行结果：会话2被阻塞
使用SHOW ENGINE INNODB STATUS \G查看阻塞发生时的锁信息
---TRANSACTION 10600, ACTIVE 7 sec inserting
mysql tables in use 1, locked 1
LOCK WAIT 2 lock struct(s), heap size 1136, 1 row lock(s), undo log entries 1
MySQL thread id 53, OS thread handle 140674620851968, query id 1317 127.0.0.1 admin update
insert into tb4001(c1,c2,c3) values(7,7,7)
------- TRX HAS BEEN WAITING 7 SEC FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 75 page no 4 n bits 72 index idx_c1 of table `test1`.`tb4001` trx id 10600 lock_mode X locks gap before rec insert intention waiting
Record lock, heap no 5 PHYSICAL RECORD: n_fields 2; compact format; info bits 0
0: len 4; hex 80000008; asc     ;;
1: len 8; hex 8000000000000004; asc         ;;

---

---TRANSACTION 10598, ACTIVE 270 sec
4 lock struct(s), heap size 1136, 3 row lock(s), undo log entries 1
MySQL thread id 52, OS thread handle 140674621650688, query id 1306 127.0.0.1 admin

##=========================================##
会话2:
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
delete from  tb4001 where c1=8;
会话2未被阻塞成功执行

##=========================================##
会话2:
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
update tb4001 set c2=888 where c1=8;
会话2未被阻塞成功执行

##=========================================##
会话2:
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
delete from  tb4001 where c1=4;
会话2未被阻塞成功执行

##=========================================##
View Code

==============================================================================

按照非唯一索引+条件更新

在可重复读事务隔离级别下，按照对非唯一索引列进行更新，会对扫描到的所有索引记录进行更新，无论该记录是否满足WHERE中的其他条件。

##=========================================##
测试数据：
CREATE TABLE `tb4001` (
`id` bigint(20) NOT NULL AUTO_INCREMENT,
`c1` int(11) DEFAULT NULL,
`c2` varchar(200) DEFAULT NULL,
`c3` int(11) DEFAULT NULL,
PRIMARY KEY (`id`),
KEY `idx_c1` (`c1`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

insert into tb4001(c1,c2,c3) values(2,2,2);
insert into tb4001(c1,c2,c3) values(4,4,4);
insert into tb4001(c1,c2,c3) values(4,4,44);
insert into tb4001(c1,c2,c3) values(7,7,7);
insert into tb4001(c1,c2,c3) values(8,8,8);

##=========================================##
##会话1：
##事务隔离级别：RR
会话1：
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
update tb4001 set c2=444 where c1=4 and c3=4;

##=========================================##
##会话2：
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
update tb4001 set c2=444 where c1=4 and c3=44;

会话2未被阻塞成功执行
##执行结果：会话2被阻塞
mysql tables in use 1, locked 1
LOCK WAIT 2 lock struct(s), heap size 1136, 1 row lock(s)
MySQL thread id 76, OS thread handle 140674621384448, query id 1636 127.0.0.1 admin updating
update tb4001 set c2=444 where c1=4 and c3=44
------- TRX HAS BEEN WAITING 13 SEC FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 79 page no 4 n bits 72 index idx_c1 of table `test1`.`tb4001` trx id 10781 lock_mode X waiting
Record lock, heap no 3 PHYSICAL RECORD: n_fields 2; compact format; info bits 0
0: len 4; hex 80000004; asc     ;;
1: len 8; hex 8000000000000002; asc         ;;

---

---TRANSACTION 10780, ACTIVE 52 sec
4 lock struct(s), heap size 1136, 5 row lock(s), undo log entries 1
MySQL thread id 75, OS thread handle 140674621916928, query id 1618 127.0.0.1 admin

##=========================================##
View Code

==============================================================================

按照非唯一组合索引更新

假设表TB1上有列C1和C2，有索引IDC_C1_C2(C1,C2)
在可重复提交事务隔离级别下,会话1按照C1=3 AND C2=4进行更新，则：

1. 会话2按照C1=3 AND C2=4进行更新,更新操作被阻塞
2. 会话2按照C1=3 AND C2=M(M<>4)进行更新,更新操作不会被阻塞
3. 会话2可以在C1=3 AND C2=4之后间隙插入记录，但不能在C1=3 AND C2=4之前的间隙插入记录

##=========================================##
##测试数据
CREATE TABLE `tb4001` (
`id` bigint(20) NOT NULL AUTO_INCREMENT,
`c1` int(11) DEFAULT NULL,
`c2` varchar(200) DEFAULT NULL,
`c3` int(11) DEFAULT NULL,
PRIMARY KEY (`id`),
KEY `idx_c1_c3` (`c1`,`c3`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

insert into tb4001(c1,c2,c3) values(2,2,2);
insert into tb4001(c1,c2,c3) values(4,4,4);
insert into tb4001(c1,c2,c3) values(4,4,44);
insert into tb4001(c1,c2,c3) values(7,7,7);
insert into tb4001(c1,c2,c3) values(8,8,8);

##=========================================##
##会话1：
##事务隔离级别：RR
会话1：
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
update tb4001 set c2=444 where c1=4 and c3=4;

##=========================================##
##会话2：
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
update tb4001 set c2=444 where c1=4 and c3=44;

会话2未被阻塞成功执行

##=========================================##
##会话2：
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
update tb4001 set c2=444 where c1=2 and c3=2;

会话2未被阻塞成功执行

##=========================================##
##会话2：
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
insert into tb4001(c1,c2,c3) values(4,4,3);

会话2被阻塞
##=========================================##
View Code

==============================================================================

按照唯一索引进行更新

在可重复读的事务隔离级别下，在唯一索引列上进行更新和删除在唯一索引的索引行上加排他锁。
如果更新或删除条件为c1=7且c1列上存在唯一索引则：

1. 阻止其他会话删除和修改c1=7的记录
2. 阻止其他会话插入c1=7的记录
3. 允许其他会话插入\删除\修改c1<>7的记录，但不允许将记录修改为c1=7的记录
   以上限制通过在唯一索引的索引记录上加排他锁X来实现，不会生产GAP锁

在根据唯一索引进行更新时，读提交事务隔离级别(RC)和可重复读事务隔离级别(RR)都只需要依赖唯一索引便可以保证事务ACID特性，无须使用GAP锁。

##=========================================##
测试数据：
CREATE TABLE `tb4001` (
`id` bigint(20) NOT NULL AUTO_INCREMENT,
`c1` int(11) DEFAULT NULL,
`c2` varchar(200) DEFAULT NULL,
`c3` int(11) DEFAULT NULL,
PRIMARY KEY (`id`),
UNIQUE KEY `idx_c1` (`c1`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

insert into tb4001(c1,c2,c3) values(2,2,2);
insert into tb4001(c1,c2,c3) values(4,4,4);
insert into tb4001(c1,c2,c3) values(7,7,7);
insert into tb4001(c1,c2,c3) values(8,8,8);

##=========================================##
##测试1：在没有索引的列上更新
##事务隔离级别：RR
会话1：
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
update tb4001 set c2=777 where c1=7;

##=========================================##
会话2：
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
insert into tb4001(c1,c2,c3) values(6,6,6);

会话2未被阻塞成功执行

##=========================================##
会话2：
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
insert into tb4001(c1,c2,c3) values(7,7,7);

##执行结果：会话2被阻塞
使用SHOW ENGINE INNODB STATUS \G查看阻塞发生时的锁信息

---TRANSACTION 10727, ACTIVE 9 sec inserting
mysql tables in use 1, locked 1
LOCK WAIT 2 lock struct(s), heap size 1136, 1 row lock(s), undo log entries 1
MySQL thread id 53, OS thread handle 140674620851968, query id 1553 127.0.0.1 admin update
insert into tb4001(c1,c2,c3) values(7,7,7)
------- TRX HAS BEEN WAITING 9 SEC FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 77 page no 4 n bits 72 index idx_c1 of table `test1`.`tb4001` trx id 10727 lock mode S waiting
Record lock, heap no 4 PHYSICAL RECORD: n_fields 2; compact format; info bits 0
0: len 4; hex 80000007; asc     ;;
1: len 8; hex 8000000000000003; asc         ;;

---

---TRANSACTION 10721, ACTIVE 32 sec
3 lock struct(s), heap size 1136, 2 row lock(s), undo log entries 1
MySQL thread id 52, OS thread handle 140674621650688, query id 1544 127.0.0.1 admin

##=========================================##
会话2：
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
update tb4001 set c2=888 where c1=8;

会话2未被阻塞成功执行

##=========================================##
会话2：
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
update tb4001 set c1=7 where c1=8;

会话2未被阻塞成功执行
##执行结果：会话2被阻塞
使用SHOW ENGINE INNODB STATUS \G查看阻塞发生时的锁信息
---TRANSACTION 10730, ACTIVE 4 sec updating or deleting
mysql tables in use 1, locked 1
LOCK WAIT 4 lock struct(s), heap size 1136, 3 row lock(s), undo log entries 1
MySQL thread id 53, OS thread handle 140674620851968, query id 1567 127.0.0.1 admin updating
update tb4001 set c1=7 where c1=8
------- TRX HAS BEEN WAITING 4 SEC FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 77 page no 4 n bits 72 index idx_c1 of table `test1`.`tb4001` trx id 10730 lock mode S waiting
Record lock, heap no 4 PHYSICAL RECORD: n_fields 2; compact format; info bits 0
0: len 4; hex 80000007; asc     ;;
1: len 8; hex 8000000000000003; asc         ;;

---

---TRANSACTION 10721, ACTIVE 100 sec
3 lock struct(s), heap size 1136, 2 row lock(s), undo log entries 1
MySQL thread id 52, OS thread handle 140674621650688, query id 1544 127.0.0.1 admin

##=========================================##
会话2：
SET SESSION tx_isolation='REPEATABLE-READ';
START TRANSACTION;
SELECT @@GLOBAL.tx_isolation, @@SESSION.tx_isolation;
delete from tb4001 where c1=8;

会话2未被阻塞成功执行

