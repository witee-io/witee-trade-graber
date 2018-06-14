# encoding:utf-8
# 多线程爬取多页面数据.
from multiprocessing import Pool
from bs4 import BeautifulSoup
import os, time

import DBA
import PretendUrl


def get_Data(url):
    start = time.time()
    page = PretendUrl.url(url)
    soup = BeautifulSoup(page, 'lxml')
    data = soup.find_all('table', class_='table common_style')
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
    t1 = time.time()
    print('Parent process %s.' % os.getpid())
    p = Pool()
    url_list = findCoinName()
    print(url_list)
    for url in url_list:
        p.apply_async(get_Data, args=(url,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    t2 = time.time()
    print('All subprocesses done. use %0.2f seconds' % (t2 - t1))
