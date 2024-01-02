title: Springboot2+mybatisplus3.0输出sql日志的两种方式
date: '2019-12-04 16:59:44'
updated: '2019-12-04 16:59:44'
tags: [springboot, mybatis-plus, sql日志]
permalink: /articles/2019/12/04/1575449984572.html
---
#### 1.springboot版本：
```
 <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.0.3.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
```
#### 2.mybatis-plus版本：
```
 <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-boot-starter</artifactId>
            <version>3.0-RC1</version>
</dependency>
```
#### 3.通过配置文件形式的
```
#mybatisPlu
mybatis-plus:
  mapper-locations: classpath:/mapper/**/*Mapper.xml
  typeAliasesPackage: com.**.entity
  global-config:
    db-config:
      #主键类型  AUTO:"数据库ID自增", INPUT:"用户输入ID",ID_WORKER:"全局唯一ID (数字类型唯一ID)", UUID:"全局唯一ID UUID";
      id-type: UUID
       #字段策略 IGNORED:"忽略判断",NOT_NULL:"非 NULL 判断"),NOT_EMPTY:"非空判断"
      field-strategy: not_empty
      #驼峰下划线转换
      column-underline: true
      db-type: mysql
    #刷新mapper
    refresh-mapper: true
  #原生配置
  configuration:
    #开启驼峰功能
    map-underscore-to-camel-case: true
    cache-enabled: false
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl  #关键部分。用来显示sql
```
效果如下


```
Creating a new SqlSession
SqlSession [org.apache.ibatis.session.defaults.DefaultSqlSession@fd01818] was not registered for synchronization because synchronization is not active
JDBC Connection [HikariProxyConnection@1262384429 wrapping com.mysql.jdbc.JDBC4Connection@ef6980] will not be managed by Spring
 JsqlParserCountOptimize sql=SELECT  id AS id,account_user AS accountUser  FROM bz_account  WHERE  1=1
==>  Preparing: SELECT COUNT(1) FROM bz_account WHERE 1 = 1 
==> Parameters: 
<==    Columns: COUNT(1)
<==        Row: 51
==>  Preparing: SELECT id AS id,account_user AS accountUser FROM bz_account WHERE 1=1 LIMIT 0,10 
==> Parameters: 
<==    Columns: id, accountUser, accountPwd, nickName, sex, regionId, regionName, remarks, status, useNumber, tagGroup, userSource, userAgent, createDate, updateDate, invalidDate
<==        Row: 1, 533527568s@afafdasdfas,
<==      Total: 10
```


#### 4. 通过配置bean形式的
```
  /***

     * plus 的性能优化，显示sql
     * @return
     */
    @Bean
    public PerformanceInterceptor performanceInterceptor() {
        PerformanceInterceptor performanceInterceptor = new PerformanceInterceptor();
        /*<!-- SQL 执行性能分析，开发环境使用，线上不推荐。 maxTime 指的是 sql 最大执行时长 -->*/
        performanceInterceptor.setMaxTime(10000);
        /*<!--SQL是否格式化 默认false-->*/
        performanceInterceptor.setFormat(true);
        return performanceInterceptor;
    }
```
效果如下
![image.png](https://img.hacpai.com/file/2019/12/image-adfd2b0a.png)


