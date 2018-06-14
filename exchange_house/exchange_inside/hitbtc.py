#-*-coding=utf-8-*-

import requests,datetime
import json,re
#import DBA
from exchange_rate import USDCNY
from pymysql import *
import pymysql
from DBUtils.PooledDB import PooledDB

def get_data():
    exc_code = 'hitbtc'
    proxys = {'http': 'http://192.168.0.252:8118', 'https': 'https://192.168.0.252:8118'}

    url = 'https://api.hitbtc.com/api/2/public/ticker'
    response = requests.get(url, proxies=proxys)
    #response = requests.get(url)
    result = json.loads(response.text)
    #print(result)
    conn = pool.connection()
    cursor = conn.cursor()
    for x in result:
        pattern=re.compile(r'BTCUSD')
        name=re.match(pattern,x['symbol'])
        try:
            name=name.group()
        except Exception as e:
            name='None'
        if name!='None':
            name='BTC'
            prices=float(x['last'])
            prices=round(prices,4)
            nows = datetime.datetime.now()
            now = nows.strftime('%Y-%m-%d %H:%M:%S')
            # conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',
            #                charset='utf8mb4')
            # cursor = conn.cursor()
            sql = "insert into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)values('" + name + "','" + exc_code + "','" + str(
                prices) + "','" + str(
                USDCNY) + "','" + now + "') ON DUPLICATE KEY UPDATE create_date=VALUES(create_date),now_price=values(now_price),exchange_rate=VALUES(exchange_rate)"
            cursor.execute(sql)
            conn.commit()
    cursor.close()
    conn.close()
    conn = pool.connection()
    cursor = conn.cursor()
    for x in result:
        pattren=re.compile(r'.*BTC$')
        names=re.match(pattren,x['symbol'])
        try:
            names=names.group()
        except Exception as e:
            names='None'
        if names!='None' and x['symbol']!='BTCUSD':
            if names == 'BTCABTC':
                name = names.replace('BTCABTC', 'BTCA').replace(' ','')
            else:
                name=names.replace('BTC','',1).replace(' ','')
            price=float(x['last'])*float(prices)
            price=round(price,4)
            conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',
                           charset='utf8mb4')
            cursor = conn.cursor()
            nows = datetime.datetime.now()
            now = nows.strftime('%Y-%m-%d %H:%M:%S')
            sql = "insert into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)values('" + name + "','" + exc_code + "','" + str(
                price) + "','" + str(
                USDCNY) + "','" + now + "') ON DUPLICATE KEY UPDATE create_date=VALUES(create_date),now_price=values(now_price),exchange_rate=VALUES(exchange_rate)"
            cursor.execute(sql)

            conn.commit()
    cursor.close()
    conn.close()

if __name__=='__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',port=3306)
    while True:
        try:
            get_data()
        except Exception as e:
            print(e)
            pass
