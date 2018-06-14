#coding=utf-8

import requests
import json
import time
import math
import pymysql
from exchange_rate import USDCNY
from DBUtils.PooledDB import PooledDB
from forex_python.converter import CurrencyRates

'''拼接请求，拿到不同币种的数据'''
proxys = {'http': 'http://192.168.0.232:8118', 'https': 'https://192.168.0.232:8118'}
def get_text(bi_name):
    '''美元和韩元进行转换'''
    c = CurrencyRates()
    USDCNY1 = c.get_rates('aud')['USD']
    exc_code = 'btcmarkets'
    time_stamp = math.floor(time.time())
    url = 'https://btcmarkets.net/data/market/BTCMarkets/'+ bi_name + '/AUD/tick?_=' + str(time_stamp)
    headers ={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    response = requests.get(url, headers=headers, proxies = proxys)
    '''返回数据转换为字典'''
    result = json.loads(response.text)
    name = result['instrument'] # 币种名称
    price = round(result['lastPrice']/100000000*USDCNY1,4) # 最后价格
    data = (name, exc_code, str(price), str(USDCNY))
    print(data)
    return data

'''数据存入数据库'''
def sava_database(datas):
    conn = pool.connection()
    cursor = conn.cursor()
    sql = "insert into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date) values (%s, %s, %s, %s, now()) ON DUPLICATE KEY UPDATE create_date=VALUES(create_date),now_price=values(now_price),exchange_rate=VALUES(exchange_rate)"
    cursor.executemany(sql, datas)
    print('更新成功')
    conn.commit()
    cursor.close()
    conn.close()


if __name__=='__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter', port=3306)
    '''获取不同币种的价格'''
    Markets = ['BTC', 'LTC', 'ETH', 'ETC', 'XRP', 'BCH']
    datas = []
    while True:
        for x in Markets:
            try:
                data = get_text(x)
                datas.append(data)
            except:
                pass
        sava_database(datas)