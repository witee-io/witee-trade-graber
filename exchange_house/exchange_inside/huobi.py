#coding=utf-8

import requests
import json,datetime
from exchange_rate import USDCNY
from pymysql import *
from time import sleep
from multiprocessing import Pool
import pymysql,time
import logging
from DBUtils.PooledDB import PooledDB



logger = logging.getLogger("simple_example")
logger.setLevel(logging.DEBUG)

exc_code='huobi'
def get_symbol():
    proxys = {'http': 'http://192.168.0.252:8118', 'https': 'https://192.168.0.252:8118'}
    url='https://api.huobi.pro/v1/common/symbols'
    response=requests.get(url,proxies=proxys)
    result=json.loads(response.text)
    symbol = []
    symbol_BTC=[]
    for x in result['data']:
        base_currency=x['base-currency']
        quote_currency=x['quote-currency']

        if base_currency=='btc'and quote_currency=='usdt':
            symbol_BTC.append(base_currency+quote_currency)
        if quote_currency=='btc':
            symbol.append(base_currency+quote_currency)
        #print(symbol,symbol_BTC)
    return symbol,symbol_BTC
    #while True:
        #try:
            #get_BTC(symbol,symbol_BTC)
            #sleep(1)
        #except Exception as e:
            #pass


def get_BTC(symbol_BTC,usdcny):
    #exc_code='huobi'
    proxys = {'http': 'http://192.168.0.252:8118', 'https': 'https://192.168.0.252:8118'}
    url='https://api.huobi.pro/market/detail/merged?symbol='+symbol_BTC[0]
    conn = pools.connection()
    cursor = conn.cursor()
    try:
        response=requests.get(url,proxies=proxys, timeout = 10, verify=False)
        print('btc行情获取成功！')
    except Exception as e:
        print(e) 
    else:
        result=json.loads(response.text)
        name=symbol_BTC[0].replace('usdt','')
        name=name.upper()
        prices=result['tick']['close']
        prices=round(float(prices),4)
        nows = datetime.datetime.now()
        now = nows.strftime('%Y-%m-%d %H:%M:%S')
        sql = "insert into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)values('" + name + "','" + exc_code + "','" + str(
        prices) + "','" + usdcny + "','" + now + "') ON DUPLICATE KEY UPDATE create_date=VALUES(create_date),now_price=values(now_price),exchange_rate=VALUES(exchange_rate)"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return prices
def get_data(x,prices,try_1,usdcny, pro_num):
    proxys = [{'http': 'http://192.168.0.252:8118', 'https': 'https://192.168.0.252:8118'},
            {'http': 'http://127.0.0.1:8118', 'https': 'https://127.0.0.1:8118'},
            {'http': 'http://192.168.0.232:8118', 'https': 'https://192.168.0.232:8118'}]
    conn = pools.connection()
    cursor = conn.cursor()
    try:
        url='https://api.huobi.pro/market/detail/merged?symbol='+x
        response=requests.get(url,proxies = proxys[pro_num], verify = False)
        result=json.loads(response.text)
    except:
        if try_1 == 11:
            pass
        else:
            print('请求失败,重新请求'+try_1+'/10。')
            try_1 += 1
            pro_num += 1 
            if pro_num == 3:
                pro_num = 0
            get_data(x,prices,try_1, pro_num)
    else:
        if result['status']=='ok':
            name = x.replace('btc', '', 1)
            name = name.upper()
            price=result['tick']['close']
            price=float(price)*prices
            price=round(price,4)
            nows = datetime.datetime.now()
            now = nows.strftime('%Y-%m-%d %H:%M:%S')
            try:
                sql = "insert into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)values('" + name + "','" + exc_code + "','" + str(
                price) + "','" + usdcny + "','" + now + "') ON DUPLICATE KEY UPDATE create_date=VALUES(create_date),now_price=values(now_price),exchange_rate=VALUES(exchange_rate)"
                cursor.execute(sql)
                print(name+'写入成功！')
                #print(name)
                conn.commit()
            except:
                print(name+'数据库写入失败')
            else:
                conn.close()
def main():
    while 1:
        try:
            usdcny = str(USDCNY)
            print('汇率获取成功！')
            break
        except:
            print('汇率获取失败，重新获取中')
            sleep(1)
    prices = get_BTC(symbol_BTC,usdcny)
    pool = Pool(processes = 3)
    print('进程开始')
    pro_num = 0
    for x in symbol:
        if pro_num == 3:
            pro_num = 0
        pool.apply_async(get_data, args=(x, prices,1,usdcny, pro_num))
        pro_num += 1
    pool.close()
    pool.join()
    print('执行完毕')



if __name__=='__main__':
    pools = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',port=3306)
    symbol,symbol_BTC=get_symbol()
    while True:
        try:
            main()
            sleep(10)
        except:
            pass
