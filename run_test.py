# @author       ：小青年
# @ProjectName  ：py24_test_project_day1125
# @Name         ：run_test
# @time         ：2019/11/25 23:45 

"""
测试用例运行程序的四个步骤：
（1）第一步：创建一个测试套件
（2）第二步：将测试用例，加载到测试套件中
 (3)第三步：创建一个测试程序运行程序启动器
 (4)第四步：使用启动器去执行测试套件
"""

# 测试用例运行程序
import unittest
import os
from library.HTMLTestRunnerNew import HTMLTestRunner
from common.contants import case_dir# 测试用例模块所在的目录
from common.contants import reports_dir# 测试报告的目录
from common.read_conf import conf  # 导入配置文件解释器对象
filename = conf.get_str("report", "filename")
# （1）第一步：创建测试套件
suite = unittest.TestSuite()

# （2）第二步：加载用例到套件中
# ①通过loader去加载
loader = unittest.TestLoader()
# ②往套件里面加载测试用例：通过所在目录路径加载
suite.addTest(loader.discover(case_dir))  # 给一个用例的所在目录的绝对路径
# 备注：加r的目的是防止转义
# (3)第三步：创建一个测试用例运行程序
report_path = os.path.join(reports_dir,filename)
with open(report_path, "wb") as f:  # 生成html文件的测试报告
    runner = HTMLTestRunner(
        stream=f,  # 打开一个报告文件，将句柄传给stream
        tester="小青年,",  # 报告中形式的测试人员，可添加多个
        description="报告的描述信息",  # 报告中显示的描述信息
        title="报告的标题")  # 报告的标题
    # (4)第四步：运行测试套件
    runner.run(suite)
