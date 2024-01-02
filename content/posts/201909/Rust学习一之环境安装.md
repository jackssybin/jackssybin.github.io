title: Rust 学习一之环境安装
date: '2019-09-21 00:28:19'
updated: '2019-09-21 16:12:05'
tags: [学习]
permalink: /articles/2019/09/21/1568996899251.html
---
![](https://img.hacpai.com/bing/20190719.jpg?imageView2/1/w/960/h/540/interlace/1/q/100) 

## 1.社区
[https://rustlang-cn.org/](https://rustlang-cn.org/)

## 2.环境安装
windows 下载地址
[https://www.rust-lang.org/install.html](https://www.rust-lang.org/install.html)
![1.png](https://img.hacpai.com/file/2019/09/1-fe9c0ecb.png)

下载完之后》rustup-init.exe
直接安装走默认的就可以了

安装完之后看看 版本，确定下是否安装成功了
```
rustc --version
```
我安装完，报错了
no default toolchain configured
执行命令


更行版本
```
rustup update
```
卸载rust
```
rustup self uninstall
```

### 3.hello word 走一波
新建文件main.rs编写程序
```
fn main() {
    println!("Hello, world!");
}

```
然后编译一下 rustc main.rs
生成编译文件 和可执行文件如图
![image.png](https://img.hacpai.com/file/2019/09/image-dcafecf4.png)

看生成了 main.exe 文件
windows用.\main.exe 执行一下这个可执行文件。看看效果哈。
![image.png](https://img.hacpai.com/file/2019/09/image-13b8cd12.png)
熟悉的世界你好。跃然屏幕上。心情很好。没遇到啥问题很好哈

学习了hello word 然后再看看rust的依赖包管理工具cargo

### 4.hello cargo 接着干
Cargo 是 Rust 的构建系统和包管理器，它可以处理很多任务，比如构建代码、下载依赖库并编译这些库。

官方默认是安装了的  --version查看一下
```
cargo --version
```
### 5.使用 Cargo 创建项目
```
cargo new hello_cargo
```
运行完这个命令会自动给你生成一个helloword文件的哈。切换到跟目录build一下
```
cargo build
```
效果图如下
![image.png](https://img.hacpai.com/file/2019/09/image-6e46b52e.png)
cargo.lock文件系统用的，不用管他，也不要修改他
生成的文件在target\debug下面
```
.\target\debug\hello_cargo.exe
如果只有一个运行文件的话
cargo run 也能达到相同目的
cargo check 是在运行之前做一下检查。校验。
```
熟悉的helloword 又出现了。

接着说下发布。
```
cargo build  #这个是开发时用的，编译快
cargo build --release #这个时发布时用的，编译可能会慢，但是cargo里内部做优化了
```

## 总结一下啊
1. rust安装
1. rust运行命令 rustc main.rs
1. cargo命令：cargo --version, cargo new hello_cargo,cargo build,cargo check,cargo run,cargo build --release

git已上传：[https://github.com/jackssybin/rust_items.git](https://github.com/jackssybin/rust_items.git)
友链：[https://blog.csdn.net/jackssybin/article/details/101109616](https://blog.csdn.net/jackssybin/article/details/101109616)








