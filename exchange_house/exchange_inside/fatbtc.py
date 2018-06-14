#coding=utf-8

from selenium import webdriver
from bs4 import BeautifulSoup
import re,datetime
#import DBA
from time import sleep
from exchange_rate import USDCNY
from pymysql import *
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pymysql
from DBUtils.PooledDB import PooledDB


def get_driver(pool):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20")
    proxy = webdriver.Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    # proxy.https_proxy='127.0.0.1:8118'
    proxy.http_proxy = '192.168.0.252:8118'
    proxy.add_to_capabilities(dcap)
    driver = webdriver.PhantomJS(desired_capabilities=dcap)

    #driver = webdriver.PhantomJS()
    url='https://www.fatbtc.com/'

    driver.get(url)
    sleep(2)

    while True:
        try:
            get_data(driver.page_source,pool)
            sleep(3)
        except Exception as e:
            driver.quit()
            sleep(1)
            get_driver(pool)

def get_data(data,pool):
    exc_code = 'fatbtc'
    bsObj=BeautifulSoup(data,'html.parser')
    div=bsObj.find('div',class_='first-box')
    tbody=div.find('tbody',class_='work-list')
    tr=tbody.find_all('tr')
    # conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',
    #                charset='utf8mb4')
    # cursor = conn.cursor()
    conn = pool.connection()
    cursor = conn.cursor()
    for x in tr:
        name_td = x.find_all('td')[0].text
        if 'FCNY' in name_td:
            name=name_td.replace('/FCNY','').replace(' ','')
            prices=x.find_all('td')[1].text
            price=round(float(prices)/float(USDCNY),4)
            print(price)
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
    get_driver(pool)
