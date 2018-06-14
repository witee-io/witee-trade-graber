import requests
import re
import time
import pymysql
from forex_python.converter import CurrencyRates
def req1():
    usdlist = {}
    req = requests.get(url,proxies={'http':'http://127.0.0.1:8118','https':'http://127.0.0.1:8118'},headers=head)
    #req = requests.get(url,headers=head)
    for i in req.json()['data']:
        b = re.split('_',i['symbol'])
        if (b[0].upper() not in list(usdlist.keys())) and (b[1] == 'usdt'):
            usdlist[b[0].upper()] = round(float(i['close']),4)
    for x in req.json()['data']:
        y = re.split('_',x['symbol'])
        if y[0].upper() not in list(usdlist.keys()):
            usdlist[y[0].upper()] = round(float(usdlist[y[1].upper()])*float(x['close']),4)
    return usdlist
def conn_mysql(names,exc_code,price,state):
    import uuid
    import datetime
    conn = pymysql.connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',charset='utf8mb4')
    cursor = conn.cursor()
    nows=datetime.datetime.now()
    now=nows.strftime('%Y-%m-%d %H:%M:%S')
    nows = nows.strftime('%Y%m')
    name = names + "_" + nows
    uid = str(uuid.uuid1()).replace('-','')
    try:
        sql = "create table exc_inside_" + name + "(name VARCHAR(50),exc_code VARCHAR(100), now_price VARCHAR(100),exchange_rate float,create_date datetime,uid VARCHAR(225),state int)"
        cursor.execute(sql)
        swl = "insert into exc_inside_" + name + "(name,exc_code,now_price,exchange_rate,create_date,uid,state)values('"+names+"','"+exc_code+"','"+ str(price)+"','"+str(USDCNY)+"','"+now+"','"+uid+"','"+str(state)+"')"
        cursor.execute(swl)
    except Exception as e:
        swl = "insert into exc_inside_" + name + "(name,exc_code,now_price,exchange_rate,create_date,uid,state)values('"+names+"','"+exc_code+"','"+str(price)+"','"+str(USDCNY)+"','"+now+"','"+uid+"','"+str(state)+"')"
        cursor.execute(swl)
    conn.commit()
    conn.close()
def sqlr(s):
    for i in s.keys():
        conn_mysql(i,'okex',s[i],1)

if __name__ == '__main__':
    USDCNY = CurrencyRates().get_rates('usd')['CNY']
    url = 'https://www.okex.com/v2/markets/tickers'
    head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    while 1:
        try:
            sqlr(req1())
            time.sleep(10)
            print('over')
        except Exception as e:
            print(e)
