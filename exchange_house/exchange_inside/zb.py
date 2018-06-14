#coding=utf-8

import requests
import json,datetime
from pymysql import *
from exchange_rate import USDCNY
from time import sleep
import pymysql
from DBUtils.PooledDB import PooledDB

def get_data(pool):
    proxys = {'http': 'http://192.168.0.252:8118', 'https': 'https://192.168.0.252:8118'}
    exc_code='zb'
    url='http://api.zb.com/data/v1/ticker?market=btc_usdt'
    req=requests.get(url,proxies=proxys)
    resu=json.loads(req.text)
    #print(resu)
    price_btc=resu['ticker']['last'].replace(',','')
    price_btc=float(price_btc)
    price_btc = round(price_btc, 4)
    list_data=['zb_btc','btc_usdt','bcc_btc','ubtc_btc','ltc_btc','eth_btc','etc_btc','bts_btc','eos_btc','qtum_btc'
    ,'hsr_btc','xrp_btc','bcd_btc','dash_btc','sbtc_btc','ink_btc','tv_btc','bcx_btc','bth_btc','lbtc_btc','chat_btc',
    'hlc_btc','bcw_btc','btp_btc','topc_btc','ent_btc','bat_btc','1st_btc','safe_btc','qun_btc','btn_btc','true_btc',
    'cdc_btc','ddm_btc','bite_btc','hotc_btc','xuc_btc','epc_btc','bds_btc','gram_btc']
    conn = pool.connection()
    cursor = conn.cursor()
    for x in list_data:
        url='http://api.zb.com/data/v1/ticker?market='+x
        response=requests.get(url,proxies=proxys)
        result=json.loads(response.text)
        print(result)
        if x=='btc_usdt':
            name='BTC'
            price=price_btc
        else:
            name=x.replace('_btc','')
            name=name.upper()
            prices=result['ticker']['last'].replace(',','')
            price=float(prices)*price_btc
            price=round(price,4)
        # conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',charset='utf8mb4')
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
            sleep(2)
        except Exception as e:
            pass

