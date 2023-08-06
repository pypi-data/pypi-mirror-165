import requests
def youtube(urly):
    r=requests.get(f"https://www.dragon.clouduz.ru/download-libarary/dlib.php?url={urly}").text
    return r


def tiktok(urlt):
    liba=requests.get(f"https://www.dragon.clouduz.ru/download-libarary/tiktok.php?url={urlt}").text
    return liba

def facebook(urlf):
    fa=requests.get(f"https://www.dragon.clouduz.ru/download-libarary/dlib.php?url={urlf}").text
    return fa

