#coding=utf-8

import json,re
#import DBA
import time,datetime
import requests
from exchange_rate import USDCNY
from pymysql import *
import pymysql
from DBUtils.PooledDB import PooledDB


def get_data(pool):
    exc_code = 'bittrex'
    proxys={'http': 'http://192.168.0.252:8118', 'https': 'https://192.168.0.252:8118'}

    url='https://bittrex.com/api/v2.0/pub/Markets/GetMarketSummaries'
    response=requests.get(url,proxies=proxys,timeout=5)
    #response = requests.get(url,timeout=5)
    result=json.loads(response.text)
    for x in result['result']:
        pattern_1 = re.compile(r'USDT-BTC')
        names = re.search(pattern_1, x['Summary']['MarketName'])
        try:
            name_USDT = names.group()
        except Exception as e:
            name_USDT = 'None'
        if name_USDT != 'None':
            prices = x['Summary']['Last']
            name=x['Market']['MarketCurrency'].replace(' ','')
            prices=round(prices,4)
            # conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',
            #                charset='utf8mb4')
            # cursor = conn.cursor()
            conn = pool.connection()
            cursor = conn.cursor()
            nows = datetime.datetime.now()
            now = nows.strftime('%Y-%m-%d %H:%M:%S')
            sql = "insert into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)values('" + name + "','" + exc_code + "','" + str(
                prices) + "','" + str(
                USDCNY) + "','" + now + "') ON DUPLICATE KEY UPDATE create_date=VALUES(create_date),now_price=values(now_price),exchange_rate=VALUES(exchange_rate)"
            cursor.execute(sql)

    conn.commit()
    cursor.close()
    conn.close()
    conn = pool.connection()
    cursor = conn.cursor()
    for x in result['result']:
        pattern=re.compile(r'BTC.*')
        name_BTC=re.match(pattern,x['Summary']['MarketName'])
        try:
            name_BTC=name_BTC.group()
        except Exception as e:
            name_BTC='None'
        if name_BTC!='None':
            price=float(x['Summary']['Last'])*float(prices)
            price=round(price,4)
            name=x['Market']['MarketCurrency']
            # conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',
            #                charset='utf8mb4')
            # cursor = conn.cursor()
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
            get_data(pool)
        except Exception as e:
            time.sleep(2)
            print(e)
