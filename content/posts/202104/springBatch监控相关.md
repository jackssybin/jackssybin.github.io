title: springBatch监控相关
date: '2021-04-21 09:18:35'
updated: '2021-04-21 09:18:35'
tags: [springBatch, prometheus, 自定义监控]
permalink: /articles/2021/04/21/1618967915021.html
---
![](https://b3logfile.com/bing/20200815.jpg?imageView2/1/w/960/h/540/interlace/1/q/100)

Spring Boot Actuator可以帮助你监控和管理Spring Boot应用，比如健康检查、审计、统计和HTTP追踪等。所有的这些特性可以通过JMX或者HTTP endpoints来获得。

Actuator同时还可以与外部应用监控系统整合，比如 [Prometheus](https://prometheus.io/), [Graphite](https://graphiteapp.org/), [DataDog](https://www.datadoghq.com/), [Influx](https://www.influxdata.com/), [Wavefront](https://www.wavefront.com/), [New Relic](https://newrelic.com/)等。这些系统提供了非常好的仪表盘、图标、分析和告警等功能，使得你可以通过统一的接口轻松的监控和管理你的应用。

Actuator使用[Micrometer](http://micrometer.io/)来整合上面提到的外部应用监控系统。这使得只要通过非常小的配置就可以集成任何应用监控系统。

# 预备知识:

| 监控 | micrometer | actuator | promethes |
| - | - | - | - |
| 概念 | 类似slf4j门面模式。提供接口和方法 | 调用micrometer对springboot体系提供了健康检查，对spring体系的扩展。也可以自定义监控。 | 监控的一类客户端。获取的数据格式需要定制化。micrometer有单独的门面扩展包 |

# 1.配置pom

```
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
​
<!-- Micrometer Prometheus registry  -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

# 2. 配置文件

```
#支持所有监控  最少需要打开info,metrics,promethes这三个
management.endpoints.web.exposure.include=*
management.endpoints.web.exposure.exclude=env,beans
​
# 单独打开 默认都是关闭
management.endpoints.enabled-by-default=false
management.endpoint.info.enabled=true
​
# 跨域解决
management.endpoints.web.cors.allowed-origins=https://example.com
management.endpoints.web.cors.allowed-methods=GET,POST
​
# 管理端口可调节，也可以直接以 tomcat的端口为准
management.server.port=8089
​
```

# 3.支持的接口

```
{
    "_links": {
        "self": {
            "href": "http://localhost:8089/metrics",
            "templated": false,
            "desc":"应用支持的所有监控接口"
        },
        "beans": {
            "href": "http://localhost:8089/metrics/beans",
            "templated": false,
            "desc":"应用内所有的Bean 信息"
        },
        "caches-cache": {
            "href": "http://localhost:8089/metrics/caches/{cache}",
            "templated": true,
            "desc":"应用的指定缓存信息"
        },
        "caches": {
            "href": "http://localhost:8089/metrics/caches",
            "templated": false,
            "desc":"应用的所以缓存信息"
        },
        "health": {
            "href": "http://localhost:8089/metrics/health",
            "templated": false,
            "desc":"应用健康的基础信息,应用是否存活"
        },
        "health-path": {
            "href": "http://localhost:8089/metrics/health/{*path}",
            "templated": true,
            "desc":"应用"
        },
        "info": {
            "href": "http://localhost:8089/metrics/info",
            "templated": false,
            "desc":""
        },
        "conditions": {
            "href": "http://localhost:8089/metrics/conditions",
            "templated": false,
            "desc":"应用内所有bean中带条件的"
        },
        "configprops": {
            "href": "http://localhost:8089/metrics/configprops",
            "templated": false,
            "desc":"应用的所以配置相关"
        },
        "env": {
            "href": "http://localhost:8089/metrics/env",
            "templated": false,
            "desc":"应用的所以环境信息系统的环境信息，应用的环境信息"
        },
        "env-toMatch": {
            "href": "http://localhost:8089/metrics/env/{toMatch}",
            "templated": true,
            "desc":"显示调用env中生效的环境信息http://localhost:8089/metrics/env/local.server.port"
        },
        "loggers": {
            "href": "http://localhost:8089/metrics/loggers",
            "templated": false,
            "desc":"应用所有日志相关,日志级别"
        },
        "loggers-name": {
            "href": "http://localhost:8089/metrics/loggers/{name}",
            "templated": true,
            "desc":"显示调用日志中生效的日志级别http://localhost:8089/metrics/loggers/com.citicbank.r2dbc"
        },
        "heapdump": {
            "href": "http://localhost:8089/metrics/heapdump",
            "templated": false,
            "desc":"提供实时的dump信息"
        },
        "threaddump": {
            "href": "http://localhost:8089/metrics/threaddump",
            "templated": false,
            "desc":"提供实时的threaddump信息"
        },
        "metrics-requiredMetricName": {
            "href": "http://localhost:8089/metrics/metrics/{requiredMetricName}",
            "templated": true,
            "desc":"指定某一个metrics查看具体的信息"
        },
        "metrics": {
            "href": "http://localhost:8089/metrics/metrics",
            "templated": false,
            "desc":"应用内提供的jvm，线程,数据库相关"
        },
        "scheduledtasks": {
            "href": "http://localhost:8089/metrics/scheduledtasks",
            "templated": false,
            "desc":"应用指定http://localhost:8089/metrics/metrics/http.server.requests "
        },
        "mappings": {
            "href": "http://localhost:8089/metrics/mappings",
            "templated": false,
            "desc":"应用所有对外暴露的接口信息"
        },
        "mappings": {
            "href": "http://localhost:8089/metrics/prometheus",
            "templated": false,
            "desc":"应用支持的promethes监控端点,将所有监控metrics数据以promethes需要的格式展示，promethes定时调用此接口实现数据的采集"
        }
    }
}
```

### 4.具体接口

请求: [http://localhost:8089/metrics/metrics/http.server.requests](http://localhost:8089/metrics/metrics/http.server.requests)

```
{
    "name": "http.server.requests",
    "description": null,
    "baseUnit": "seconds",
    "measurements": [{
        "statistic": "COUNT",
        "value": 21.0
    }, {
        "statistic": "TOTAL_TIME",
        "value": 1.1525394000000002
    }, {
        "statistic": "MAX",
        "value": 0.0
    }],
    "availableTags": [{
        "tag": "exception",
        "values": ["None", "ResponseStatusException"]
    }, {
        "tag": "method",
        "values": ["GET"]
    }, {
        "tag": "uri",
        "values": ["/metrics/loggers/{name}", "/metrics/threaddump", "/metrics/heapdump", "/metrics/configprops", "/metrics/mappings", "/metrics/loggers", "/metrics/metrics", "/metrics/env", "/metrics/env/{toMatch}", "/metrics/metrics/{requiredMetricName}", "/metrics/info", "/**"]
    }, {
        "tag": "outcome",
        "values": ["CLIENT_ERROR", "SUCCESS"]
    }, {
        "tag": "status",
        "values": ["404", "200"]
    }]
}
```

#### 4. springBatch 接口

需要项目运行过job任务。

在源码层次手动注入过，AbstractJob,AbstractStep#excute抽象方法 添加了micrometer 记录方法。
![image20210420184351593.png](https://b3logfile.com/file/2021/04/image-20210420184351593-1c113c8d.png)
![image20210420184243854.png](https://b3logfile.com/file/2021/04/image-20210420184243854-88b95ff5.png)
![image20210420201533923.png](https://b3logfile.com/file/2021/04/image-20210420201533923-f869305e.png)




默认支持

| metrics name | type | *Description* | *Tags* |
| - | - | - | - |
| spring.batch.job | TIMER | 作业job执行期间 | name, status |
| spring.batch.job.active | LONG_TASK_TIMER | 正在运行的job | name |
| spring.batch.step | TIMER | 作业step执行情况 | name, job.name, status |
| spring.batch.item.read | TIMER | 作业read情况 | job.name, step.name,status |
| spring.batch.item.process | TIMER | 作业process情况 | job.name, step.name,status |
| spring.batch.chunk.write | TIMER | 作业write情况 | job.name, step.name,status |

1. [http://localhost:8099/actuator/metrics/spring.batch.step](http://localhost:8099/actuator/metrics/spring.batch.step)
   查看系统中Step的运行情况

```
{
    "name": "spring.batch.step",
    "description": "Step duration",
    "baseUnit": "seconds",
    "measurements": [{
        "statistic": "COUNT",
        "value": 1.0
    }, {
        "statistic": "TOTAL_TIME",
        "value": 628.3536165
    }, {
        "statistic": "MAX",
        "value": 628.3536165
    }],
    "availableTags": [{
        "tag": "application",
        "values": ["testjackssyappname"]
    }, {
        "tag": "name",
        "values": ["testBatchTranscationStep"]
    }, {
        "tag": "job.name",
        "values": ["testBatchTranscation123458888"]
    }, {
        "tag": "status",
        "values": ["COMPLETED"]
    }]
}
```

2. [http://localhost:8097/actuator/metrics/spring.batch.job.active](http://localhost:8097/actuator/metrics/spring.batch.job.active)
    查看系统中的job运行状态

```
{
    "name": "spring.batch.job.active",
    "description": "Active jobs",
    "baseUnit": "seconds",
    "measurements": [{
        "statistic": "ACTIVE_TASKS",
        "value": 1.0
    }, {
        "statistic": "DURATION",
        "value": 8.35068088E10
    }],
    "availableTags": [{
        "tag": "application",
        "values": ["testjackssyappname"]
    }]
}
```

3. [http://localhost:8099/actuator/metrics/spring.batch.job](http://localhost:8099/actuator/metrics/spring.batch.job)
    查看系统运行中job的状况

```
{
    "name": "spring.batch.job",
    "description": "Job duration",
    "baseUnit": "seconds",
    "measurements": [{
        "statistic": "COUNT",
        "value": 1.0
    }, {
        "statistic": "TOTAL_TIME",
        "value": 636.9190648
    }, {
        "statistic": "MAX",
        "value": 0.0
    }],
    "availableTags": [{
        "tag": "application",
        "values": ["testjackssyappname"]
    }, {
        "tag": "name",
        "values": ["testBatchTranscation123458888"]
    }, {
        "tag": "status",
        "values": ["COMPLETED"]
    }]
}
```

4. [http://localhost:8099/actuator/prometheus](http://localhost:8099/actuator/prometheus)
    支持的promethes 接口数据

```
# HELP jvm_memory_committed_bytes The amount of memory in bytes that is committed for  the Java virtual machine to use
# TYPE jvm_memory_committed_bytes gauge
jvm_memory_committed_bytes{area="nonheap",id="Code Cache",} 9830400.0
jvm_memory_committed_bytes{area="nonheap",id="Metaspace",} 4.3032576E7
jvm_memory_committed_bytes{area="nonheap",id="Compressed Class Space",} 6070272.0
jvm_memory_committed_bytes{area="heap",id="PS Eden Space",} 2.63192576E8
jvm_memory_committed_bytes{area="heap",id="PS Survivor Space",} 1.2058624E7
jvm_memory_committed_bytes{area="heap",id="PS Old Gen",} 1.96608E8
# HELP logback_events_total Number of error level events that made it to the logs
# TYPE logback_events_total counter
logback_events_total{level="error",} 0.0
logback_events_total{level="warn",} 0.0
logback_events_total{level="info",} 42.0
logback_events_total{level="debug",} 0.0
logback_events_total{level="trace",} 0.0
.....
```

4. 增加自定义属性

```
//   spring.application.name ="testjackssyappname"
   @Bean
    MeterRegistryCustomizer<MeterRegistry> configurer(@Value("${spring.application.name}") String applicationName){
        return registry -> registry.config().commonTags("application", applicationName);
    }
```

6. 自定义监控

```
​
@Component
public class DemoMetrics implements MeterBinder {
    private AtomicLong systemMemoryUsed = new AtomicLong(999);
​
​
    //这里实现了MeterBinder接口的bindTo方法，将要采集的指标注册到MeterRegistry
    // 将此"system.memory.used" 注册到metrics中。通过metrics/system.memory.used 就能   
    @Override
    public void bindTo(MeterRegistry meterRegistry) {
        //这里的MeterRegistry 是全局的
        Gauge.builder("system.memory.used", systemMemoryUsed, AtomicLong::get)
//              .tag("groupName", this.groupName)
                .description("系统已用内存（byte）")
                .register(meterRegistry);
    }
​
    //定时器，定时改变内存数值
    @Scheduled(fixedRate = 1000)
    public void recordMemory() {
        //获取内存信息，省略
        //更改内存
//      systemMemoryUsed.set(physicalUse);
    }
}
```

