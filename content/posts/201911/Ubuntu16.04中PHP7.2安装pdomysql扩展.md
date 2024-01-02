title: Ubuntu16.04中PHP7.2 安装pdo_mysql扩展
date: '2019-11-14 18:56:04'
updated: '2019-11-14 19:41:44'
tags: [php]
permalink: /articles/2019/11/14/1573728964758.html
---
##### 1.查看php版本
```
php -v
当前7.2版本
```
##### 2.查看是否安装mysql扩展
两种方式
```
php -m
php -r 'phpinfo();'
#查看加载顺序
grep -Hrv ";" /etc/php | grep -E "extension(\s+)?="
```
##### 3. 安装mysql扩展
```
sudo apt install php7.2-mysql
```

##### 4. 修改配置文件
```
 cd /etc/php/7.2/cli //进入配置文件目录
 sudo vim php.ini //vim打开配置文件
 //可能会输入root用户密码
 /pdo //查找，输入后按enter键即可
 //按i键进入vim编辑模式
 extension=php_pdo_mysql.dll //去掉extensions前面的;号
 //按shift + : 号，然后输入wq
```