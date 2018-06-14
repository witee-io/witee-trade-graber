#coding=utf-8

import requests
import json,datetime
from pymysql import *
from time import sleep
import pymysql
from DBUtils.PooledDB import PooledDB
from exchange_rate import USDKRW
def get_data(pool):
    proxys = {'http': 'http://192.168.0.232:8118', 'https': 'https://192.168.0.232:8118'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    exc_code='coinone'
    url='https://api.coinone.co.kr/ticker/?currency=all&format=json'
    response=requests.get(url, proxies=proxys, headers=headers)
    result=json.loads(response.text)
    conn = pool.connection()
    cursor = conn.cursor()
    for x in result:
        try:
            name=result[x]['currency']
        except Exception as e:
            name='None'
        if name!='None':
            USDKRW_1 = USDKRW.replace(',','')
            name = name.upper()
            prices=result[x]['last']
            price=float(prices)/float(USDKRW_1)
            price=round(price,4)
            conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',
                           charset='utf8mb4')
            cursor = conn.cursor()
            nows = datetime.datetime.now()
            now = nows.strftime('%Y-%m-%d %H:%M:%S')
            sql = "insert into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)values('" + name + "','" + exc_code + "','" + str(
                price) + "','" + str(
                USDKRW_1) + "','" + now + "') ON DUPLICATE KEY UPDATE create_date=VALUES(create_date),now_price=values(now_price),exchange_rate=VALUES(exchange_rate)"
            cursor.execute(sql)
            conn.commit()
    cursor.close()
    conn.close()

if __name__=='__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',port=3306)
    while True:
        try:
            get_data(pool)
            sleep(2)
        except Exception as e:
            print(e)
            pass

