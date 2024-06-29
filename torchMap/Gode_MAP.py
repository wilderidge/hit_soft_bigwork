import requests
import pandas as pd


def get_jingwei(address):
    url = 'https://restapi.amap.com/v3/geocode/geo?parameters/GET'
    parms = {
        'key': '35fb55770e895cada2a792bd1c4768d8',
        'address': address
    }
    response = requests.get(url, parms)
    data = response.json()
    a = list()
    if data['status'] == '0':
        print('根据地址拿经纬度请求失败')
        return None
    else:
        print('根据地址拿经纬度请求成功')
    for i in data['geocodes']:
        a.append(i['location'])
    return a


def use_jingwei(jingwei, radius='1000'):
    # jingwei是一个字符串，格式为'经度,纬度'
    url = 'https://restapi.amap.com/v3/geocode/regeo?parameters/GET'
    parms = {
        'key': '35fb55770e895cada2a792bd1c4768d8',
        'location': jingwei,
        'radius': radius,
        'extensions': 'base'
    }
    response = requests.get(url, parms)
    data = response.json()
    print(data)
    if data['status'] == '0':
        print('根据经纬度拿地址请求失败')
        return None
    else:
        print('根据经纬度拿地址请求成功')
    a = {
        'formatted_address': data['regeocode']['formatted_address'],
        'province': data['regeocode']['addressComponent']['province'],
        'city': data['regeocode']['addressComponent']['city'],
        'district': data['regeocode']['addressComponent']['district'],
        'towncode': data['regeocode']['addressComponent']['towncode'],
        'township': data['regeocode']['addressComponent']['township'],
        'streetNumber': data['regeocode']['addressComponent']['streetNumber'],
        'businessAreas': data['regeocode']['addressComponent']['businessAreas'],
        'adcode': data['regeocode']['addressComponent']['adcode'],
        'country': data['regeocode']['addressComponent']['country'],
        'neighborhood': data['regeocode']['addressComponent']['neighborhood'],
        'building': data['regeocode']['addressComponent']['building'],
        'citycode': data['regeocode']['addressComponent']['citycode']
    }
    return a


class Lu_Jing:
    def __init__(self, start, end, city=None):
        self.key = '35fb55770e895cada2a792bd1c4768d8'
        self.start = start
        self.end = end
        self.start_jingwei = get_jingwei(start)
        self.end_jingwei = get_jingwei(end)
        self.city = city  # 本地公交所在城市或跨市公交起点城市    只有公交需要用

    def precise_jingwei(self, jingwei_str):
        jingwei = jingwei_str.split(',')
        return f"{round(float(jingwei[0]), 5)},{round(float(jingwei[1]), 5)}"

    # 返回的是一个列表，列表中的元素是字典，字典中的元素是路径规划的信息
    # distance 起点和终点的步行距离，单位为米
    # duration 起点和终点的步行时间，单位为秒
    # paths 路径规划方案，可能包含多个方案，按照规划的距离从小到大排序
    # steps 步行方案，可能包含多个步行子路径
    # instruction 步行子路径的行走指示
    # 剩下的懒得写了，自己去高德的官网上看吧，网址在下面，四个都有详细的说明
    # https://lbs.amap.com/api/webservice/guide/api/direction
    def Bu_Xing(self):
        url = 'https://restapi.amap.com/v3/direction/walking?parameters/GET'
        # print(len(self.start_jingwei))
        # print(len(self.end_jingwei))
        b = list()
        for i in range(len(self.start_jingwei)):
            for j in range(len(self.end_jingwei)):
                parms = {
                    'key': self.key,
                    'origin': self.precise_jingwei(self.start_jingwei[i]),
                    'destination': self.precise_jingwei(self.end_jingwei[j])
                }
                response = requests.get(url, parms)
                data = response.json()
                a = list()
                if data['status'] == '0':
                    print(f'第{i * len(self.end_jingwei) + j + 1}次请求失败')
                    continue
                else:
                    print(f'第{i * len(self.end_jingwei) + j + 1}次请求成功')
                for i in range(int(data['count'])):
                    a.append(data['route']['paths'][i])
                b.append(a)
        return b

    def Gong_Jiao(self):
        url = 'https://restapi.amap.com/v3/direction/transit/integrated?parameters/GET'
        # print(len(self.start_jingwei))
        # print(len(self.end_jingwei))
        b = list()
        for i in range(len(self.start_jingwei)):
            for j in range(len(self.end_jingwei)):
                parms = {
                    'key': self.key,
                    'origin': self.precise_jingwei(self.start_jingwei[i]),
                    'destination': self.precise_jingwei(self.end_jingwei[j]),
                    'city': self.city
                }
                response = requests.get(url, parms)
                data = response.json()
                a = dict()
                if data['status'] == '0':
                    print(f'第{i * len(self.end_jingwei) + j + 1}次请求失败')
                    continue
                else:
                    print(f'第{i * len(self.end_jingwei) + j + 1}次请求成功')
                for i in range(int(data['count'])):
                    for j in data['route']['transits'][i]['segments']:
                        a = j['bus']['buslines']
                        for k in a:
                            if 'polyline' in k:
                                del k['polyline']
                            print(k)
                            b.append(k)
        return b

    def Jia_Che(self):
        url = 'https://restapi.amap.com/v3/direction/driving?parameters/GET'
        # print(len(self.start_jingwei))
        # print(len(self.end_jingwei))
        b = list()
        for i in range(len(self.start_jingwei)):
            for j in range(len(self.end_jingwei)):
                parms = {
                    'key': self.key,
                    'origin': self.precise_jingwei(self.start_jingwei[i]),
                    'destination': self.precise_jingwei(self.end_jingwei[j]),
                    'extensions': 'base'
                }
                response = requests.get(url, parms)
                data = response.json()
                a = list()
                if data['status'] == '0':
                    print(f'第{i * len(self.end_jingwei) + j + 1}次请求失败')
                    continue
                else:
                    print(f'第{i * len(self.end_jingwei) + j + 1}次请求成功')
                for i in data['route']['paths']:
                    for k in i['steps']:
                        if 'polyline' in k:
                            del k['polyline']
                    a.append(i)
                b.append(a)
        return b

    def Qi_Xing(self):
        url = 'https://restapi.amap.com/v4/direction/bicycling?parameters/GET'
        # print(len(self.start_jingwei))
        # print(len(self.end_jingwei))
        b = list()
        for i in range(len(self.start_jingwei)):
            for j in range(len(self.end_jingwei)):
                parms = {
                    'key': self.key,
                    'origin': self.precise_jingwei(self.start_jingwei[i]),
                    'destination': self.precise_jingwei(self.end_jingwei[j])
                }
                response = requests.get(url, parms)
                data = response.json()
                a = list()
                if not data['errmsg'] == "OK":
                    print(f'第{i * len(self.end_jingwei) + j + 1}次请求失败')
                    continue
                else:
                    print(f'第{i * len(self.end_jingwei) + j + 1}次请求成功')
                for i in data['data']['paths']:
                    a.append(i['steps'])
                b.append(a)
        return b


