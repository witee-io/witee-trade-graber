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
    url="https://www.feixiaohao.com/all"
    demo =getHttpText(url)
    soup=BeautifulSoup(demo,"lxml")
    data_list = []  # 结构: [dict1, dict2, ...], dict结构{'排名': rank, '名称': symbol, '流通市值': ...}
    for idx, tr in enumerate(soup.find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            # data_list.append({
            #     '排名': tds[0].contents[0],
            #     '名称': tds[1].contents[1].find('img').attrs.get('alt').split('-')[0:1],
            #    # '图片':tds[1].contents[1].find('img').attrs.get('src'),
            #     '流通市值': tds[2].contents[0],
            #     '价格': tds[3].contents[0].text,
            #     '流通数量': tds[4].contents[0],
            #     '流通率': tds[5].contents[0],
            #     '成交额(24h)': tds[6].contents[0].text,
            #     '涨幅(1h)': tds[7].contents[1].text,
            #     '涨幅(24h)': tds[8].contents[1].text,
            #     '涨幅(7d)': tds[9].contents[1].text
            # })
            # tu = tds[1].contents[1].find('img').attrs.get('src')#币种图片
            name = tds[1].contents[1].find('img').attrs.get('alt').split('-')[0:1] #币种名称
            dataBase._replaceObject_(
                tds[0].contents[0],
                ''.join(name),
                tds[2].contents[0],
                tds[3].contents[0].text,
                tds[4].contents[0],
                tds[5].contents[0],
                tds[6].contents[0].text,
                tds[7].contents[1].text,
                tds[8].contents[1].text,
                tds[9].contents[1].text
            )
            # print(tds[0])

    #print(data_list)
    #print(data_list)