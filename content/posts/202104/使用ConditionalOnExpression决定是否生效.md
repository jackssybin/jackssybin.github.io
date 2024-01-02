title: 使用@ConditionalOnExpression决定是否生效
date: '2021-04-21 10:45:05'
updated: '2021-04-21 10:45:05'
tags: [springbatch]
permalink: /articles/2021/04/21/1618973105136.html
---
![](https://b3logfile.com/bing/20201202.jpg?imageView2/1/w/960/h/540/interlace/1/q/100)

@ConditionalOnExpression 根据表达式选择性加载
@ConditionalOnProperty  根据配置选择性加载

```
#消费者总开关，0关1开
mq.cumsumer.enabled=1
#rocketmq消费者开关，true开启，false关闭
rocketmq.comsumer.enabled=false
#rabbitmq消费者开关，true开启，false关闭
rabbitmq.comsumer.enabled=true
#消费者选择
mq.comsumer=rabbitmq
```

//布尔值和数字
@Component
@RabbitListener(queues = "monitorDataQueue")
@ConditionalOnExpression("${mq.cumsumer.enabled:0}==1&&${rabbitmq.comsumer.enabled:false}")

//字符串
@Component
@RabbitListener(queues = "monitorDataQueue")
@ConditionalOnExpression("'${mq.comsumer}'.equals('rabbitmq')")

// 直接使用boolean 的校验
// spring.batch.job.enabled = true

@ConditionalOnProperty(prefix = "spring.batch.job", name = "enabled", havingValue = "true", matchIfMissing = true)

```


