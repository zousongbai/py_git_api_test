# @author       ：小青年
# @ProjectName  ：py24_unittest_class
# @Name         ：my_log
# @time         ：2019/11/25 22:19 

import logging
import os
from common.read_conf import conf  # 导入配置文件解释器对象
from common.contants import log_dir#导入日志目录的路径
# 日志有哪些内容需要放在配置文件里面：收集器的等级、输出到文件的等级、输出到控制台的等级
# 读取配置文件中的数据
# (1)收集器的等级
level = conf.get_str("logging", "level")
# (2)输出到文件的等级
f_level = conf.get_str("logging", "f_leval")
# (3)输出到控制台的等级
s_leval = conf.get_str("logging", "s_leval")
# (4)读取日志文件的名字
filename = conf.get_str("logging", "filename")
#获取日志文件的绝对路径
file_path=os.path.join(log_dir,filename)
class MyLog(object):
    @staticmethod  # 封装成类方法
    def create_logger():  # 该方法用来创建日志收集器的
        # (1)步骤一：创建一个名为：py24的日志收集器
        my_log = logging.getLogger("py24")

        # (2)步骤二：设置日志收集器的等级
        my_log.setLevel(level)

        # (3)步骤三：添加输出渠道(输出到控制台)
        # ①创建一个输出到控制台的输出渠道
        sh = logging.StreamHandler()
        # ②设置输出等级：设置输出到控制台的等级
        sh.setLevel(s_leval)
        # ③将输出渠道绑定到日志收集器上
        my_log.addHandler(sh)

        # (4)步骤四：添加输出渠道(输出到文件)
        # ①创建一个输出到文件的输出渠道
        fh = logging.FileHandler(file_path,encoding="utf-8")  # 输出到log.log的文件里面
        # ②设置输出等级：设置输出到控制台的等级
        fh.setLevel(f_level)
        # ③将输出渠道绑定到日志收集器上
        my_log.addHandler(fh)

        # (5)步骤五：设置日志输出的格式
        # ①创建一个日志输出格式
        formatter = logging.Formatter('%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s')
        # asctime：当前系统的时间
        # filename：当前文件名
        # lineno：当前输出是哪一行
        # levelname：当前输出日志的等级
        # message：输出的日志信息
        # ②将输出格式和输出渠道进行绑定
        sh.setFormatter(formatter)  # 输出到控制台的绑定
        fh.setFormatter(formatter)  # 输出到文件的绑定

        return my_log


# 调用类的静态方法，创建一个日志收集器my_log
my_log = MyLog().create_logger()  # 用于test_register_login.py导入日志收集器my_log
