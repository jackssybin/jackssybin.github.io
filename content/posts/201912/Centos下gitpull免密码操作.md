title: Centos下git pull免密码操作
date: '2019-12-20 01:23:16'
updated: '2019-12-20 01:23:16'
tags: [centos7, centos, git, 免密]
permalink: /articles/2019/12/20/1576776196766.html
---
**1.服务器使用的centos部署的Java项目，使用git pull拉下代码的class文件的时候，经常会提示需要输入帐号和密码。**

```
git config --global credential.helper store
```

**2. git pull 一次之后下次就不用密码了**