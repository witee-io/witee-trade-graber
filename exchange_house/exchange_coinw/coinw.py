#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
from forex_python.converter import CurrencyRates
import pymysql
import time
from DBUtils.PooledDB import PooledDB
USDCNY = CurrencyRates().get_rates('usd')['CNY']
coinsymbol = {'ETH': '14', 'Coins': '31', 'Hsr': '5', 'SDA': '30', 'BDG': '32', 'Chat': '33', 'snt': '24', 'Storj': '23', 'Rct': '36', 'WICC': '28', 'EOS': '29', 'Doge': '25', 'Dew': '20', 'MAG': '21', 'Rnt': '19', 'Dat': '18', 'AE': '15', 'hpy': '17', 'Data': '16', 'OMG': '11', 'Kyber': '12', 'MANA': '10', '0X': '7', 'TNT': '9', 'STX': '6', 'CDT': '8', 'BC': '2'}
head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
def trades():
    a = {}
    for i in coinsymbol.keys():
        url = 'https://www.coinw.com/appApi.html?action=trades&symbol='+coinsymbol[i]
        req = requests.get(url,proxies={'http':'http://192.168.0.252:8118','https':'http://192.168.0.252:8118'},headers=head,timeout=10)
        #print(req.json()['data'][0]['price'],'aaaa')
        b = req.json()['data'][0]['price']
        a[i.upper()] = round(float(b)/float(USDCNY),4)
    return a
def sqlr(s):
    conn1 = pool.connection()
    cursor1 = conn1.cursor()
    sql = '''replace into  exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)VALUES(%s,%s,%s,%s,now())'''
    for i in s.keys():
        cursor1.execute(sql, (i,'coinw',s[i],USDCNY ))
    conn1.commit()
    conn1.close()
if __name__ == '__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',port=3306)
    while 1:
        try:
            while 1:
                t = time.time()
                sqlr(trades())
                print(time.time()-t)
                time.sleep(10)
        except Exception as e:
            print(e)
