# -*- coding: UTF-8 -*-
# 1次爬取多页面数据.
from bs4 import BeautifulSoup
import time
import DBA
import PretendUrl


def get_Data(url):
    page = PretendUrl.url(url)
    soup = BeautifulSoup(page, 'lxml')
    coinId = ''.join(url.split('/')[1:][3]).lower()
    print(url)
    time.sleep(2)
    for idx, tr in enumerate(soup.find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            rank = tds[0].text
            exchange = tds[1].text.replace('\n', '').replace('\r', '')
            dealgoldplay = tds[2].text
            price = tds[3].text
            vol = tds[4].text
            amount = tds[5].text
            percentchange = tds[6].text
            tradinghour = tds[7].text
            sql = "INSERT INTO  tb_exchange (rank,coinId,exchange,dealgoldplay,price,vol,amount,percentchange,tradinghour) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"
            # DBA.insertObject(
            #     sql,
            #     rank,
            #     coinId,
            #     exchange,
            #     dealgoldplay,
            #     price,
            #     vol,
            #     amount,
            #     percentchange,
            #     tradinghour
            # )
            print(
                # sql,
                rank,
                coinId,
                exchange,
                dealgoldplay,
                price,
                vol,
                amount,
                percentchange,
                tradinghour
            )


def findCoinName():
    url_list = []
    sql = "SELECT name FROM fxhprice ORDER BY rank"
    # sql = "SELECT name FROM fxhprice WHERE name = 'bitcoin' ORDER BY rank"
    for i in DBA.findObjects(sql):
        x = list(i)
        for tt in x:
            url_list.append('https://www.feixiaohao.com/coinmarket/' + ''.join(tt))
    return url_list


if __name__ == '__main__':
    url_list = findCoinName()
    print('Waiting for ...')
    t1 = time.time()
    for url in url_list:
        get_Data(url)
    t2 = time.time()
    print('Done. use %0.2f seconds' % (t2 - t1))
