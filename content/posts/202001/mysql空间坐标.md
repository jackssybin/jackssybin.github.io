title: mysql空间坐标
date: '2020-01-03 11:18:41'
updated: '2020-01-03 12:31:59'
tags: [mysql, 空间坐标, 范围查询, gis]
permalink: /articles/2020/01/03/1578021520851.html
---
![](https://img.hacpai.com/bing/20181109.jpg?imageView2/1/w/960/h/540/interlace/1/q/100)

# 1.常用使用场景  
矩形查询：  
适合智能手机、网页端高效展示屏幕范围内数据。通过API获取显示屏4角的坐标点，顺序连接生成矩形，空间数据库提供查询矩形范围内坐标功能。  
圆型查询：  
根据当前所在位置为中心点，根据给定的里程数为半径生成圆形，搜索圆形范围内的数据。

# 2.MySql支持的类型
点 POINT(15 20)
线 LINESTRING(0 0, 10 10, 20 25, 50 60)
面 POLYGON((0 0,10 0,10 10,0 10,0 0),(5 5,7 5,7 7,5 7, 5 5))
多个点 MULTIPOINT(0 0, 20 20, 60 60)
多个线 MULTILINESTRING((10 10, 20 20), (15 15, 30 15))
多个面 MULTIPOLYGON(((0 0,10 0,10 10,0 10,0 0)),((5 5,7 5,7 7,5 7, 5 5)))
集合 GEOMETRYCOLLECTION(POINT(10 10), POINT(30 30), LINESTRING(15 15, 20 20))，简称GEOMETRY，可以放入点、线、面。
# 3.测试
```
DROP TABLE IF EXISTS points;
CREATE TABLE `points` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL DEFAULT '',
  `location` point NOT NULL,
  PRIMARY KEY (`id`),
  SPATIAL KEY `sp_index` (`location`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# 天安门
INSERT INTO points VALUES (1,'aaaa',POINT(116.397389,39.908149));

# 颐和园
INSERT INTO points VALUES (2,'bbbb',POINT(116.273106,39.992634));

# 定义多边形
SET @rect = CONCAT('POLYGON((116.373871 39.915786,116.417645 39.916444,116.41816 39.900841,116.374214 39.900182,116.373871 39.915786))');
# 使用变量
select name,X(location),Y(location),Astext(location) from points where INTERSECTS( location, GEOMFROMTEXT(@rect) ) ;
```
# 4.sql 范围查询
sql是基于[半正矢公式](http://www.movable-type.co.uk/scripts/latlong.html) `a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)`的SQL查询语句。

* `6371`是地球的半径，单位：公里。如果想以英里搜索，将6371换成3959即可。
* `39.915599`是搜索点中心纬度（例如想搜索北京天安门附近的标记点，则这里就是北京天安门的纬度）
* `116.402687`是搜索点中心经度（例如想搜索北京天安门附近的标记点，则这里就是北京天安门的经度）
* `distance`字段是标记点与搜索点中心的距离，单位：公里（如果地球半径是英里，则这里也是英里）
* `25`是范围，表示搜索出搜索中心点25公里以内的标记点
```
#数据库表结构
CREATE TABLE `markers` (
  `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID' ,
  `name` VARCHAR( 60 ) NOT NULL COMMENT '标记名称' ,
  `address` VARCHAR( 80 ) NOT NULL COMMENT '标记地址' ,
  `lat` FLOAT( 10, 6 ) NOT NULL COMMENT '纬度' ,
  `lng` FLOAT( 10, 6 ) NOT NULL COMMENT '经度'
) ENGINE = InnoDB COMMENT = '标记表' ;
#数据库表数据
INSERT INTO `markers` (`name`, `address`, `lat`, `lng`) VALUES ('北京市天安门','北京市东城区东长安街','39.915599','116.402687');
INSERT INTO `markers` (`name`, `address`, `lat`, `lng`) VALUES ('广州华立科技职业学院','广东省广州市增城广州华立科技园华立路7号','23.248335','113.871302');
INSERT INTO `markers` (`name`, `address`, `lat`, `lng`) VALUES ('韶关市风采楼','广东省韶关市浈江区风采路34号','24.813028','113.606039');
#查询

SELECT `id` , `name`
    , 6371 * acos(cos(radians(39.915599)) * cos(radians(`lat`)) * cos(radians(`lng`) - radians(116.402687)) + sin(radians(39.915599)) * sin(radians(`lat`))) AS `distance`
FROM `markers`
HAVING `distance` < 25
ORDER BY `distance`
LIMIT 0, 20;
```
