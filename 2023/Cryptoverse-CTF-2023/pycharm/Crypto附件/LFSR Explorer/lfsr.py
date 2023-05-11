from Crypto.Util.number import *
from secret import flag

assert flag.startswith("cvctf{")
assert flag.endswith("}")

flag = flag[6:-1].encode()
assert len(flag) == 8

def explore(state, mask):
    curr = (state << 1) & 0xffffffff # 将 state 乘以 2，然后保留最低 4 字节
    i = state & mask & 0xffffffff # state 掩码按位与
    last = 0
    '''
    while 循环依次遍历 i 的最低位到最高位，所以 last 实质上是 i 的二进制表示中取值为 1 的那些位的 异或
    '''
    while i != 0:
        last ^= (i & 1)
        i >>= 1
    curr ^= last # curr 最低位的零 变为 last 的值，若 i 有奇数个 1，那么 last 值为1，即 curr最低位为1
    return (curr, last)

states = [bytes_to_long(flag[4:]), bytes_to_long(flag[:4])]
mask = 0b10000100010010001000100000010101

output = []
for i in range(8):
    tmp = 0
    for j in range(8):
        (states[i // 4], out) = explore(states[i // 4], mask) # states 总长是2，那么 i=0-4 时都取 states[0]，5-7 取 states[1]
        tmp = (tmp << 1) ^ out
    output.append(tmp) # tmp 的二进制表示蕴含着 lsfr 的输出是什么，这一点很重要。

with open("output.txt", "wb") as f:
    f.write(bytes(output))
