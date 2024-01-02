title: Rust学习之二猜字谜
date: '2019-09-24 16:07:42'
updated: '2019-09-24 16:07:42'
tags: [Rust学习]
permalink: /articles/2019/09/24/1569312462439.html
---
1.首先cargo一个项目
```
 cargo new guessing_game
```
2.修改toxml
添加依赖
```
[dependencies]
rand = "0.3.14"
```
3.切换数据源,一来源
对于在国内的人来说，Rust开发时有时使用官方的源太慢，可以考虑更换使用国内中科大的源。更换方法如下： 在 *$HOME/.cargo/config* 中添加如下内容（如果文件不存在请直接新建该文件）：
```
[source.crates-io]
registry = "https://mirrors.ustc.edu.cn/crates.io-index"
replace-with = 'ustc'

[source.ustc]
registry = "https://mirrors.ustc.edu.cn/crates.io-index"
```
4.引入依赖的api文档
```
cargo doc --open
```
5.最终代码
```
use std::io;
use std::cmp::Ordering;
use rand::Rng;

fn main() {
    println!("Guess the number!");

    let secret_number = rand::thread_rng().gen_range(1, 101);

    loop {
        println!("Please input your guess.");

        let mut guess = String::new();

        io::stdin().read_line(&mut guess)
            .expect("Failed to read line");

        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        println!("You guessed: {}", guess);

        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    }
}
```

效果图
![image.png](https://img.hacpai.com/file/2019/09/image-752bf172.png)
代码已上传
