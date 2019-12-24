# @author       ：小青年
# @ProjectName  ：py24_api_test_day1206
# @Name         ：test_recharge
# @time         ：2019/12/6 21:20 

import unittest
from common.read_excel import ReadExcel
from common.contants import data_dir  # 用例数据所在的路径
import os
from library.ddt import ddt, data
from common.read_conf import conf  # 配置文件解析对象
from common.handle_request import HandleRequest
from common.my_log import my_log  # 导入日志
import jsonpath
from common.handle_db import HandleDB
import decimal

# ----------------------修改充值用例类-----------------------------------------
from common.handle_data import TestData,replace_data
data_file_path = os.path.join(data_dir, "test_data.xlsx")  # 用例数据的路径
user = conf.get_str("test_data", "user")
pwd = conf.get_str("test_data", "pwd")
"""
setUpClass中提取的用户id和token，如何在用例方法中使用
（1）设为全局变量
（2）保存为类属性：在setUpClass类中，通过加上cls，设置为类属性，测试方法直接通过self调用类属性
（3）写入到配置文件
（4）保存在临时变量的类中(后面会讲的，先不要去研究)
"""


@ddt
class TestRecharge(unittest.TestCase):
    # 通过类创建excel对象
    excel = ReadExcel(data_file_path, "recharge")
    # 读取数据
    test_data = excel.read_excel()
    http = HandleRequest()
    # 创建DB对象
    db = HandleDB()

    @classmethod
    def setUpClass(cls):  # 在测试用例类(TestRecharge)执行之前就会执行这个方法
        # 登录：获取用户的id以及鉴权需要用到的token
        url = conf.get_str("env", "url_ip") + "/member/login"
        login_data = {
            "mobile_phone": user,
            "pwd": pwd
        }
        headers = eval(conf.get_str("env", "headers"))
        response = cls.http.send(url=url, method="post", json=login_data,
                                 headers=headers)  # 此处用cls是因为是类方法setUpClass(cls)里面的，是通过类属性去调用的
        result = response.json()
        # 登录之后，从响应结果中提取用户id和token
        # （1）获取用户id
        # cls.member_id = str(jsonpath.jsonpath(result, "$..id")[0])#设置为TestRecharge类的类属性

        member_id = jsonpath.jsonpath(result, "$..id")[0] # 获取member_id
        print(member_id)
        # 设置TestData类的类属性
        setattr(TestData,"member_id",str(member_id))#设置TestData类的类属性,设置类属性为member_id，类属性的值为member_id
        # （2）提取token
        token_type = jsonpath.jsonpath(result, "$..token_type")[0]
        token = jsonpath.jsonpath(result, "$..token")[0]
        # cls.token_data = token_type + " " + token#设置为TestRecharge类的类属性
        token_data = token_type + " " + token  #
        setattr(TestData, "token_data", token_data)  # 设置TestData类的类属性,设置类属性为token_data，类属性的值为token_data
    # def setUp(self):#每个用例执行之前都会执行
    # 如果把登录放在这里，每执行完一个用例就会登录，增加代码的运行时间，没有必要
    @data(*test_data)  # 进行解包
    def test_recharge(self, test_data_cases):
        # 第一步：准备用例数据
        # 备注：列表、字典方式存储的，excel读取出来是字符串。数值类型，读取出来是数值类型的，字符串类型，读取出来是字符串类型。
        # ①拼接完整的接口地址
        url = conf.get_str("env", "url_ip") + test_data_cases["url"]
        # ②请求的方法
        method = test_data_cases["method"]

        # ③请求参数
        # 判断是否有用户id需要替换
        # if "#member_id#" in test_data_cases["data"]:
        #     # 进行替换
        #     test_data_cases["data"] = test_data_cases["data"].replace("#member_id#",
        #                                                               self.member_id)  # 替换完后需要接收，不然没有实质的替换
        test_data_cases["data"]=replace_data(test_data_cases["data"])#调用replace_data方法
        data = eval(test_data_cases["data"])

        # ④请求头
        headers = eval(conf.get_str("env", "headers"))
        # 添加鉴权
        # headers["Authorization"] = self.token_data
        # 从TestData类里面获取token_data属性：两种方法
        # headers["Authorization"] = TestData.token_data#方法一：直接从TestData类里面获取token_data属性
        headers["Authorization"] = getattr(TestData,"token_data") # 方法二：用getattr获取TestData类里面获取token_data属性
        # ⑤预期结果
        expected = eval(test_data_cases["expected"])
        # ⑥该用例在表单中所在行
        row = test_data_cases["case_id"] + 1

        # 第二步：发送请求到接口，获取实际结果
        if test_data_cases["check_sql"]:  # 先判断用例里面check_sql字段是否有数据，如果有数据，说明需要进行数据库校验
            sql = test_data_cases["check_sql"].format(user)
            # 获取充值之前的余额
            start_money = self.db.get_one(sql)[0]

        response = HandleRequest().send(url=url, method=method, json=data, headers=headers)
        result = response.json()

        # 第三步：比对预期结果和实际结果
        try:
            self.assertEqual(expected["code"], result["code"])
            self.assertEqual(expected["msg"], result["msg"])
            # 充值后，进行数据库校验
            if test_data_cases["check_sql"]:
                sql = test_data_cases["check_sql"].format(user)
                # 获取充值之后的余额
                end_money = self.db.get_one(sql)[0]
                # 获取请求参数里面的充值金额
                recharge_money = decimal.Decimal(str(data["amount"]))
                my_log.info("充值之前金额为：{}\n，充值金额为：{}\n，充值之后金额为：{}\n".format(start_money, recharge_money, end_money))
                # 进行断言
                self.assertEqual(recharge_money, end_money - start_money)
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
