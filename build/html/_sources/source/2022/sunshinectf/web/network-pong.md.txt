---
description: >-
  https://github.com/MirRoR4s/SunshineCTF-2022-Public/tree/master/Web/network-pong
---

# Network Pong

简单的命令注入，不能使用空格。简单的模糊测试可以探查到执行的命令是什么样式的。

有一个点比较有意思，不用cat、head、tail如何看flag的内容呢？作者用到了grep -r 命令，这个命令可以递归地搜索指定模式或字符串，如果搜索到了就会显示出来。

所以 grep -r sun 就找到了flag。
