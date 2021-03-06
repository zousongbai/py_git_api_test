# @author       ：小青年
# @ProjectName  ：py24_api_test_day1213
# @Name         ：test_07_invest
# @time         ：2019/12/15 14:57 

import unittest
from common.read_excel import ReadExcel
import os
from common.contants import data_dir
from library.ddt import ddt,data
from common.read_conf import conf
from common.handle_data import replace_data,TestData
import jsonpath
from common.handle_request import HandleRequest
from common.my_log import my_log
file_path=os.path.join(data_dir,"test_data.xlsx")
@ddt
class TestInvest(unittest.TestCase):
    excel=ReadExcel(file_path,"invest")
    test_data=excel.read_excel()
    http=HandleRequest()
    @data(*test_data)
    def test_invest(self,test_data_cases):
        # 第一步：准备用例数据
        # (1)获取url
        url = conf.get_str("env", "url_ip") + test_data_cases["url"]
        # （2）获取数据
        test_data_cases["data"] = replace_data(test_data_cases["data"])  # 调用replace_data方法
        # （3）数据转换
        data = eval(test_data_cases["data"])
        # (4)预期结果
        expected = eval(test_data_cases["expected"])  # excel是字典类型，需要转换一下
        # （5）请求方法
        method = test_data_cases["method"]
        # （6）用例所在的行
        row = test_data_cases["case_id"] + 1
        # （7）请求头
        headers = eval(conf.get_str("env", "headers"))
        if test_data_cases["interface"] != "login":
            # 如果不是token，需要添加请求头
            headers["Authorization"] = getattr(TestData, "token_data")  # 调用保存在临时变量的类中


        # 第二步：发送请求到接口，获取实际结果
        res = self.http.send(url=url, method=method, json=data, headers=headers)
        result = res.json()

        # 判断是否是登录用例，是的话，则提取token
        if test_data_cases["interface"] == "login":
            # 如果是登录的用例，提取对应的token
            token_type = jsonpath.jsonpath(result, "$..token_type")[0]
            token = jsonpath.jsonpath(result, "$..token")[0]
            token_data = token_type + " " + token
            # 通过setattr方法保存到TestData类里面
            setattr(TestData, "token_data", token_data)
            # 提取member_id
            member_id = jsonpath.jsonpath(result, "$..id")[0]
            # 通过setattr方法保存到TestData类里面
            setattr(TestData, "member_id", str(member_id))  # 存类属性的时候，需要与excel中的参数名一致
        elif test_data_cases["interface"]=="add":
            #如果是添加项目，则提取项目id
            loan_id = jsonpath.jsonpath(result, "$..id")[0]
            # 通过setattr方法保存到TestData类里面
            setattr(TestData, "admin_member_id", str(loan_id))  # 存类属性的时候，需要与excel中的参数名一致
        # 第三步：比对预期结果和实际结果
        try:
            self.assertEqual(expected["code"], result["code"])
            self.assertEqual(expected["msg"], result["msg"])

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


