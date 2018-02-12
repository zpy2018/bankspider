import mysql.connector


MYSQL_HOSTS = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123'
MYSQL_PORT = '3306'
MYSQL_DB = 'work'

cnn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
cur = cnn.cursor(buffered=True)


def select(city, pagenum):
    sql = 'select * from bulletin where num like %(city)s;'
    value = {
        'city': city + '%'
    }
    cur.execute(sql, value)
    res = cur.fetchall()
    #res.sort(key=lambda x:int(x[0][2:]))

    total = (len(res) - 1) // 10
    if 0 <= int(pagenum) < total:
        ret = res[10 * int(pagenum): 10 * (int(pagenum) + 1)]
    elif int(pagenum) < 0:
        ret = res[0: 10]
    else:
        ret = res[total * 10:]
    return ret, total


def getlinks(num):
    sql = 'select links from bulletin where num = %(num)s;'
    value = {
        'num': num
    }
    cur.execute(sql, value)
    res = cur.fetchall()[0][0]
    return res


def getname(num):
    sql = 'select name from bulletin where num = %(num)s;'
    value = {
        'num': num
    }
    cur.execute(sql, value)
    res = cur.fetchall()[0][0]
    return res


def getbank(num):
    sql = 'select bank from bulletin where num = %(num)s;'
    value = {
        'num': num
    }
    cur.execute(sql, value)
    res = cur.fetchall()[0][0]
    return res

