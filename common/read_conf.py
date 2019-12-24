# @author       ：小青年
# @ProjectName  ：py24_test_project_day1125
# @Name         ：read_config
# @time         ：2019/11/26 16:01 


from configparser import ConfigParser
from common.contants import conf_dir#导入配置文件的路径
import os
# 1、没有使用继承方式封装
class MyConf:
    def __init__(self, filename, encoding="utf-8"):
        """
        初始化方法：没有使用继承方式封装
        :param filename: 配置文件名
        :param encoding: 文件编码方法
        """
        self.filename = filename
        self.encoding = encoding
        # 创建一个文件解析对象,设置为对象的conf属性
        self.conf = ConfigParser()  # ConfigParser：专门解析配置文件的
        # 使用解释器对象，加载配置文件中的内容
        self.conf.read(filename, encoding)

    # 读取数据
    def get_str(self, section, option):
        """
        :param section:配置块
        :param option:配置项
        :return:对应配置项的数据
        """
        # 使用配置文件解释器，调用里面的get方法，然后传入section和option，获取到后返回出去
        return self.conf.get(section, option)

    # 读取整型数据类型
    def get_int(self, section, option):
        """
        :param section:配置块
        :param option:配置项
        :return:对应配置项的数据
        """
        # 使用配置文件解释器，调用里面的get方法，然后传入section和option，获取到后返回出去
        return self.conf.getint(section, option)

    # 读取浮点数据类型
    def get_float(self, section, option):
        """
        :param section:配置块
        :param option:配置项
        :return:对应配置项的数据
        """
        # 使用配置文件解释器，调用里面的get方法，然后传入section和option，获取到后返回出去
        return self.conf.getfloat(section, option)

    def get_boolean(self, section, option):
        """
        :param section:配置块
        :param option:配置项
        :return:对应配置项的数据
        """
        # 使用配置文件解释器，调用里面的get方法，然后传入section和option，获取到后返回出去
        return self.conf.getboolean(section, option)

    # 写入数据
    def write_data(self, section, option, value):  # 传入块、配置项、写入的内容
        """
        :param section:配置块
        :param option:配置项
        :param value:配置项对应的值
        :return:
        """
        #  (1)写入：通过文件解释器对象，在通过set方法，然后传入块、配置项、写入的内容
        self.conf.set(section, option, value)
        # （2）保存到文件
        self.conf.write(open(self.filename, "w", encoding=self.encoding))

#获取配置文件的绝对路径
conf_path=os.path.join(conf_dir,"conf.ini")
#创建配置文件解析对象
conf=MyConf(conf_path)