class Tian_Qi:
    def __init__(self, city):
        self.my_pd = pd.read_csv('data/adcode_citycode.csv')
        self.key = '35fb55770e895cada2a792bd1c4768d8'
        self.city = city
        self.citycode = self.my_pd[self.my_pd['中文名'] == city]['adcode'].values[0]

    def get_tianqi_base(self):
        url = 'https://restapi.amap.com/v3/weather/weatherInfo?parameters/GET'
        parms = {
            'key': self.key,
            'city': self.citycode,
            'extensions': 'base'
        }
        response = requests.get(url, parms)
        data = response.json()
        if data['status'] == '0':
            print('请求失败')
            return None
        else:
            print('请求成功')
        b = list()
        for i in range(int(data['count'])):
            b.append(data['lives'][i])
        return b

    def get_tianqi_pre(self):
        url = 'https://restapi.amap.com/v3/weather/weatherInfo?parameters/GET'
        parms = {
            'key': self.key,
            'city': self.citycode,
            'extensions': 'all'
        }
        response = requests.get(url, parms)
        data = response.json()
        if data['status'] == '0':
            print('请求失败')
            return None
        else:
            print('请求成功')
        b = list()
        for i in range(int(data['count'])):
            b.append(data['forecasts'][i])
        return b


class search:
    def __init__(self, address):
        self.address = address
        self.jingwei = get_jingwei(address)

    def Get_accurate_address(self, city=None, location=None):
        url = 'https://restapi.amap.com/v3/assistant/inputtips?parameters/GET'
        parms = {
            'key': '35fb55770e895cada2a792bd1c4768d8',
            'keywords': self.address,
            'city': city,
            "location": location
        }
        response = requests.get(url, parms)
        data = response.json()
        if data['status'] == '0':
            print('请求失败')
            return None
        else:
            print('请求成功')
        b = list()
        for i in data['tips']:
            b.append(i)
        return b


def Get_railwy_station_add(jingwei=None, addr=None):
    url = 'https://restapi.amap.com/v3/place/around?parameters/GET'
    if jingwei == None and not addr == None:
        jingwei = get_jingwei(addr)[0]
    parms = {
        'key': '35fb55770e895cada2a792bd1c4768d8',
        'location': jingwei,
        'keywords': '火车站',
        'sortrule': 'distance',
        'types': '150200'
    }
    response = requests.get(url, parms)
    data = response.json()
    if not data['info'] == 'OK':
        print('请求失败')
        return None
    else:
        print('请求成功')
    b = list()
    for i in data['pois']:
        a = {
            'location': i['location'],
            'name': i['name'],
            'address': i['address'],
            'distance': i['distance'],
            'photos': i['photos']
        }
        b.append(a)
    return b


def Get_jingdian(city):
    url = 'https://restapi.amap.com/v3/place/text?parameters/GET'
    parms = {
        'key': '35fb55770e895cada2a792bd1c4768d8',
        'keywords': '风景名胜',
        'types': '110000',
        'city': city
    }
    response = requests.get(url, parms)
    data = response.json()
    if not data['info'] == 'OK':
        print('请求失败')
        return None
    else:
        print('请求成功')
    b = list()
    for i in data['pois']:
        a = {
            'type': i['type'],
            'location': i['location'],
            'name': i['name'],
            'address': i['address'],
            'photos': i['photos']
        }
        b.append(a)
    return b

if __name__ == '__main__':
    # print(use_jingwei(get_jingwei("哈尔滨哈特广场")[0])['formatted_address'])
    # print(get_jingwei('哈尔滨工业大学二校区'))
    #use_jingwei(get_jingwei(start)[0]), use_jingwei(get_jingwei(dest)[0])
    #my_LJ = Lu_Jing('哈尔滨工业大学', '哈尔滨工业大学二校区', '哈尔滨')
    #print(my_LJ.Bu_Xing()[0])
    # ans=my_LJ.Gong_Jiao()
    #print(my_LJ.Jia_Che()[0])
    # my_TQ = Tian_Qi('哈尔滨市')
    # print(my_TQ.get_tianqi_base())
    # print(my_TQ.get_tianqi_pre())
    # print(use_jingwei('126.63177,45.74208'))    # 126.63177,45.74208是哈尔滨工业大学的经纬度，可以自己换成别的经纬度试试看
    b = Get_jingdian(city='哈尔滨市')
    print(b)
    pass