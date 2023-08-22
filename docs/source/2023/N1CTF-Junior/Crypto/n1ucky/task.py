# !/usr/bin/env python3
import socketserver
import os
import signal
import string
import random
from hashlib import sha256
from Crypto.Util.number import *
from secret import flag


BANNER = br"""                                                                                                
::::    :::   :::  :::    :::  ::::::::  :::    ::: :::   ::: 
:+:+:   :+: :+:+:  :+:    :+: :+:    :+: :+:   :+:  :+:   :+: 
:+:+:+  +:+   +:+  +:+    +:+ +:+        +:+  +:+    +:+ +:+  
+#+ +:+ +#+   +#+  +#+    +:+ +#+        +#++:++      +#++:   
+#+  +#+#+#   +#+  +#+    +#+ +#+        +#+  +#+      +#+    
#+#   #+#+#   #+#  #+#    #+# #+#    #+# #+#   #+#     #+#    
###    #### ####### ########   ########  ###    ###    ###         
"""

MENU = br"""
1. guess
2. exit
"""


class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'[+] '):
        self.send(prompt, newline=False)
        return self._recvall()

    def recvint(self, prompt=b'> '):
        self.send(prompt, newline=False)
        try:
            data = int(self._recvall().decode('latin-1'))
        except ValueError:
            self.send(b"Wrong type")
            self.close()
            return None
        return data

    def close(self):
        self.send(b"Bye~")
        self.request.close()

    def proof_of_work(self):
        random.seed(os.urandom(8))
        proof = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(20)])
        _hexdigest = sha256(proof.encode()).hexdigest()
        self.send(f"sha256(XXXX+{proof[4:]}) == {_hexdigest}".encode())
        x = self.recv(prompt=b'Give me XXXX: ')
        if len(x) != 4 or sha256(x + proof[4:].encode()).hexdigest() != _hexdigest:
            return False
        return True

    def handle(self):
        signal.alarm(120)

        if not self.proof_of_work():
            return

        self.send(BANNER)
        secret = random.getrandbits(4096)

        time = 0
        self.send("Nu1L's 🚩 are only for the lucky people~".encode())
        self.send("😊 Try to prove you're lucky enough!".encode())

        while time < 20:
            self.send(MENU, newline=False)
            choice = self.recv()
            time += 1

            if choice == b"1":
                p = getPrime(888)
                r = getPrime(30)
                res = r * secret % p
                self.send("\n🎁 here : {}, {}\n".format(res, p).encode())
                guess = self.recvint(prompt=b"Your guess > ")
                if guess == secret:
                    self.send("🎉 So lucky!!! Here is your flag: ".encode() + flag)
                    self.close()
                    break
                else:
                    self.send("👻 A little hapless".encode())
                continue

            self.close()
            break

        self.send("\n\n💀 No Chance!".encode())
        self.close()


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10000
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()

