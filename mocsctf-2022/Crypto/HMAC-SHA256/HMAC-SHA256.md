**题目要求我们输入N组不同的key跟msg**

 **digest = hmac.digest(key, msg, hashlib.sha256)**

**outputs.append(digest.hex())**

**如果最后 len(set(outputs)) 的长度为1即可拿到flag**

![1645499399023](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645499399023.png)

**当密钥key的长度小于一个块大小，(sha256一个块大小是64字节),密钥key会先在右边填充字节0**

比如key是hello world的话就会被填充为hello world__________________________________________________________________________________________________________________，零用下划线代替。

**所以很容易观察到foo跟foo_将会被填充为一样的key然后生成相同的哈希值**

**所以按照下图的方法构造key发给服务器即可拿到flag**

![1645499533769](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645499533769.png)

```python
from pwn import*
host = "34.136.108.210"
port = "50002"
r = remote(host,port)
for i in range(1,65):
    tmp = '00'*i
    msg = 'ef'
    r.sendline(tmp.encode())
    r.sendline(msg.encode())

print(r.recvline())
r.interactive()

```

