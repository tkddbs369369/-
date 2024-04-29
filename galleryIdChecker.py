import requests
from bs4 import BeautifulSoup
import operator
import time
import re
import os


def request(url):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'gall.dcinside.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    try:
        url_get = requests.get(url, headers=header)
    except:
        url_get = requests.get(url, headers=header)
    return url_get


def gall_check(mg: bool, gall: str) -> (bool, str) :
    if mg:
        recept = request(f"http://gall.dcinside.com/board/lists/?id={gall}")
    else:
        recept = request(f"http://gall.dcinside.com/mgallery/board/lists?id={gall}")
    soup = BeautifulSoup(recept.text, "html.parser")
    meta_data = soup.find_all("meta", {"name": "title"})
    comp = re.findall("\"(.*갤러리)", str(meta_data))
    if comp == []:
        if mg != True:
            return (False, "망갤")
        else:
            return gall_check(False, gall)
    else:
        gall_name = comp[0]
        tuple = (mg, gall_name)
        return tuple
