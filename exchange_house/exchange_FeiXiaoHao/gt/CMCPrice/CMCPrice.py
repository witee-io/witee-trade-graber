# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import PretendUrl

if __name__ == "__main__":
    url = "https://coinmarketcap.com/currencies/volume/24-hour/"
    demo = PretendUrl.url(url)
    soup = BeautifulSoup(demo, 'lxml')
    data_list = []  # 结构: [dict1, dict2, ...], dict结构{'排名': rank, '名称': symbol, '流通市值': ...}.
    for idx, tr in enumerate(soup.find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            print(tds)
