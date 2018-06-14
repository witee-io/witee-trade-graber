# -*- coding: UTF-8 -*-
# 1次爬取多页面数据.
import json
from bs4 import BeautifulSoup
import time
import DBA
import Logs
import PretendUrl


def get_Data(url):
    page = PretendUrl.url(url)
    soup = BeautifulSoup(page, 'lxml')
    soup = soup.text
    try:
        str_soup = soup.replace(",,", "null,null,")
        data = json.loads(str_soup)
    except:
        Logs.logger.info(url + 'json解析异常')
        print(url + 'json解析异常')
    # data=soup.text
    maxsupply = data['market_cap_by_available_supply']
    pricebtc = data['price_btc']
    priceusd = data['price_usd']
    hvolumeusd = data['vol_usd']
    coinname = ''.join(url.split('/')[1:][3]).lower()
    num = 0
    tds = 1
    time.sleep(10)
    for tt in maxsupply:
        if tds == 17:
            tds = 1
        tabaName = "tb_brokenlile_" + str(tds)
        sql = "INSERT INTO " + tabaName + " (name,maxsupply,pricebtc,priceusd,hvolumeusd) VALUES ('%s','%s','%s','%s','%s')"
        DBA.insertObject(
            sql,
            coinname,
            str(maxsupply[num]),
            str(pricebtc[num]),
            str(priceusd[num]),
            str(hvolumeusd[num])
        )

        # 测试
        num = num + 1
        tds = tds + 1


def findCoinName():
    url_list = []
    # sql = "SELECT name FROM fxhprice ORDER BY rank"
    sql = "SELECT name FROM fxhprice WHERE name = 'bitcoin' ORDER BY rank"
    for i in DBA.findObjects(sql):
        x = list(i)
        for tt in x:
            url_list.append('https://api.feixiaohao.com/coinhisdata/' + ''.join(tt))
    return url_list


if __name__ == '__main__':
    url_list = findCoinName()
    print('Waiting for ...')
    t1 = time.time()
    num = 1
    for url in url_list:
        print("第" + str(num) + "个币种" + "路径：" + url)
        get_Data(url)
        num = num + 1
    t2 = time.time()
    print('Done. use %0.2f seconds' % (t2 - t1))
