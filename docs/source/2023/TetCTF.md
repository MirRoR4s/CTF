# TetCTF 2023

## 前言

每年过年越南似乎都会举办一场ctf比赛，这也是ctftime上2023年的第一场ctf比赛。

源码：https://drive.google.com/file/d/13QLDDnauyMogu8RX-xLqB8jP-degF28d/view

## WEB

### NewYearBot

**题目描述**

**Description**
New Year New Code! My friend decide to learn code in new year, here his very first website: http://172.105.120.180:9999/

**File**
He said it is very secure because he is very strict on what user can input, can you check?
https://drive.google.com/file/d/1tU18ePUAHHYpxJ9QhdVKBpuBm_eXy--r/view?usp=sharing

**Note**
Don't generate excessive load. Scanning/Dirbust is not needed.

#### 题目分析

这是一个传入type和number然后回显对应的问候语的应用。type用于选择特定的问候语列表，number选择列表中的元素。一番审计感觉应该是下面这个地方的代码有问题：

![image-20230825065628741](../../_static/images/image-20230825065628741.png)

对于传入的type仅做了一个变量名是否合法的校验，这里或许可能执行任意的函数，而非是题目期望的问候语列表。

flag是在FL4G这个变量里面，所以很自然的想法就是显示该变量的内容。如果传入的type为FL4G，那么肯定希望number是对应的下标索引。但是number有一个botValidator函数过滤，该函数限制了number各个字符的ascii值不可以在57-123之内，并且数字部分总长度不可以超过最长的问候语列表的长度。（最大长度是 6）那么我们传入的 number 必须小于等于 5 。所以如何截取剩余的flag字符呢？我看到的有两种手法：

**slice切片结合同型字符**

python的 [slice](https://www.runoob.com/python/python-func-slice.html) 

我们只要得到一个截取很多个元素的切片 myslice，然后通过 FL4G[myslice] 不就可以截取出 flag 来了么？只要截取元素够多，就可以拿到完整的 flag。

要调用 slice 函数，我们需要得到一个整数，在 python 下，id 函数用于获取对象的唯一标识符，而标识符是一个整数，所以我们可以通过 slice(id(对象)) 来得到一个元素切片。而这个对象我们有很多种选择，比如在题目源码中导入的几个模块 re、random等，不过长度尽量短，因为我们传入的 number 参数是有长度限制的。例如我们可以选择 `number=slice(id(re))`

但是还有一个很关键的问题，那就是题目不允许我们传入 ascii 码值在 57 和 123 之间的字符

我们可以通过传入 `slice(id(re))` 的 **unicode 同形字符**来绕过这个限制，尽管说这些并不是 ascii 字符，但是 python 会自动 normalize 它们。[同形字符](https://www.freebuf.com/vuls/229446.html) 𝔰𝔩𝔦𝔠𝔢(𝔦𝔡(𝔯𝔢))



**位运算**

[Python Bitwise Operators](https://www.w3schools.com/python/gloss_python_bitwise_operators.asp)

`~` 是 python 中的 取反运算符。

`-~5` 会得到 `6` ，关于其底层原理，可以看这篇文章：[取反运算符~详解](https://zhuanlan.zhihu.com/p/261080329)。而减号和波浪号是在允许的 ascii 码值范围内，所以我们可以通过这种手法拿到 flag 的第六个字符

```
type=FL4G&number=𝔰𝔩𝔦𝔠𝔢(𝔦𝔡(𝔯𝔢)) # POST
```

```
-~0-~4 -> 6
-~0-~5 -> 7
-~0-~0-~5 -> 8
-~0-~0-~0-~5 -> 9
(-~0-~0)*5 -> 10
~0-(-~0-~0)*~5 -> 11
(-~0-~0-~0)*4 -> 12
~0-(-~0-~0)*5 -> -11
(-~0-~0)*~4 -> -10
~(-~0-~0)*3 -> -9
(-~0-~0)*~3 -> -8
~0--~5 -> -7
~5 -> -6
~4 -> -5
~3 -> -4
~2 -> -3
~1 -> -2
~0 -> -1
```

### Image Services Viewer

**题目描述**

Do you know secret which on my server!!!!

源码地址：https://drive.google.com/file/d/1K8XJXrdwEgJWGwu2V3cqLiZUo4nrdweM/view?usp=share_link

#### 题目分析



