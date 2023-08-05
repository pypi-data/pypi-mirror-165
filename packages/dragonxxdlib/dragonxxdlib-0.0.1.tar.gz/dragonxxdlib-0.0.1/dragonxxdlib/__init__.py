import requests
def youtube(urly):
    r=requests.get(f"https://www.dragon.clouduz.ru/download-libarary/dlib.php?url={urly}").text
    return r


def tiktok(urlt):
    liba=requests.get(f"https://www.dragon.clouduz.ru/download-libarary/tiktok.php?url={urlt}").text
    return liba

