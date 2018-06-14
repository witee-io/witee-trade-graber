import requests
import re, sys
import time
import pymysql
sys.path.append("..")
from exchange_rate import USDCNY
from forex_python.converter import CurrencyRates
from DBUtils.PooledDB import PooledDB
def req1():
    usdlist = {}
    req = requests.get(url,proxies={'http':'http://192.168.0.252:8118','https':'http://192.168.0.252:8118'},headers=head)
    #req = requests.get(url,headers=head)
    for i in req.json()['data']:
        b = re.split('_',i['symbol'])
        if (b[0].upper() not in list(usdlist.keys())) and (b[1] == 'usdt'):
            usdlist[b[0].upper()] = round(float(i['close']),4)
    for x in req.json()['data']:
        y = re.split('_',x['symbol'])
        if y[0].upper() not in list(usdlist.keys()):
            usdlist[y[0].upper()] = round(float(usdlist[y[1].upper()])*float(x['close']),4)
    return usdlist
def sqlr(s):
    conn1 = pool.connection()
    cursor1 = conn1.cursor()
    sql1 = '''replace into  exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)VALUES(%s,%s,%s,%s,now())'''
    for i in s.keys():
        cursor1.execute(sql1, (i,'okex',s[i],USDCNY ))
    conn1.commit()
if __name__ == '__main__':
    url = 'https://www.okex.com/v2/spot/markets/tickers'
    head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',port=3306)
    while 1:
        try:
            req = req1()
            sqlr(req)
            print('over')
            time.sleep(10)
        except Exception as e:
            print(e)
