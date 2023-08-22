import requests

def run(url):
    data = {
        "username" : "admin",
        "password" : "dGhpcyBpcyBzb21lIGdpYmJlcmlzaCB0ZXh0IHBhc3N3b3Jk"
    }
    r = requests.post(url=url,json=data)
    ans = r.text
    print(ans)

if __name__ == "__main__":
    run("http://litctf.org:31784/login.php")