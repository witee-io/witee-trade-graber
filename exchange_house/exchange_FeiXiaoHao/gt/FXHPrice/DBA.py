# -*- coding: UTF-8 -*-
import pymysql.cursors

# 连接数据库
connect = pymysql.Connect(
    host='192.168.0.252',
    # host='116.62.135.114',
    port=3306,
    user='bibaogao',
    passwd='3bbibaogao2018',
    db='datacenter',
    charset='utf8'
)
# 获取游标.
cursor = connect.cursor()


def trim(str):
    return str.replace(' ', '')


# 插入数据
def insertObject(sql, *param):
    data = []
    for i in param:
        if (isinstance(i, str)):
            data.append(trim(i))
        else:
            data.append(i)
    cursor.execute(sql % tuple(data))
    connect.commit()




# 替换数据
def replaceObject(sql, *param):
    data = []
    for i in param:
        if (isinstance(i, str)):
            data.append(trim(i))
        else:
            data.append(i)
    cursor.execute(sql % tuple(data))
    connect.commit()


# 查询数据
def findObjects(sql):
    cursor.execute(sql)
    return list(cursor.fetchall())


# 删除数据
def deleteByParam(sql):
    cursor.execute(sql)
    connect.commit()


# 修改数据
def updaObject(sql, *param):
    data = []
    for i in param:
        if (isinstance(i, str)):
            data.append(trim(i))
        else:
            data.append(i)
    cursor.execute(sql % tuple(data))
    connect.commit()
