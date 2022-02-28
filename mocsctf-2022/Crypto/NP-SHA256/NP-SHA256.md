**题目复制了python的sha256算法实现，但是同时删除了一些行**

![1645496509232](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645496509232.png)

**这道题的考点就是让做题者找到两个不同的明文的哈希碰撞，且这两个明文的长度至少是64byte**

题目其实简单到不行，只需要让m1是64个null bytes ，m2 是65个null bytes，这样就满足题目要求拿到flag

![1645496717047](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645496717047.png)

```
[>] 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
[>] 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
[<] Good! MOCSCTF{ev3ry_d3t41l_1n_cryp70gr4phy_m4t73rs}
```

**但是为什么这样就能产生相同的哈希值呢？让我们分析一下**：

我们可以输入一个**空的m3** 和**一个null byte的m4** 并看一下他们哈希值的计算过程：

![1645496786991](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645496786991.png)

让我们把generate_hash 函数复制过来解释一下生成哈希值的过程吧！

![1645496967416](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645496967416.png)

```python
def generate_hash(message: bytearray) -> bytearray:
    """Return a SHA-256 hash from the message passed.
    The argument should be a bytes, bytearray, or
    string object."""

    if isinstance(message, str):
        message = bytearray(message, 'ascii')
    elif isinstance(message, bytes):
        message = bytearray(message)
    elif not isinstance(message, bytearray):
        raise TypeError

    # Padding
    length = len(message) * 8
    message.append(0x80)

    # [MYSTIZ'S COMMENT]
    # At this stage,
    #   message = bytes.fromhex("80")   # -- for m3
    #   message = bytes.fromhex("0080") # -- for m4

    blocks = []
    for i in range(0, len(message), 64): # 64 bytes is 512 bits
        blocks.append(message[i:i+64])

    # [MYSTIZ'S COMMENT]
    # At this stage,
    #   blocks = [bytes.fromhex("80")]   # -- for m3
    #   blocks = [bytes.fromhex("0080")] # -- for m4

    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h5 = 0x9b05688c
    h4 = 0x510e527f
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19

    # [MYSTIZ'S COMMENT]
    # Since there is only one block, I'll rewrite below without losing the meaning:
    message_block = blocks[0]

    message_schedule = []
    for t in range(0, 64):
        if t <= 15:
            message_schedule.append(bytes(message_block[t*4:(t*4)+4]))
            # [MYSTIZ'S COMMENT]
            # At this stage,
            #   message_schedule[0] = bytes.fromhex("80")   # -- for m3
            #   message_schedule[0] = bytes.fromhex("0080") # -- for m4
            # and for i = 1, 2, ..., 15
            #   message_schedule[i] = b""                   # for both m3 and m4
            #这里应该是讲错了，不是说m3跟m4的message_schedule[i]相等，是m4的m_s[i]是m3的倍数，后面计算t1的时候会mod 2的32次方，导致最终计算的t1相同，从而最终哈希值相等
        else:
            term1 = _sigma1(int.from_bytes(message_schedule[t-2], 'big'))
            term2 = int.from_bytes(message_schedule[t-7], 'big')
            term3 = _sigma0(int.from_bytes(message_schedule[t-15], 'big'))
            term4 = int.from_bytes(message_schedule[t-16], 'big')
            #这里m3对应的term4=128,m4对应的term4=3158144，其他term的话m3跟m4是相同的，因为他们除了第一个字节不同，其他字节填充了相同的b'',而3158144 % 128 = 0

            schedule = ((term1 + term2 + term3 + term4) % 2**32).to_bytes(4, 'big')
            #到这里m3对应的schedule为b'\x00\x00\x00\x80'
            #m4对应的schedule为b'\x0000\x80'
            message_schedule.append(schedule)
            # [MYSTIZ'S COMMENT]
            # For i = 16, 17, ..., 64, message_schedule[i] for m3 and m4 are equal.
            # This is because that the big-endian representations for
            # bytes.fromhex("80") and bytes.fromhex("0080") are the same.

    assert len(message_schedule) == 64

    # (omitted)

    for t in range(64):
        t1 = ((h + _capsigma1(e) + _ch(e, f, g) + K[t] +
                int.from_bytes(message_schedule[t], 'big')) % 2**32)
        # [MYSTIZ'S COMMENT]
        # t1 on the i-th round looks for the big-endian representation for
        # message_schedule[i]. That said, t1 for m3 and m4 would always be the same.
        # After all, this makes a, b, ..., h for both m3 and m4 equal for each round.

        # (omitted)
    
    # [MYSTIZ'S COMMENT]
    # Now h0, h1, ..., h7 for both m3 and m4 are equal.
    # That would imply the digests would be the same.
    h0 = (h0 + a) % 2**32
    h1 = (h1 + b) % 2**32
    h2 = (h2 + c) % 2**32
    h3 = (h3 + d) % 2**32
    h4 = (h4 + e) % 2**32
    h5 = (h5 + f) % 2**32
    h6 = (h6 + g) % 2**32
    h7 = (h7 + h) % 2**32

    return ((h0).to_bytes(4, 'big') + (h1).to_bytes(4, 'big') +
            (h2).to_bytes(4, 'big') + (h3).to_bytes(4, 'big') +
            (h4).to_bytes(4, 'big') + (h5).to_bytes(4, 'big') +
            (h6).to_bytes(4, 'big') + (h7).to_bytes(4, 'big'))
```

m1 跟 m2 本质上是相同的，除了初始值h0-h7不同，接下来请自行分析作为练习

![1645497105861](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645497105861.png)

解题脚本

```python
from pwn import*
host = "34.136.108.210"
port = "50004"
r = remote(host,port)
s1 = '00'*64
s2 = '00'*65
r.sendline(s1.encode())
r.sendline(s2.encode())
print(r.recvline())
r.interactive()
```

