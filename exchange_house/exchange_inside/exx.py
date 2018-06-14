#coding=utf-8


from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import re,datetime
#import DBA
from exchange_rate import USDCNY
from pymysql import *

def get_driver():
    url='https://www.exx.com/'
    driver=webdriver.PhantomJS()
    driver.get(url)
    while True:
        try:
            sleep(2)
            driver.find_element_by_xpath('//*[@id="home-market"]/div/div/div/ul/li[4]').click()
            get_data(driver.page_source)
            driver.find_element_by_xpath('//*[@id="home-market"]/div/div/div/ul/li[3]').click()
            BTC_data(driver.page_source)
            sleep(3)
        except Exception as e:
            print(e)
            driver.quit()
            get_driver()

def get_data(data):
    exc_code = 'Exx'
    bsObj=BeautifulSoup(data,'html.parser')
    ul=bsObj.find('ul',class_='market-list')
    li=ul.findAll('li')
    for x in li:
        name=x.find('em').text
        price=x.findAll('div',class_='item')[3].text.replace('$','')
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
        # sql = "REPLACE INTO exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date) VALUES ('%s','%s','%s','%s',now())"
        # DBA.replaceObject(sql, name, exc_code, price, USDCNY)

def BTC_data(data):
    exc_code = 'Exx'
    bsObj = BeautifulSoup(data, 'html.parser')
    ul = bsObj.find('ul', class_='market-list')
    li = ul.findAll('li')
    for x in li:
        names = x.find('em').text
        pattern=re.compile(r'BTC')
        name=re.match(pattern,names)
        try:
            name=name.group()
        except Exception as e:
            name='None'
        if name!='None':
            price = x.findAll('div', class_='item')[3].text.replace('$', '')
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
            # sql = "REPLACE INTO exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date) VALUES ('%s','%s','%s','%s',now())"
            # DBA.replaceObject(sql, name, exc_code, price, USDCNY)


if __name__=='__main__':
    get_driver()
