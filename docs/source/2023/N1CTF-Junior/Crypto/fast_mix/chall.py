from Crypto.Util.number import *
from secret import flag

assert len(flag) == 48
gift = b'yX~\xe1\xd3\xe7\xcdw_)/G\xdc\x0er\x18\xc0\xb2\xc1sKv\xd4\x857\x94D\xf91\xc2\x98\x873\x8bG\xc3hG\xbbC\x98\x16e\xe8\x11C\n\x04'
block_size = 16
date = bytes_to_long(b'2023-1-31 10:00')
f1 = lambda x: (x << 1) ^ 0b110100011 if x & 0x80 else x << 1
f2 = lambda x: x ^ f1(f1(x))
f3 = lambda x: f1(f1(f1(x))) ^ f1(f1(x))


def slow_func(init, time):
    tmp = init
    for _ in range(time):
        tmp = sum([[
            f3(tmp[j]) ^ f2(tmp[j+1]) ^ f2(tmp[j+2]) ^ f1(tmp[j+3]),
            f1(tmp[j]) ^ f3(tmp[j+1]) ^ f1(tmp[j+2]) ^ f2(tmp[j+3]),
            f3(tmp[j]) ^ f2(tmp[j+1]) ^ f3(tmp[j+2]) ^ f2(tmp[j+3]),
            f2(tmp[j]) ^ f1(tmp[j+1]) ^ f2(tmp[j+2]) ^ f3(tmp[j+3])
        ] for j in range(0, 16, 4)], [])
    return bytes(tmp)


v = b''
for i in range(0, len(flag), block_size):
    block = gift[i:i+block_size]
    v += slow_func(block, date)

assert flag == v
