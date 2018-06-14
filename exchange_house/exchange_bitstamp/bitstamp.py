import requests
import re, sys
sys.path.append("..")
from exchange_rate import USDCNY
import pymysql
import time
from DBUtils.PooledDB import PooledDB
pair = ['btcusd','xrpusd','ltcusd','ethusd','bchusd']
def req1():
    data = {}
    for i in pair:
        url = 'https://www.bitstamp.net/api/v2/transactions/'+i
        req = requests.get(url,timeout=10)
        symbol1 = re.match('.*(?=usd)',i).group().upper()
        data[symbol1] = round(float(req.json()[0]['price']),4)
    return data
def sqlr(s):
    conn1 = pool.connection()
    cursor1 = conn1.cursor()
    sql1 = '''replace into  exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)VALUES(%s,%s,%s,%s,now())'''
    for i in s.keys():
        cursor1.execute(sql1, (i,'bitstamp',s[i],USDCNY ))
    conn1.commit()
    conn1.close()
if   __name__ == '__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',port=3306)
    while 1:
        try:
            req = req1()
            sqlr(req)
            print('over')
            time.sleep(10)
        except Exception as e:
            pass
            print(e)
