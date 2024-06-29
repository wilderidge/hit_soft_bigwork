import requests
import json

key = '35fb55770e895cada2a792bd1c4768d8'


# 获取地址编码，传进地址(字符串类型)
def get_code(address: str):
    # 网址的参数
    parameters = {'key': key, 'address': address}
    # 网址url
    res = requests.get("https://restapi.amap.com/v3/geocode/geo?parameters", params=parameters)
    # 获取到字符串类型，要获取地址编码需要转型
    r = res.text
    # 把字符串转换成一个Python对象，对象可以是字典，列表...这里是字典
    jd = json.loads(r)
    # 从中获得
    code = jd['geocodes'][0]['location']
    return code


def get_route(origin: str, destination: str):
    code1 = get_code(origin)
    code2 = get_code(destination)
    parameters2 = {'key': key, 'origin': code1, 'destination': code2}
    res2 = requests.get("https://restapi.amap.com/v3/direction/walking?parameters", params=parameters2)
    r = res2.text
    jd2 = json.loads(r)
    steps = jd2['route']['paths'][0]['steps']
    len_steps = len(steps)
    for i in range(len_steps):
        step = steps[int(i)]['instruction']
        print(step)


ori = input('输入起始点：')
des = input('输入终点：')
get_route(ori, des)