import requests
from bs4 import BeautifulSoup
import pymysql
import re, sys
import time
sys.path.append("..")
from exchange_rate import USDCNY
from DBUtils.PooledDB import PooledDB
url = 'https://www.bitfinex.com/stats'
head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
def sqlr(s):
    sql1 = '''replace into  exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)VALUES(%s,%s,%s,%s,now())'''
    for i in s.keys():
        cursor1.execute(sql1, (i,'bitfinex',s[i],USDCNY ))
    conn1.commit()
    conn1.close()
def req1():
    s = {}
    req = requests.get(url,proxies={'http':'http:/192.168.0.252/:8118','https':'http://192.168.0.252:8118'},headers=head,timeout=10)
    soup = BeautifulSoup(req.text, 'lxml')
    table1 = soup.find('table', class_='compact striped')
    tr1 = table1.find_all('tr')
    for i in tr1:
        if i.find('td', class_='col-info') != None:
            price = i.find('td',class_='col-currency').text
            symbol = re.split('/',i.find('td',class_='col-info').text)
            if symbol[1] == 'USD':
                symbol = symbol[0]
                s[symbol] = round(float(price),6)
    print(s)
    return s
if __name__ == '__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',port=3306)
    while 1:
        conn1 = pool.connection()
        cursor1 = conn1.cursor()
        try:
            req = req1()
            sqlr(req)
            print('over')
            time.sleep(10)
        except Exception as e:
            print(e)
            pass
