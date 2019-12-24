# @author       ：小青年
# @ProjectName  ：py24_api_test_day1206
# @Name         ：handle_db
# @time         ：2019/12/8 10:57 

import pymysql
from common.read_conf import conf


class HandleDB:
    # 先连接连接数据库
    def __init__(self):
        # 连接数据库
        self.con = pymysql.connect(host=conf.get_str("mysql", "host"),
                                   user=conf.get_str("mysql", "user"),
                                   password=conf.get_str("mysql", "password"),
                                   port=conf.get_int("mysql", "port"),  # 获取整数类型用get_int
                                   charset=conf.get_str("mysql", "charset"))  # charset：编码方式
        # 创建一个游标
        self.cur = self.con.cursor()

    # 获取查询到的第一条数据的方法
    def get_one(self, sql):
        # 在执行查询语句之前一定要增加commit，保证当前的状态与数据库是同步实时的
        self.con.commit()
        # 通过游标对象去执行传入的sql语句
        self.cur.execute(sql)  # 此处self是调用的init方法
        return self.cur.fetchone()

    # 获取sql语句查询到的所有数据
    def get_all(self, sql):
        # 在执行查询语句之前一定要增加commit
        self.con.commit()
        # 通过游标对象去执行传入的sql语句
        self.cur.execute(sql)  # 此处self是调用的init方法
        return self.cur.fetchall()

    # 获取sql语句查询到的所有数据的条数
    def count(self, sql):
        # 在执行查询语句之前一定要增加commit
        self.con.commit()
        # 通过游标对象去执行传入的sql语句
        res=self.cur.execute(sql)  # 此处self是调用的init方法
        return res
    # 关闭数据库方法
    def close(self):
        # 关闭游标对象
        self.cur.close()
        # 断开连接对象
        self.con.close()
if __name__ == '__main__':
    sql1 = "select leave_amount from futureloan.member where mobile_phone=15500000016"
    res=HandleDB().get_one(sql1)
    print(res)
    res1=res[0]
    res2=float(res1)
    print(res2)
    print(type(res2))