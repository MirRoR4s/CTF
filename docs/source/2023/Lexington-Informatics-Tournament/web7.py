import requests
from PIL import Image
from io import BytesIO
def main():
    url = "http://litctf.org:31770/runHTML"
    
    with open("./exp.html","rb") as file:
        files = {"file" : ("exp.html", file, 'text/html')}
        r = requests.post(url=url,files=files)
        ans = r.content
        image = Image.open(BytesIO(ans))
        image.save("flag.png")
        print("check!")
    
    

if __name__ == "__main__":
    main()
