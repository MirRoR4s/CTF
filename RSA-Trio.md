![1645415852787](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645415852787.png)



当连接到服务器，会产生三个1024bit的素数 p,q,r. 让n1 = pq, n2= qr, n3 = rp  ,且三个素数使用相同的e来生成，

![1645416415566](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645416415566.png)

![1645415956295](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645415956295.png)



从上图可以看到一个原始消息m被加密了三次,且加密模数从小到大排序,我们设为 n1 < n2 < n3, 最终返回一个密文c，三次加密都使用了相同的e. 服务器的提供了一个加密功能，**我们可以自由选择明文加密**，但是如果选择的明文 不能大于其加密过程中的模数 n1 n2 n3 ，否则返回空. **现在可执行的操作是拥有加密后的flag，自由加密任意符合大小的明文，该如何恢复flag？**



解决方案：

复原 n1

![1645416465747](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645416465747.png)

题目要求每一轮作为加密的信息都必须位于其模数的区间之内

比如第一轮用我们传入的m进行加密，m必须位于[0,n1)之间，m加密之后的结果t1作为第二轮加密的信息，t1必须位于[0,n2)之间，t2同理也必须位于[0,n3)之间.

**这个m是我们可以控制的，每一轮连接服务器都会生成这三个素数，而且保持不变。只要我们通过二分法不断的输入一个m，如果m满足m+1是空，且m不空，那么m+1就是n1，通过这种方法我们就找到了n1**. 为什么是n1呢？换句话说为什么能保证加密失败那么这个数一定是大于n1而不是其他数呢？

**(我们假设第一轮符合加密的要求，也就是0<m<n1 ，于是t1=pow(m,e,n1) ，由于取模操作，t1是肯定小于n1的，而n1 < n2 < n3，所以说从第二轮开始的所有加密的数都是肯定满足要求的，也就是说如果加密失败那么问题一定是出在加密过程的第一轮，即我们输入的数大于n1了！)**

找到了n1，不妨看看如何找出n2 n3 

应该没有很好的办法找出n2来，但是却可以很轻松地找到n3

![1645445921493](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645445921493.png)

注意到 e= 0b10001 不是0x10001 所以e应该是17 ，果然细节一定要注意！！

我们可以构造一组m，使得a =pow(m,289) 小于n2而pow(m,4913)大于等于n3 ，所以最终的加密结果c其实就是pow(a,e,n3)除以n3的余数，转化为算式即 kn3 = pow(m,4913) - c.

 比如找一组m0=2,m1=3 。 这两组转为算式之后的最大公约数就是n3的倍数，然后我们再枚举一下k就可以得到n3啦，或者更具体的去检查当前枚举的n3是否能被小素数整除![1645446303684](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645446303684.png)

![1645446431686](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645446431686.png)

得到了n1,n3 所以可以求出p q r进而求出每一轮加密的d，进而求出欧拉函数值，最终解密获得flag

![1645448632566](C:\Users\镜子\AppData\Roaming\Typora\typora-user-images\1645448632566.png)



```python
#二分查找n1的脚本
from pwn import *
from demical import *
n1 = 0
def via_Binary_Search(r,left,right):
    cnt = 0
    flag = 0
    print("加密后的flag=",r.recvline())
    while(left <= right ):
        print(cnt)
       # print("right-left=",right-left)
        getcontext().prec = 2048
        mid = (left) + ((right-left)//2)
        print("mid=",mid)
        tmp = str(mid).encode()
        r.sendline(tmp)
        sleep(0.1)
        rec = r.recvline()
        sleep(0.1)
        tmp1 = str(mid+1).encode()
        r.sendline(tmp1)
        sleep(0.1)
        rec1 = r.recvline()
       # print("tmp=",tmp)
        #print("tmp1=",tmp1)
       # print("rec=",rec)
        #print("rec1=",rec1)
        assert int(tmp1)-int(tmp)==1
        if rec != b'> None\n' and rec1 ==b'> None\n':
            print("n1=",tmp1)
            n1 = tmp1
            flag = 1
            break
        elif rec ==b'> None\n' and rec1 ==b'> None\n':
            print("b")
            right = mid - 1
        elif rec !=b'> None\n' and rec1!=b'> None\n':
            print("s")
            left = mid + 1

    return flag,left

host = '34.136.108.210'
port = '50005'
r = remote(host,port)
flag,left = via_Binary_Search(r,0,2**2048)
if flag==0:
    r.sendline(str(left).encode())
    rec = r.recvline()
    if rec==b'> None\n':#还是大，继续二分
        via_Binary_Search(r,0,left)

    else : #小了，从当前开始逐步递增
        num = left + 1
        r.sendline(str(num).encode())
        rec = r.recvline()
        while (rec !=b'> None\n'):
            num = num + 1
            r.sendline(str(num).encode())
        print("num=",num)


r.interactive()


```











