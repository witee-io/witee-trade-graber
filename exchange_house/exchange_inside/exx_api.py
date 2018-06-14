#coding=utf-8

import requests
import json
import re,datetime
from pymysql import *
from exchange_rate import USDCNY
from time import sleep
import pymysql
from DBUtils.PooledDB import PooledDB


def get_data():
    #proxys = {'http':'http://192.168.0.252:8118','https':'http://192.168.0.252:8118'}
    exc_code='exx'
    url='https://api.exx.com/data/v1/tickers'
    head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    response = requests.get(url,proxies={'http':'http://192.168.0.252:8118','https':'http://192.168.0.252:8118'},headers=head,timeout=10, verify = False)
    #response=requests.get(url,proxies=proxys,timeout=10)
    #response=requests.get(url)
    result=json.loads(response.text)
    print(result)
    # conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',
    #                charset='utf8mb4')
    # cursor = conn.cursor()
    conn = pool.connection()
    cursor = conn.cursor()
    for x in result:
        print(x)
        pattren=re.compile(r'btc_usdt')
        name_btc=re.match(pattren,x)
        try:
            name_btc=name_btc.group()
        except Exception as e:
            name_btc='None'
        if name_btc!='None':
            name='BTC'
            prices=result[name_btc]['last'].replace(',','')
            prices=round(float(prices),4)
            nows = datetime.datetime.now()
            now = nows.strftime('%Y-%m-%d %H:%M:%S')
            sql = "insert into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)values('" + name + "','" + exc_code + "','" + str(
                prices) + "','" + str(
                USDCNY) + "','" + now + "') ON DUPLICATE KEY UPDATE create_date=VALUES(create_date),now_price=values(now_price),exchange_rate=VALUES(exchange_rate)"
            cursor.execute(sql)
            conn.commit()
    cursor.close()
    conn.close()
            #print(name, prices)
    conn = pool.connection()
    cursor = conn.cursor()
    for x in result:
        pattren=re.compile(r'.*_btc')
        names=re.match(pattren,x)
        try:
            names=names.group()
        except Exception as e:
            names='None'
        if names!='None':
            name=names.replace(' ','').replace('_btc','')
            name=name.upper()
            price=result[names]['last']
            price=float(price)*prices
            price=round(price,4)
            nows = datetime.datetime.now()
            now = nows.strftime('%Y-%m-%d %H:%M:%S')
            sql = "insert into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)values('" + name + "','" + exc_code + "','" + str(
                price) + "','" + str(
                USDCNY) + "','" + now + "') ON DUPLICATE KEY UPDATE create_date=VALUES(create_date),now_price=values(now_price),exchange_rate=VALUES(exchange_rate)"
            cursor.execute(sql)
            print(name)

            conn.commit()
    cursor.close()
    conn.close()

if __name__=='__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',port=3306)
    while True:
        try:
            get_data()
            sleep(1)
        except Exception as e:
            print(e)
            pass

