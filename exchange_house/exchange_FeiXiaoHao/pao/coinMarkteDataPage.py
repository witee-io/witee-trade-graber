import urllib
from datetime import time
from os import mkdir
import  requests
import  urllib.request
from bs4 import BeautifulSoup
import dataBase
#伪装浏览器头
headers={
            'User_Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }

def getHttpText(url):
    print()
    try:
        r=requests.get(url,headers)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return "产生异常"


if __name__ == "__main__":
    url="https://coinmarketcap.com/exchanges/volume/24-hour/"
    demo =getHttpText(url)
    soup=BeautifulSoup(demo,'html.parser')
    data_list = []  # 结构: [dict1, dict2, ...], dict结构{'排名': rank, '名称': symbol, '流通市值': ...}
    regStr =soup.find_all('table')
    for list in regStr:
        tds=list.find_all('td')
        print(
            tds[0].text+" ",
            tds[1].text+" ",
            tds[2].text+" ",
            tds[3].text+" ",
            tds[4].text+" ",
            tds[5].text+" ",
            tds[6].text+" ",
        )
    #print(data_list)
