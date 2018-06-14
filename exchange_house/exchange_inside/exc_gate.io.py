from selenium import  webdriver
from time import sleep
from exchange_rate import USDCNY
from bs4 import BeautifulSoup
import pymysql
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pymysql
from DBUtils.PooledDB import PooledDB


def start():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20")
    proxy = webdriver.Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    # proxy.https_proxy='127.0.0.1:8118'
    proxy.http_proxy = '192.168.0.232:8118'
    proxy.add_to_capabilities(dcap)
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    #driver = webdriver.PhantomJS()
    url = 'https://gate.io/trade/BTC_USDT'
    driver.get(url)
    driver.maximize_window()

    num = 0
    while 1:
        if num < 1350:
            # conn = pymysql.connect(host='192.168.0.252',port=3306, user='root',passwd='3bgaoshiqing',db='datacenter',charset='utf8mb4')
            # cursor = conn.cursor()
            soup = BeautifulSoup(driver.page_source, 'lxml')
            tbody = soup.find('tbody', id='usdtTbody')
            all_tr = tbody.find_all('tr')
            conn = pool.connection()
            cursor = conn.cursor()
            for i in all_tr:
                name = i.find('span',class_='bizhong_en').text.replace('\n', '').strip()
                price = i.find('span',class_='left-price').text.replace('\n', '').strip()
                exc_code = 'gate.io'
                sql = '''REPLACE INTO exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date) VALUES(%s,%s,%s,%s,now())'''
                #print(name, exc_code, price, USDCNY)
                cursor.execute(sql,(name,exc_code,price,USDCNY))
                print(name)
                conn.commit()
            cursor.close()
            conn.close()
            num += 1
            sleep(5)
        else:
            driver.quit()
            break

if __name__ == '__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',
                    port=3306)
    while 1:
        try:
            start()
            
        except Exception as e:
            print(e)
            pass
