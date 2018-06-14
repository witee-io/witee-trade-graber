import requests,datetime
from lxml import etree
from pymysql import *
from exchange_rate import USDCNY
from time import sleep
#import DBA
from multiprocessing import Pool
import pymysql
from DBUtils.PooledDB import PooledDB

headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
        }
proxys = {'http': 'http://192.168.0.252:8118', 'https': 'https://192.168.0.252:8118'}

def url_1(method,name,page,n):
    if n == 1:
        url = 'https://otcbtc.com/'+method+'_offers?currency='+name+'&fiat_currency=cny&page='+page+'&payment_type=all'
        rep = requests.get(url,headers = headers,proxies=proxys)
        tree = etree.HTML(rep.text)
        ul_tree = tree.xpath('//a[@class="page-link"]/text()')
        #print(ul_tree)
        if ul_tree != []:
            page = ul_tree[-2]
            n = 2
            return url_1(method,name,page,n)
        else:
            while 1:
                try:
                    p1_1 = tree.xpath('//div[@class="recommend-card__price"]/text()')[0].replace('\n', '').replace(',', '').strip()
                    p2_1 = tree.xpath('//ul[@class="list-content"]/li/text()')[-4].replace('\n', '').replace(',', '').strip()
                    p1 = round(float(p1_1) / float(USDCNY),4)
                    p2 = round(float(p2_1) / float(USDCNY),4)
                    #print(name,method,'-',p1,'-',p2)
                    return p1, p2
                except:
                    return url_1(method, name, page, n)


    else:
        num_2 = 1
        while 1:
            if num_2 < 11:
                try:
                    url = 'https://otcbtc.com/' + method + '_offers?currency=' + name + '&fiat_currency=cny&page=' + page + '&payment_type=all'
                    rep = requests.get(url, headers=headers,proxies=proxys)
                    tree = etree.HTML(rep.text)
                    p1_1 = tree.xpath('//div[@class="recommend-card__price"]/text()')[0].replace('\n', '').replace(',', '').strip()
                    p2_1 = tree.xpath('//ul[@class="list-content"]/li/text()')[-4].replace('\n', '').replace(',', '').strip()
                    p1 = round(float(p1_1) / float(USDCNY),4)
                    p2 = round(float(p2_1) / float(USDCNY),4)
                    #print(name,method, '-', p1, '-', p2,'2ci')
                    return p1, p2
                    break

                except:
                    #print(name,'重新请求中。。。。,',num_2)
                    num_2 += 1
                    sleep(1)
                    pass
            else:
                break

def sql_1(name,page,n):

    hb, lb = url_1('buy',name,page,n)
    ls, hs = url_1('sell',name,page,n)
    exc_name = 'OTCBTC'
    nows = datetime.datetime.now()
    now = nows.strftime('%Y-%m-%d %H:%M:%S')
    # conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',
    #                charset='utf8mb4')
    # cursor = conn.cursor()
    conn = pool_1.connection()
    cursor = conn.cursor()
    sql = "insert into exc_outside_realtime(name,high_buy,low_buy,high_sell,low_sell,exc_name,exchange_rate,create_date)values('" + name + "','" + str(hb) + "','" + str(
        lb) + "','" + str(hs) + "','" + str(ls) + "','" + str(exc_name) + "','" + str(USDCNY) + "','" + now + "') ON DUPLICATE KEY UPDATE high_buy=VALUES(high_buy),low_buy=values(low_buy),high_sell=VALUES(high_sell),low_sell=values(low_sell),exchange_rate=values(exchange_rate),create_date=VALUES(create_date)"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()





def file_1():
    #创建进程池，进程数4个
    bi_list = ['BTC', 'ETH', 'VEN', 'OMG', 'EOS', 'QTUM', 'XRP', 'ZEC', 'BNB', 'SNT']
    pool=Pool(3)
    for i in bi_list:
        pool.apply_async(sql_1, args=(i,'1',1))

    print('等待所有进程执行……')
    pool.close()
    pool.join()
    print("执行完毕")
if __name__ == "__main__":
    pool_1 = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',port=3306)
    while 1:
        file_1()
        sleep(5)
