# 前言

记录 CTF 的学习过程。


## 计划表
目前我的想法是把2023年可以获取到源码从而进行复现的比赛全部复现完。
1. TetCTF
2. [IrisCTF 2023](https://github.com/IrisSec/IrisCTF-2023-Challenges)

## 环境搭建
1. 采用 [ubuntu 23.04](https://ubuntu.com/download/desktop) 作为镜像机。
2. 利用 [v2raya](https://v2raya.org/) 科学上网，记住安装完毕之后打开浏览器本地2017端口配置vpn，同时注意配置相应的代理设置（这一步很重要）
- 代理真真真太重要了，否则拉取镜像的时候你会感受到什么叫怀疑人生，我在拉取gcr.io的镜像时疯狂连接被拒绝、超时等等等。
- 很多时候拉取镜像的时候要求身份认证的，所以一定要docker login登录一下。
3. 安装docker，参看[菜鸟教程](http://www.runoob.com/docker/ubuntu-docker-install.html)

4. 解决普通用户docker ps、images 等权限否认问题：https://blog.csdn.net/qq_21139827/article/details/127607011?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-127607011-blog-119377535.235%5Ev38%5Epc_relevant_sort_base3&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-127607011-blog-119377535.235%5Ev38%5Epc_relevant_sort_base3&utm_relevant_index=1

- 软件源使用的是[清华大学](https://mirrors.tuna.tsinghua.edu.cn/help/kali/)的
