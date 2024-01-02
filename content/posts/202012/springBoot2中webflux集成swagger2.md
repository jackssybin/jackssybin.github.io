title: springBoot2中webflux集成swagger2
date: '2020-12-25 10:01:38'
updated: '2020-12-25 10:01:38'
tags: [springboot2, swagger2]
permalink: /articles/2020/12/25/1608861698265.html
---
1.pom文件中引用如下

```xml
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-boot-starter</artifactId>
    <version>3.0.0</version>
</dependency>
```

2.添加swagger2配置文件

```
@Configuration
@EnableSwagger2
public class SwaggerConfiguration {

    @Bean
    public Docket createRestApi() {
        return new Docket(DocumentationType.SWAGGER_2)
                .apiInfo(apiInfo())
                .select()
                .apis(RequestHandlerSelectors.basePackage("com.*.controller"))
                .paths(PathSelectors.any())
                .build();
    }

    private ApiInfo apiInfo() {
        return new ApiInfoBuilder()
                .title("swagger-bootstrap-ui RESTful APIs")
                .description("swagger-bootstrap-ui")
                .termsOfServiceUrl("http://localhost:8080/")
                .version("1.0")
                .build();
    }
}
```

3.启动服务访问
原版页面地址：http://127.0.0.1:8080/swagger-ui/index.html

