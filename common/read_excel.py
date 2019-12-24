# @author       ：小青年
# @ProjectName  ：py24_unittest_class
# @Name         ：read_excel
# @time         ：2019/11/21 12:46


import openpyxl
import os
from common.contants import data_dir
filename=os.path.join(data_dir,"test_data_01.xlsx")

"""ddt：通过用例数据生成测试用例"""
# 用来保存用来数据
class CaseData:  # 用来保存用来数据
    pass


class ReadExcel(object):
    def __init__(self, file_name, sheet_name):
        self.file_name = file_name
        self.sheet_name = sheet_name

    # 打开工作簿的方法
    def open(self):
        # 打开工作簿、选中表单
        self.workbook = openpyxl.load_workbook(self.file_name)  # 创建工作簿workbook对象
        self.sheet = self.workbook[self.sheet_name]  # 创建表单对象

    #关闭工作簿的方法
    def close(self):
    #关闭工作簿对象，释放内存
        self.workbook.close()
    #返回的数据为：列表嵌套字典的格式
    def read_excel(self):
        # (1)打开工作簿，调用open方法
        self.open()
        # （2）按行获取所有的格子
        rows = list(self.sheet.rows)  # 按行获取所有的格子
        # (3)获取表头
        title = []
        for r in rows[0]:
            title.append(r.value)
        cases = []
        # (4)遍历除了表头剩余的行
        for row in rows[1:]:  # r：格子对象
            # print(row)  # 通过value获取格子里面的数据
            # （5）创建一个空列表，用来存储该行的数据
            data = []
            # （6）再次遍历该行里的每一个格子
            for r in row:  # r：格子对象
                # print(r.value)  # 通过value获取格子里面的数据
                # （7）将该行的格子中的数据，添加到data中
                data.append(r.value)
            # print(data)
            # （8）将title和data进行打包，转换成字典
            case = dict(zip(title, data))
            # print(case)
            # (9)将该行数据添加到cases列表里面
            cases.append(case)
        #(10)关闭工作簿
        self.close()
        # print(cases)
        return cases

    # 获取的数据为对象：object
    # 返回的数据为：列表嵌套对象的格式
    def read_excel_obj(self):

        # (1)打开工作簿，调用open方法
        self.open()
        # （2）按行获取所有的格子
        rows = list(self.sheet.rows)  # 按行获取所有的格子
        # (3)获取表头
        title = []
        for r in rows[0]:
            title.append(r.value)
        cases = []
        # (4)遍历除了表头剩余的行
        for row in rows[1:]:  # r：格子对象
            # print(row)  # 通过value获取格子里面的数据
            # （5）创建一个空列表，用来存储该行的数据
            data = []
            # （6）再次遍历该行里的每一个格子
            for r in row:  # r：格子对象
                # print(r.value)  # 通过value获取格子里面的数据
                # （7）将该行的格子中的数据，添加到data中
                data.append(r.value)
            # print(data)
            # （8）将title和data进行打包，转换成列表
            case = list(zip(title, data))

            # （9）创建一个对象用来保存该行用例数据
            case_obj = CaseData()  # 创建对象
            # (10)遍历列表中该行用例数据、使用setattr设置为对象属性和属性值
            for k, v in case:
                # print(k,v)
                setattr(case_obj, k, v)  # 属性动态设置
            # print(case_obj, case_obj.__dict__)#保存为case_obj的属性和属性值
            # (11)将对象添加到cases列表里面
            cases.append(case_obj)
        # (12)关闭工作簿
        self.close()
        # (13)返回cases:包含所有用例数据对象的列表
        return cases
    #写入数据到excel的方法
    def write_data(self,row,column,value):
        #(1)打开工作簿
        self.open()
        #(2)写入数据
        self.sheet.cell(row=row,column=column,value=value)
        #(3)保存文件
        self.workbook.save(self.file_name)
        #(4)关闭工作簿
        self.close()
if __name__ == '__main__':
    excel = ReadExcel(filename, "login")
    test_data = excel.read_excel()
    print(test_data)

