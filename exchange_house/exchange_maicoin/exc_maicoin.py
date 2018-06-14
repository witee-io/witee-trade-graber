from selenium import  webdriver
from bs4 import BeautifulSoup
import re
import requests
import pymysql
from DBUtils.PooledDB import PooledDB
import datetime
from time import sleep


def get_data():
    url = 'https://www.maicoin.com/zh-TW?currency=usd'
    driver = webdriver.PhantomJS()
    driver.get(url)
    driver.maximize_window()
    exchange_rate = get_rate()
    num = 0
    while True:
        if num == 920:
            driver.quit()
            break
        else:
            soup = BeautifulSoup(driver.page_source,'html.parser')
            all_span_w = soup.find_all('span', class_ = 'crypto')
            try:
                my_sql(all_span_w,exchange_rate)
                sleep(4)
                num += 1
            except:
                num += 1


def my_sql(data,exchange_rate):
    exc_code = 'maicoin'
    conn = pools.connection()
    cursor = conn.cursor()
    for i in data:
        name = i.find_all('span')[0].text.replace('\n', '').strip().replace(':', '')
        prices = i.find_all('span')[1].text.replace('\n', '').strip().replace('$', '').replace(',', '')
        nows = datetime.datetime.now()
        now = nows.strftime('%Y-%m-%d %H:%M:%S')
        sql = "insert into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)values('" + name + "','" + exc_code + "','" + str(prices) + "','" + exchange_rate + "','" + now + "') ON DUPLICATE KEY UPDATE create_date=VALUES(create_date),now_price=values(now_price),exchange_rate=VALUES(exchange_rate)"
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()


def get_rate():
    url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query=1%E7%BE%8E%E5%85%83%E7%AD%89%E4%BA%8E%E5%A4%9A%E5%B0%91%E6%96%B0%E5%8F%B0%E5%B8%81&co=&resource_id=6017&cardId=6017&ie=utf8&oe=gbk&cb=op_aladdin_callback&format=json&tn=baidu&cb=jQuery110209102089538147091_1526454514071&_=1526454514080'
    while 1:
        try:
            req = requests.get(url=url)
        except:
            print('汇率获取失败！')
            pass
        else:
            text = req.text
            re_1 = re.search('1美元=(.*?)新台币', text)
            exchange_rate = re_1.group(1)
            return exchange_rate


if __name__ == '__main__':
    pools = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',
                     port=3306)
    while 1:
        try:
            get_data()
        except:
            sleep(3)

