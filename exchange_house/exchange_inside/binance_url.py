#coding=utf-8

import requests
import json
import re,datetime
from pymysql import *
from exchange_rate import USDCNY
from time import sleep
import pymysql
from DBUtils.PooledDB import PooledDB




def get_data(pool):
    exc_code='binance'
    proxys = {'http': 'http://192.168.0.252:8118', 'https': 'https://192.168.0.252:8118'}
    url='https://www.binance.com/exchange/public/product'
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'referer':'https://www.binance.com/',
    }
    response=requests.get(url=url,headers=headers,proxies=proxys,timeout=5)
    # response = requests.get(url=url, headers=headers)
    result=json.loads(response.text)
    conn = pool.connection()
    cursor = conn.cursor()
    for i in result['data']:
        pattern1=re.compile(r'BTCUSDT')
        name=re.findall(pattern1,i['symbol'])
        if name!=[]:
            name=i['baseAsset'].replace(' ','')
            price=float(i['close'])
            prices=round(price,4)
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

    # conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',
    #                charset='utf8mb4')
    # cursor = conn.cursor()
    conn = pool.connection()
    cursor = conn.cursor()
    for x in result['data']:
        pattern=re.compile(r'.*BTC$')
        names=re.match(pattern,x['symbol'])
        try:
            name=names.group()
        except:
            name='None'

        if name!='None':
            name=x['baseAsset'].replace(' ','')
            price=float(x['close'])*prices
            price=round(price,4)
            nows = datetime.datetime.now()
            now = nows.strftime('%Y-%m-%d %H:%M:%S')
            sql = "insert into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)values('" + name + "','" + exc_code + "','" + str(
                price) + "','" + str(
                USDCNY) + "','" + now + "') ON DUPLICATE KEY UPDATE create_date=VALUES(create_date),now_price=values(now_price),exchange_rate=VALUES(exchange_rate)"
            cursor.execute(sql)
            print(name, price)
    conn.commit()
    cursor.close()
    conn.close()


if __name__=='__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',port=3306)
    while True:
        try:
            get_data(pool)
            sleep(3)
        except Exception as e:
            print(e)
            pass
