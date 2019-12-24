# @author       ：小青年
# @ProjectName  ：py24_test_project_day1202
# @Name         ：handle_request
# @time         ：2019/12/3 14:04 

"""
封装的目的：

封装的需求：
（1）发送post请求、发送get请求、发送patch请求
（2）代码中如何做到不同请求方式的接口去发送不同的请求
（3）解决方法：加判断
"""
import requests


# 封装处理请求的类
class HandleRequest:
    def send(self, url, method, params=None, json=None, data=None, headers=None):
        # 将请求的方法转换为小写
        method = method.lower()
        # post时，params参数不需要传参。get时，json和headers参数不需要传参，所以需要加默认值
        if method == "post":
            return requests.post(url=url, json=json, data=data, headers=headers)
        elif method == "patch":
            return requests.patch(url=url, json=json, data=data, headers=headers)
        elif method == "get":
            return requests.get(url=url, params=params)
        # 备注：如果还有其他方式，就用elif添加


# 处理session鉴权的接口，使用这个类发送请求
class HandleSessionRequest:
    def __init__(self):
        # 创建session对象
        self.se = requests.session()

    def send(self, url, method, params=None, json=None, data=None, headers=None):
        # 将请求的方法转换为小写
        method = method.lower()
        # post时，params参数不需要传参。get时，json和headers参数不需要传参，所以需要加默认值
        if method == "post":
            return self.se.post(url=url, json=json, data=data, headers=headers)
        elif method == "patch":
            return self.se.patch(url=url, json=json, data=data, headers=headers)
        elif method == "get":
            return self.se.get(url=url, params=params)


if __name__ == '__main__':
    # 登录接口地址
    login_url = "http://api.lemonban.com/futureloan/member/login"
    # 登录的参数
    login_data = {
        "mobile_phone": "15500000016",
        "pwd": "123456aa"
    }
    # 登录的请求头
    header = {"X-Lemonban-Media-Type": "lemonban.v2",
              "Content-Type": "application/json"}
    http = HandleRequest()
    res = http.send(url=login_url, method="POST", json=login_data, headers=header)
    print(res.json())
