# @author       ：小青年
# @ProjectName  ：py24_api_test_day1211
# @Name         ：handle_data
# @time         ：2019/12/12 14:04 

# 处理数据替换的模块
# 专门用来保存一些要替换的数据
class TestData:
    # 要替换的内容先设置位类属性
    member_id = ""  # 没有替换前，先设置默认值为空


import re
from common.read_conf import conf

def replace_data(data):
    r = r"#(.+?)#"  # 匹配规则
    # 判断是否有需要替换的数据
    while re.search(r, data):  # 如果匹配到有数据，就提取出来
        # 匹配出第一个要替换的数据
        res = re.search(r, data)
        # 提取待替换的内容
        item = res.group()
        # 获取替换内容的数据项
        key = res.group(1)
        try:
            # 根据替换内容中的数据项去配置文件中找到对应的内容，进行替换
            data = data.replace(item, conf.get_str("test_data", key))
        except:  # 没有可以通过提取的时候，写入配置文件中
            # 没有进行替换，替换成
            data = data.replace(item, getattr(TestData, key))  # getattr：动态的获取属性
            # 备注：TestData传入类名，key如果没有找到就去类里面获取属性
    # 返回替换好的数据
    return data  # 替换完后，返回data


# data2 = '{"member_id": "#member_id#","amount":600}'
# data2 = replace_data(data2)
# print(data2)
