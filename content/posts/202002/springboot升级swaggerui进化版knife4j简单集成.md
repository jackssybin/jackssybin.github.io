title: springboot升级swagger-ui进化版knife4j简单集成
date: '2020-02-27 09:53:09'
updated: '2020-02-27 09:53:09'
tags: [swagger, knife4j, java, springboot]
permalink: /articles/2020/02/27/1582768389143.html
---
### 1.官方文档
[knife4j接入文档](https://doc.xiaominfo.com/guide/useful.html#java%E5%BC%80%E5%8F%91)

### 2.概述
引入基础包，如果老项目以前有swagger做doc文档。那就省事了。可以直接引入新ui包
```

<dependency>
 <groupId>io.springfox</groupId>
 <artifactId>springfox-swagger2</artifactId>
 <version>2.9.2</version>
</dependency>
``````
新ui包 ，我用的 lastVersion =1.9.6
```
<dependency>
  <groupId>com.github.xiaoymin</groupId>
  <artifactId>swagger-bootstrap-ui</artifactId>
  <version>${lastVersion}</version>
</dependency>
``````

### 3.配置相关
其实就是swagger的配置哈
```

@Configuration
@EnableSwagger2
public class SwaggerConfiguration {

 @Bean
 public Docket createRestApi() {
     return new Docket(DocumentationType.SWAGGER_2)
     .apiInfo(apiInfo())
     .select()
     .apis(RequestHandlerSelectors.basePackage("com.bycdao.cloud"))
     .paths(PathSelectors.any())
     .build();
 }

 private ApiInfo apiInfo() {
     return new ApiInfoBuilder()
     .title("swagger-bootstrap-ui RESTful APIs")
     .description("swagger-bootstrap-ui")
     .termsOfServiceUrl("http://localhost:8999/")
     .contact("developer@mail.com")
     .version("1.0")
     .build();
 }
}

```
### 4.添加访问路径 doc.html 和swagger-ui.html 同理
SpringBoot中访问`doc.html`

实现SpringBoot的`WebMvcConfigurer`接口，添加相关的`ResourceHandler`,代码如下：

```

@SpringBootApplication

@ConditionalOnClass(SpringfoxWebMvcConfiguration.class)
public class SwaggerBootstrapUiDemoApplication  implements WebMvcConfigurer{

	@Override
	public void addResourceHandlers(ResourceHandlerRegistry registry) {
		registry.addResourceHandler("doc.html").addResourceLocations("classpath:/META-INF/resources/");
		registry.addResourceHandler("/webjars/**").addResourceLocations("classpath:/META-INF/resources/webjars/");
	}
}
``````

### 5.成果展示
![null](https://doc.xiaominfo.com/images/s1.png)



