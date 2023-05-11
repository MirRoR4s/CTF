from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
iv = bytes.fromhex('1df49bc50bc2432bd336b4609f2104f7')
ct = bytes.fromhex('a40c6502436e3a21dd63c1553e4816967a75dfc0c7b90328f00af93f0094ed62')

import itertools

target = b'cvctf{'

for i in itertools.product(range(256),repeat=2):
    tmpKey = bytes(i)
    key = pad(tmpKey, 16)
    cipher = AES.new(key,AES.MODE_CBC,iv)
    tmpM = cipher.decrypt(ct)
    if tmpM.find(target)!=-1:
        print(tmpKey)
        print(tmpM)



