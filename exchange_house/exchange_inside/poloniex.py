#coding=utf-8

import requests
import json,time
import re,datetime
#import DBA
from exchange_rate import USDCNY
from pymysql import *
import pymysql
from DBUtils.PooledDB import PooledDB

def get_data():
    exc_code = 'poloniex'
    proxys = {'http': 'http://192.168.0.252:8118', 'https': 'https://192.168.0.252:8118'}
    url='http://poloniex.com/public?command=returnTicker'
    response=requests.get(url,proxies=proxys,timeout=5)
    result=json.loads(response.text)
    conn = pool.connection()
    cursor = conn.cursor()
    for x in result:
        pattern=re.compile(r'USDT_BTC')
        names=re.match(pattern,x)
        try:
            names=names.group()
        except Exception as e:
            names='None'
        if names!='None':
            name=names.replace('USDT_','')
            prices=result[x]['last'].replace(',','')
            prices=round(float(prices), 4)
            # conn = connect(host='192.168.0.252', port=3306, user='root',passwd='3bgaoshiqing',db='datacenter',charset='utf8mb4')
            # cursor = conn.cursor()
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
    for x in result:
        pattern=re.compile(r'BTC_.*')
        names=re.match(pattern,x)
        try:
            names=names.group()
        except Exception as e:
            names='None'
        if names!='None':
            name=names.replace('BTC_','')
            price=float(result[x]['last'])*float(prices)
            price=round(price, 4)
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
            time.sleep(2)
            pass

