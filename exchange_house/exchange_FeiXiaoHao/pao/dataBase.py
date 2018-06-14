import pymysql.cursors
# 连接数据库
connect = pymysql.Connect(
    # host='localhost',
    host='116.62.135.114',
    port=3306,
    user='root',
    passwd='root',
    db='test',
    charset='utf8'
)
# 获取游标
cursor = connect.cursor()
# def __inser__(name,age):
#     sql = "INSERT INTO employe (name,age) VALUES ('%s',%2.f)"
#     data = (name, age)
#     cursor.execute(sql % data)
#     connect.commit()
#     print('成功插入', cursor.rowcount, '条数据')

#保存数据
def _insertObject_(*parma):
    #for list in parma:
        #print(list)
    sql="INSERT INTO fxhprice (rank,symbol,marketcapcny,pricecny,totalsupply,flow,hvolumecny,percentchange1h,percentchange24h,percentchange7d) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
    data=(parma[0],parma[1],parma[2].upper(),parma[3],parma[4],parma[5],parma[6],parma[7],parma[8],parma[9])
    cursor.execute(sql % data)
    connect.commit()
    # print("成功插入",cursor.rowcount,'条数据')


#替换数据#######################
def _replaceObject_(*parma):
    #for list in parma:
        #print(list)
    sql="REPLACE INTO fxhprice (rank,symbol,marketcapcny,pricecny,totalsupply,flow,hvolumecny,percentchange1h,percentchange24h,percentchange7d) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
    data=(parma[0],parma[1],parma[2].upper(),parma[3],parma[4],parma[5],parma[6],parma[7],parma[8],parma[9])
    cursor.execute(sql % data)
    # cursor.executemany(sql % data)
    connect.commit()
    # print("成功插入",cursor.rowcount,'条数据')

#查询数据
def _findBySymbol_(*parma):
    sql="SELECT * FROM fxhprice where symbol = '%s'"
    data=parma[0]
    data.upper()
    cursor.execute(sql % data)
    for row in cursor.fetchall():
        print(row)
    print('共查找出', cursor.rowcount, '条数据')
#删除数据
def _deleteBySymbol_(*parma):
    sql = "DELETE FROM fxhprice where symbol = '%s'"
    data = parma[0]
    data.upper()
    cursor.execute(sql % data)
    connect.commit()
    print('成功删除', cursor.rowcount, '条数据')
