# @author       ：小青年
# @ProjectName  ：py24_test_project_day1127
# @Name         ：contants
# @time         ：2019/11/27 23:35 

"""
该模块用来处理整个项目目录的路径
"""
import os

# __file__)：当前文件的绝对路径
# dirname：获取父级目录
# print(__file__)
# # # 当前文件的绝对路径方法：如果运行的时候，项目目录路径出错，使用abspath的方式来获取当前文件的路径
# dir = os.path.abspath(__file__)
# print(dir)
# # (1)当前文件所在的父级目录绝对路径
# res=os.path.dirname(__file__)
# print(res)
# #(2)获取当前项目的根目录
# basedir=os.path.dirname(res)


# 项目目录的路径：如果运行的时候，项目目录路径出错，使用abspath的方式来获取当前文件的路径
basedir = os.path.dirname(os.path.dirname(__file__))
print(basedir)
# 配置文件的路径
conf_dir = os.path.join(basedir, "conf")  # 项目路径与配置文件的目录进行拼接
# 用例数据的目录
data_dir = os.path.join(basedir, "data")
# 日志文件目录
log_dir = os.path.join(basedir, "log")
# 测试报告的目录
reports_dir = os.path.join(basedir, "reports")
# 测试用例模块所在的目录
case_dir = os.path.join(basedir, "TestCases")

