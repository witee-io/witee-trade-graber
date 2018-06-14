#!/usr/bin/env python3
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
import sys
from selenium import  webdriver
sys.path.append("..")
from exchange_rate import USDCNY
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pymysql
import time
from DBUtils.PooledDB import PooledDB
createvar = locals()
def loger(l):
    log = open('coincola.log','a')
    log.write(time.strftime('%y-%m-%d %H:%M:%S',time.localtime(time.time()))+" "+l+'\n')
    log.close()
def buy_price():
    '''查询价格'''
    a = []
    soup = BeautifulSoup(driver.page_source, 'lxml')
    p1 = soup.find_all('td',class_='td-price')[0]
    b = float(re.split(' ', p1.text)[0]) / float(USDCNY)
    a.append('%.4f' % b)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'pager')))[-2].click()
    p2 = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'td-price')))[-1]
    b = float(re.split(' ', p2.text)[0]) / float(USDCNY)
    a.append('%.4f' % b)
    return a
def switch():
    '''切换币种'''
    n = ['比特币(BTC)','以太坊(ETH)','比特币现金(BCH)','莱特币(LTC)']
    n = ['BTC','ETH','BCH','LTC']
    c = {}
    for x in n:
        s = 0
        loger('switch to'+x)
        while s<=3:
            try:
                driver.find_element_by_link_text(x).click()
                break
            except:
                s+=1
                loger('switch超时'+str(s)+'次')
                sleep(1)
        else:
            driver.find_element_by_link_text(x).click()
        o = buy_price()
        y = re.search('[a-zA-Z]+',x).group()
        c[y] = o
    loger('switch_ok')
    return c
def exec():
    
    global driver
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(5)
    driver.set_script_timeout(5)
    driver.get(url)
    driver.maximize_window()
    sleep(5)
    n = 0
    while n<=10:
        conn1 = pool.connection()
        cursor1 = conn1.cursor()
        click1 = 0
        click2 = 0
        loger('begining_ask')
        ask = switch()
        while click1<=3:
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'more')))[1].click()
                break
            except:
                click1 += 1
                loger('ask_click超时'+str(click1)+'次')
        else:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'more')))[1].click()
        loger('begining_bid')
        bid = switch()
        while click2 <= 3:
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'more')))[0].click()
                break
            except:
                click2 += 1
                loger('bid_click超时'+str(click2)+'次')
        else:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'more')))[0].click()
        sql = '''replace into  exc_outside_realtime(name,exc_name,low_sell,high_sell,low_buy,high_buy,exchange_rate,create_date)VALUES(%s,%s,%s,%s,%s,%s,%s,now())'''
        sqlhis = '''insert into  exc_outside_his_btc_'''+time.strftime('%Y%m',time.localtime(time.time()))+'''(name,exc_name,low_sell,high_sell,low_buy,high_buy,exchange_rate,create_date)VALUES(%s,%s,%s,%s,%s,%s,%s,now())'''
        for e in list(ask.keys()):
            loger('sql'+e)
            for i, s in enumerate(range(1, 3)):
                createvar['a' + str(s)] = ask[e][i]
                createvar['b' + str(s)] = bid[e][i]
            cursor1.execute(sql, (e, 'coincola', a1, a2, b2, b1, USDCNY))
            #cursor1.execute(sqlhis, (e, 'coincola', a1, a2, b2, b1, USDCNY))
        conn1.commit()
        cursor1.close()
        conn1.close()
        n+=1
        loger('成功'+str(n)+'次\n\n')
    else:
        driver.quit()
if __name__ == '__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',port=3306)
    n = 1
    while 1:
        try:
            url = 'https://www.coincola.com/buy/ETH?country_code=CN'
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
            dcap["phantomjs.page.settings.loadImages"] = False
            #proxy = webdriver.Proxy()
            #proxy.proxy_type = ProxyType.MANUAL
            ## proxy.https_proxy='127.0.0.1:8118'
            #proxy.http_proxy = '127.0.0.1:8118'
            #proxy.add_to_capabilities(dcap)
            exec()
        except Exception as e:
            loger('重启'+str(n)+'次')
            n+=1
            loger(str(e))
            driver.quit()
            pass
