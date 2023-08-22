# PicoCTF 2023

##  前言

题目地址：[picoCTF - picoGym Challenges](https://play.picoctf.org/practice?category=1&originalEvent=72&page=1)

官方discord：[Discord](https://discord.com/channels/575006934089072650/960896102427656263)

## WEB

### findme

抓包，前半部分Cookie在响应头处，后半部分登录看网页源码。

### MatchTheRegex

注意到网页源码中的 ^p…F，提示我们以p开头，以F结尾。这不就是picoCTF吗？尝试一下果然得到了flag。

### SOAP

经典的[XML外部实体注入](https://xz.aliyun.com/t/3357)，读取/etc/passwd文件即可。注意元素的名字要和题目的一样，分别是data和ID。

### More SQLi

题目提示是SQLiLite，网上搜索几篇[文章](https://blog.csdn.net/HBohan/article/details/120672745)学习一下SQLiLite注入。

本题并不复杂，似乎构造一个联合注入payload就会自动弹出flag了。

```
username=123&password=123' union select 1;
```

### Java Code Analysis!?!

#### 题目描述

BookShelf Pico, my premium online book-reading service.I believe that my website is super secure. I challenge you to prove me wrong by reading the 'Flag' book!Here are the credentials to get you started:

- Username: "user"
- Password: "user"

Source code can be downloaded [here](https://artifacts.picoctf.net/c/481/bookshelf-pico.zip).Website can be accessed [here!](http://saturn.picoctf.net:64868/).

#### 题目分析

> 看不懂代码就交给gpt帮忙分析。

描述让大家读取“Flag”这本书，但是普通用户没有权限。

![image-20230807111456682](images/image-20230807111456682.png)

源码已经给了，找一找读取FLAG的路由代码。抓包看一下发现是`GET /base/books/cover/5`。

点击vscode左侧的放大镜进行工作区内全局搜索，最终确定应该是如下的路由：

![image-20230807112057833](images/image-20230807112057833.png)

![image-20230807112251495](images/image-20230807112251495.png)

我的问题是这个路由处理函数似乎并不含有身份验证功能？所以代码是在什么地方进行了身份验证的呢？问了下gpt发现应该是利用Spring Security来进行身份验证，通常该功能的代码含有`EnableWebSecurity`等字样。不过一开始搜索/books的时候就已经弹出了SecurityConfig了。

![image-20230807114006396](images/image-20230807114006396.png)

上面代码意思是除了列出的那三个路由，其他的路由都要身份验证。具体的身份验证方法应该是`reauthenticationFilter`。

跟进去就可以看到jwt解码的函数了，再跟进去就可以看到jwt相关的类了。过分的是生成密钥的代码被出题人删掉了，所以光凭题目给的源码是猜不出密钥的。不过该项目是基于github上某个项目的。

在github项目中，密钥是硬编码写在源码中的，所以我们直接拿过来修改jwt即可。

当然，也可以利用jwtcracker爆破jwt。





