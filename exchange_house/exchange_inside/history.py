#coding=utf-8

import pymysql
import datetime
import uuid
from pymysql import *
from multiprocessing import Pool
from DBUtils.PooledDB import PooledDB

def get_data():
    print('连接实时数据库')
    conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',
                    charset='utf8mb4')
    cursor = conn.cursor()
    #conn = pool.connection()
    #cursor = conn.cursor()

    sql="select * from exc_inside_realtime"
    cursor.execute(sql)
    return cursor.fetchall()
    cursor.close()
    conn.close()

#历史数据入库
def conn_mysql(name,exc_code,price,USDCNY,now):
    #print('将数据插入历史表')
    uids = uuid.uuid1()
    uid = str(uids).replace('-', '')
    state = 1
    # conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='exchangedata',
    #                charset='utf8mb4')
    # cursor = conn.cursor()
    conn = pool.connection()
    cursor = conn.cursor()
    nows=datetime.datetime.now()
    nows = nows.strftime('%Y%m')
    name=name.replace(' ','')
    names = name  + nows
    try:
        sql = "create table exc_inside_" + names + "(name VARCHAR(50),exc_code VARCHAR(100) DEFAULT NULL, now_price VARCHAR(100),exchange_rate float,create_date datetime DEFAULT NULL,uid VARCHAR(225),state int,CONSTRAINT pk_PersonID PRIMARY KEY (exc_code,create_date))"
        cursor.execute(sql)
        swl = "insert IGNORE into exc_inside_" + names + "(name,exc_code,now_price,exchange_rate,create_date,uid,state)values('"+name+"','"+exc_code+"','"+ str(price)+"','"+str(USDCNY)+"','"+str(now)+"','"+uid+"','"+str(state)+"')"
        print(swl)
        cursor.execute(swl)
        conn.commit()
    except Exception as e:
        swl = "insert IGNORE into exc_inside_" + names + "(name,exc_code,now_price,exchange_rate,create_date,uid,state)values('"+name+"','"+exc_code+"','"+str(price)+"','"+str(USDCNY)+"','"+str(now)+"','"+uid+"','"+str(state)+"')"
        print(swl)
        cursor.execute(swl)
        conn.commit()
    cursor.close()
    conn.close()

if __name__=='__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='hrr', passwd='gaoshiqing', db='exchangedata',port=3306)
    while True:
        try:
            data=get_data()
            pool_1 = Pool(4)
            for x in data:
                #print(x)
                pool_1.apply_async(conn_mysql, args=(x[0],x[1],x[2],x[3],x[4]))
            pool_1.close()
            pool_1.join()
        except Exception as e:
            print(e)
            pass
