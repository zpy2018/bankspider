import mysql.connector
from bank import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

cnn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
cur = cnn.cursor(buffered=True)


class Sql:

    @classmethod
    def insert(cls, num, name, url, bank, links):
        sql = 'INSERT INTO bulletin (`num`, `name`, `url`, `bank`, `links`)' \
              ' VALUES (%(num)s, %(name)s, %(url)s, %(bank)s, %(links)s)'
        value = {
            'num': num,
            'name': name,
            'url': url,
            'bank': bank,
            'links': links
        }
        cur.execute(sql, value)
        cnn.commit()
        print('插入成功！！！')
    # @classmethod
    # def id_name(cls, xs_name):
    #     sql = 'SELECT id FROM dd_name WHERE xs_name=%(xs_name)s'
    #     value = {
    #         'xs_name': xs_name
    #     }
    #     cur.execute(sql, value)
    #     for name_id in cur:
    #         return name_id[0]

    @classmethod
    def select(cls, num):
        sql = "SELECT EXISTS(SELECT 1 FROM bulletin WHERE num=%(num)s)"
        value = {
            'num': num
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]

