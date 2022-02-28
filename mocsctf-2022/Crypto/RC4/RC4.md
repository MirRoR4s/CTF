![1645500604755](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645500604755.png)

题目利用自己的RC4函数生成一个数值，并将明文和该数值的异或值作为密文返回给我们，该数值与密钥有关

![1645501450216](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645501450216.png)

```python
class RC4:
    def __init__(self, key):
        keylength = len(key)

        s = [i for i in range(256)]

        j = 0
        for i in range(256):
            j = (j + s[i] + key[i % keylength]) % 0xff
            s[i], s[j] = s[j], s[i]

        self.i = 0
        self.j = 0
        self.s = s

    def __next(self):
        s, i, j = self.s, self.i, self.j

        i = (i + 1)    % 0xff
        j = (j + s[i]) % 0xff

        s[i], s[j] = s[j], s[i]

        self.s, self.i, self.j = s, i, j

        return s[(s[i] + s[j]) % 0xff]

    def encrypt(self, message):
        return bytes(m^self.__next() for m in message)
```

**仔细阅读RC4这个函数的代码就会发现置换s数组的时候不应该mod 0xff（255） ，应该是与& 0xff ,这导致下标总是在区间0-254内，而s数组原本的值是0-255的有序数字**

![1645501565974](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645501565974.png)

该如何利用这个缺陷呢？

因为最后_next()函数的返回值模上了255，所以s数组下标为255的数字将永远不会被用到去加密![1645502016797](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645502016797.png)

![1645502227905](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645502227905.png)

**所以我们可以不断加密flag ，如果观察到255个不同的c[i]值(c[i]位于0到255之间),那么就知道没有出现的那个c[i]就是s[255] xor m[i]了，由于已知s[255]，所以可以解出m[i] ，最终得到flag**

