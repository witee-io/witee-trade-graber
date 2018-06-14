#coding=utf-8

from selenium import webdriver
from bs4 import BeautifulSoup
import time,datetime
from exchange_rate import USDCNY
from pymysql import *
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import pymysql
from DBUtils.PooledDB import PooledDB
from time import sleep

def get_response():
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap["phantomjs.page.settings.userAgent"] = (
    #     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    # dcap["phantomjs.page.settings.loadImages"] = False
    driver = webdriver.PhantomJS()
    driver.set_page_load_timeout(30)
    try:
        driver.get('https://www.bithumb.com')
    except:
        pass
    finally: 
        while True:
            try:
                get_data(driver.page_source)
                sleep(5)
            except Exception as e:
                driver.quit()
                print(e)
                time.sleep(1)
                get_response()

def get_data(data):
    exc_code = 'bithumb'
    bsObj=BeautifulSoup(data,'html.parser')
    tbody=bsObj.find('tbody')
    tr=tbody.findAll('tr')
    conn = pool.connection()
    cursor = conn.cursor()
    for x in tr:
        try:
            name = x.find('td', class_='left_l').text
            print(name)
        except:
            pass
        else:
            #names=x.get('title').replace(' Please click to see information','').replace('(','').replace(')','').replace(name,'')
            names = x.get('title').replace(' 请点击就可查看信息', '').replace('(', '').replace(')', '').replace(name, '')
            prices = x.findAll('td')[2].find('strong').text.replace('￥ ', '').replace(',', '')
            price = float(prices) / float(USDCNY)
            #prices = x.findAll('td')[2].find('strong').text.replace('$ ', '').replace(',', '')
            #price = float(prices)
            price = round(price, 4)
            nows = datetime.datetime.now()
            now = nows.strftime('%Y-%m-%d %H:%M:%S')
            sql = "insert into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)values('" + names + "','" + exc_code + "','" + str(price) + "','" + str(USDCNY) + "','" + now + "') ON DUPLICATE KEY UPDATE create_date=VALUES(create_date),now_price=values(now_price),exchange_rate=VALUES(exchange_rate)"
            cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


if __name__=='__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',port=3306)
    get_response()
