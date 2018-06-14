from selenium import  webdriver
from time import sleep
import datetime
from bs4 import BeautifulSoup
from pymysql import *
from exchange_rate import USDCNY



def get_result():
    driver = webdriver.PhantomJS()
    url = 'https://www.huobipro.com/zh-cn/'
    driver.get(url)
    price=get_BTC(driver.page_source)
    sleep(2)
    driver.find_elements_by_xpath('//*[@id="drawer"]/div[1]/div[1]/span[2]')[0].click()
    sleep(2)
    get_data(driver.page_source,price)

    driver.quit()

def get_BTC(data):
    exc_code='huobi'
    result = BeautifulSoup(data, 'html.parser')
    div = result.find('div', class_='coin_list')
    div_list = div.findAll('div', class_='coin_unit')[0]
    name=div_list.find('em',class_='base_currency').text.upper().replace(' / USDT','').replace(' ','')
    prices = div_list.find('span', price='price').text.split('≈')[0].replace(' ', '')
    prices = round(float(prices), 4)
    conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',
                   charset='utf8mb4')
    cursor = conn.cursor()
    nows = datetime.datetime.now()
    now = nows.strftime('%Y-%m-%d %H:%M:%S')
    sql = "insert into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)values('" + name + "','" + exc_code + "','" + str(
        prices) + "','" + str(
        USDCNY) + "','" + now + "') ON DUPLICATE KEY UPDATE create_date=VALUES(create_date),now_price=values(now_price),exchange_rate=VALUES(exchange_rate)"
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return prices

def get_data(data,price):
    exc_code = 'huobi'
    result=BeautifulSoup(data,'html.parser')
    div=result.find('div',class_='coin_list')
    div_list=div.findAll('div',class_='coin_unit')
    conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',
                   charset='utf8mb4')
    cursor = conn.cursor()
    for x in div_list:
        name=x.find('em',class_='base_currency').text
        name=name.upper().replace(' / BTC','').replace(' ','')
        prices=x.find('span',price='price').text.split('≈')[0].replace(' ', '')
        prices=round(float(prices)*price,4)
        nows = datetime.datetime.now()
        now = nows.strftime('%Y-%m-%d %H:%M:%S')
        sql = "insert into exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)values('" + name + "','" + exc_code + "','" + str(
            prices) + "','" + str(
            USDCNY) + "','" + now + "') ON DUPLICATE KEY UPDATE create_date=VALUES(create_date),now_price=values(now_price),exchange_rate=VALUES(exchange_rate)"
        cursor.execute(sql)
        conn.commit()
    conn.close()

if __name__ == '__main__':
    while True:
        try:
            get_result()
        except Exception as e:
            print(e)
            pass
