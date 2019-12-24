# @author       ：小青年
# @ProjectName  ：py24_api_test_day1204
# @Name         ：test_login
# @time         ：2019/12/5 12:44 

import unittest
from common.read_excel import ReadExcel
from common.contants import data_dir  # 用例数据所在的路径
import os
from library.ddt import ddt, data
from common.read_conf import conf  # 配置文件解析对象
from common.handle_request import HandleRequest
from common.my_log import my_log  # 导入日志
import random
from common.handle_db import HandleDB
data_file_path = os.path.join(data_dir, "test_data.xlsx")  # 用例数据的路径

@ddt
class TestRegister(unittest.TestCase):
    # 通过类创建excel对象
    excel = ReadExcel(data_file_path, "register")
    # 读取数据
    test_data = excel.read_excel()
    #创建DB对象
    db=HandleDB()
    @data(*test_data)  # 进行解包
    def test_register(self, test_data_cases):
        # 第一步：准备用例数据
        # 备注：列表、字典方式存储的，excel读取出来是字符串。数值类型，读取出来是数值类型的，字符串类型，读取出来是字符串类型。
        # ①拼接完整的接口地址
        url = conf.get_str("env", "url_ip") + test_data_cases["url"]
        # ②请求的方法
        method = test_data_cases["method"]

        # ③请求参数
        #判断是否有手机号需要替换
        if "#phone#" in test_data_cases["data"]:
            #生成一个手机号码
            phone=self.random_phone()
            #进行替换
            test_data_cases["data"]=test_data_cases["data"].replace("#phone#",phone)# 替换完后需要接收，不然没有实质的替换

        data = eval(test_data_cases["data"])
        # ④请求头
        headers = eval(conf.get_str("env", "headers"))
        # ⑤预期结果
        expected = eval(test_data_cases["expected"])
        # ⑥该用例在表单中所在行
        row = test_data_cases["case_id"] + 1
        # 第二步：发送请求到接口，获取实际结果
        response = HandleRequest().send(url=url, method=method, json=data, headers=headers)
        result = response.json()

        # 第三步：比对预期结果和实际结果
        try:
            self.assertEqual(expected["code"], result["code"])
            self.assertEqual(expected["msg"], result["msg"])
            if result["msg"]=="OK":
                #如果注册成功，去数据库查询当前注册的账号是否存在
                sql="select * from futureloan.member where mobile_phone={}".format(phone)
                #获取数据库中有没有该用户的信息：通过db对象，然后调用count方法
                count=self.db.count(sql)#查找的结果
                #数据库中返回的数据做断言，判断是否有一条数据
                self.assertEqual(1,count)
            print("预期结果：{}".format(expected))
            print("实际结果：{}".format(result))
        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="未通过")  # 可以把列(column)放在配置文件里面
            # 记录没有通过的日志
            my_log.info("用例：{}------>执行未通过".format(test_data_cases["title"]))
            # 在没有通过的时候，使用print会打印在测试报告中
            print("预期结果：{}".format(expected))
            print("实际结果：{}".format(result))
            # 在没有通过的时候，将print输出到日志里面
            my_log.info("预期结果：{}".format(expected))
            my_log.info("实际结果：{}".format(result))
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")  # 可以把列(column)放在配置文件里面
            # 记录通过的日志
            my_log.info("用例：{}------>执行通过".format(test_data_cases["title"]))
    @staticmethod
    def random_phone():
        # 生成随机的手机号码
        phone = "136"
        for i in range(8):  # 遍历8次
            phone += str(random.randint(0, 9))  # 每次生成转换为字符串，再与phone进行拼接
        return phone
    @classmethod
    #所有用例执行完后，再执行
    def tearDownClass(cls):
        #关闭数据库的连接和游标对象
        cls.db.close()
