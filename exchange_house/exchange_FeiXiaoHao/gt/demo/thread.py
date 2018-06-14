# -*- coding: UTF-8 -*-
# 1次爬取多页面数据.
from bs4 import BeautifulSoup
import time
import requests

import DBA
import PretendUrl


def get_Data(url):
    start = time.time()
    page = PretendUrl.url(url)
    soup = BeautifulSoup(page, 'lxml')
    data = soup.find_all('div', class_='table-responsive')
    end = time.time()
    print('%s runs %0.2f seconds.' % (data, (end - start)))


def findCoinName():
    url_list = []
    for i in DBA.findAllName():
        x = list(i)
        for tt in x:
            url_list.append('http://gthe.shop/coin/findBySymbol/' + ''.join(tt))
    return url_list

if __name__ == '__main__':
    url_list = findCoinName()
    print(url_list)
    print('Waiting for ...')
    t1 = time.time()
    for url in url_list:
        get_Data(url)
    t2 = time.time()
    print('Done. use %0.2f seconds' % (t2 - t1))
