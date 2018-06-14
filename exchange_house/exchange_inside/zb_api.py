#coding=utf-8

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import datetime
from pymysql import *
from exchange_rate import USDCNY

from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def get_driver():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    # 设置user-agent请求头
    dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    dcap["phantomjs.page.settings.loadImages"] = False  # 禁止加载图片
    proxy = webdriver.Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = '127.0.0.1:8118'
    proxy.add_to_capabilities(dcap)
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.get('https://www.zb.com/')
    while True:
        try:
            driver.find_element_by_xpath('//*[@id="zbCarousel"]/div[3]/div/a[2]').click()
            sleep(2)
            prices=get_BTC(driver.page_source)

            driver.find_element_by_xpath('//*[@id="zbCarousel"]/div[3]/div/a[3]').click()
            get_data(driver.page_source,prices)
            sleep(1)
        except:
            driver.quit()
            get_driver()




def get_BTC(data):
    exc_code='zb'
    result=BeautifulSoup(data,'html.parser')
    tr=result.find('tr',class_='H_btcusdtMarket')
    name=tr.find('td').find('b').text
    price=tr.find('b',class_='price').text.replace(',','')
    price=round(float(price),4)
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
    conn.close()
    return price


def get_data(data,prices):
    exc_code = 'zb'
    result=BeautifulSoup(data,'html.parser')
    tr=result.find('table',class_='market_btc_list').findAll('tr')
    conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',
                   charset='utf8mb4')
    cursor = conn.cursor()
    for x in tr[2:]:
        try:
            name=x.find('td').find('b').text
            price=float(x.find('b',class_='price').text)
            price=round(price*prices,4)
        except:
            pass
        #print(name,price)
        nows = datetime.datetime.now()
        now = nows.strftime('%Y-%m-%d %H:%M:%S')
        sql = "insert into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)values('" + name + "','" + exc_code + "','" + str(
            price) + "','" + str(
            USDCNY) + "','" + now + "') ON DUPLICATE KEY UPDATE create_date=VALUES(create_date),now_price=values(now_price),exchange_rate=VALUES(exchange_rate)"
        cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__=='__main__':
    get_driver()
