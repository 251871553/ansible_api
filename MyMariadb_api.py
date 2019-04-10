import pymysql


class Mariadb_api(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect(host='10.11.6.64', user='admin', passwd='ZTc2YTUyNm_admin', db='ansible_inv', port=3306, charset="utf8")
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def select_db(self,sql_cmd):
        self.cur = self.conn.cursor()
        #cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.cur.execute(sql_cmd)
        #rows = self.cur.execute(sql_cmd)
        rows = self.cur.fetchall()
#        print(rows)
        self.cur.close()
        return rows
        #sql ='insert into userinfo (user,pwd) values (%s,%s);'
        #name = 'wuli'
        #pwd = '123456789'
        #cursor.execute(sql, [name, pwd])     //solve  select * from xxx  where id =a or id=b;

    def insert_db(self,sql_cmd):
        self.cur = self.conn.cursor()
        #sql_cmd="INSERT INTO USER1 (name,age) values  ( 'bob701', 27)"
        try:
           rows=self.cur.execute(sql_cmd)
           self.conn.commit()
        except:
           rows=self.conn.rollback()
        finally:
#           print(rows)
           self.cur.close()
           return rows

    def insert_many_db(self,sql_cmd):
        self.cur = self.conn.cursor()
        #sql_cmd="INSERT INTO USER1 (name,age) values  ( %s, %s)"
        try:
           rows=self.cur.executemany(sql_cmd,[('tom2',1),('abc1',123)])
           self.conn.commit()
        except Exception as e :
           print(e)
           rows=self.conn.rollback()
        finally:
#           print(rows)
           self.cur.close()
           return rows

    def update_db(self,sql_cmd):
        self.cur = self.conn.cursor()
        #sql_cmd="update USER1 set name='asd1' where id=9"
        try:
           rows=self.cur.execute(sql_cmd)
           self.conn.commit()
        except Exception as e :
           print(e)
           rows=self.conn.rollback()
        finally:
#           print(rows)
           self.cur.close()
           return rows

    def delete_db(self,sql_cmd):
        self.cur = self.conn.cursor()
        #sql_cmd="delete from USER1 where id=23"
        try:
           rows=self.cur.execute(sql_cmd)
           self.conn.commit()
        except Exception as e :
           print(e)
           rows=self.conn.rollback()
        finally:
#           print rows
           self.cur.close()
           return rows

    def __del__(self):
        self.conn.close()


if __name__ != "__main__":
     pass
