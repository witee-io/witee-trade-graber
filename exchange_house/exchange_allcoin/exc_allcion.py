# coding : utf-8
'''

黄飞

2018/4/25 16:11

'''
import requests
from decimal import Decimal
from decimal import getcontext
#from forex_python.converter import CurrencyRates
from exchange_rate import USDCNY
from DBUtils.PooledDB import PooledDB
import pymysql
from time import sleep
#  将获取到的数据存入数据库
def my_sql(dic):
    conn = pool.connection()
    cursor1 = conn.cursor()
    for i in dic:
        sql = '''replace into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)VALUES(%s,%s,%s,%s,now())'''
        cursor1.execute(sql, (i.upper(), 'allcoin', dic[i], USDCNY))
        conn.commit()
        print(i, dic[i])
    conn.close()
    sleep(5)



#  获取每个交易区的价格
def my_json(rep):
    getcontext().prec = 4  # 设置精度
    list = []
    price_dic = {}
    rep = rep.json()
    '''
    优先将ckusd交易区的所有交易详情拿出来，并将币种存在空列表list中，
    当别的交易区币种不在list中时，计算出当前币种价格存储
    '''
    print(rep)
    ckusd_list = rep['ckusd']
    for i in ckusd_list:
        name = i['coin_from']
        price = i['current']
        price_dic[name] = price
        list.append(name)
    btc_list = rep['btc']
    for i in btc_list:
        if i['coin_from'] not in list:
            name = i['coin_from']
            list.append(name)
            price = i['current']
            price = Decimal(price) * Decimal(price_dic['btc'])
            price = round(float(price), 4)
            price_dic[name] = price
        else:
            pass
    eth_list = rep['eth']
    for i in eth_list:
        if i['coin_from'] not in list:
            name = i['coin_from']
            list.append(name)
            price = i['current']
            price = Decimal(price) * Decimal(price_dic['eth'])
            price = round(float(price), 4)
            price_dic[name] = price
        else:
            pass
    qtum_list = rep['qtum']
    for i in qtum_list:
        if i['coin_from'] not in list:
            name = i['coin_from']
            price = i['current']
            price = Decimal(price) * Decimal(price_dic['qtum'])
            price = round(float(price), 4)
            price_dic[name] = price
        else:
            pass
    my_sql(price_dic)


def my_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    proxys = {'http': 'http://192.168.0.232:8118', 'https': 'https://192.168.0.232:8118'}
    rep = requests.get(url = url, headers = headers, proxies = proxys, verify = False)
    return rep



def rate():
    while True:
        try:
            USDCNY = CurrencyRates().get_rates('usd')['CNY']
            print('汇率获取成功')
            return USDCNY
        except:
            print('汇率获取失败')


def main():
    url = 'https://www.allcoin.ca/Api_Market/getPriceList'
    rep = my_request(url)
    my_json(rep)


if __name__ == '__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',port=3306)
    while True:
        try:
            #USDCNY = rate()
            main()
        except:
            pass
