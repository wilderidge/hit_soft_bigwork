from qw import *
import re
import json


def qw_jiaotong(departure_city, arrival_city):
    context = f'我想在五一假期期间从{departure_city}出发，前往{arrival_city}旅游。'

    question = '请你为我做出一些建议，并严格按照如下格式填写返回，且不要出现其余无关内容：{"交通安排":"","行程规划":"","旅游活动":""}'
    res = qw_chat(context, question)

    return res


def my_fun(departure_city, arrival_city):
    context = f'我想在五一假期期间从{departure_city}出发，前往{arrival_city}旅游。'

    question = '请你为我做出一些建议，并严格按照如下格式填写返回，且不要出现其余无关内容：{"交通安排":"","行程规划":"","旅游活动":""}'
    res = qw_chat(context, question)

    # 使用正则表达式匹配 JSON 对象
    matches = re.findall(r'\{.*?\}', res, re.DOTALL)

    # 使用 json.loads() 函数解析每个 JSON 对象
    # 在解析之前，先使用 str.replace() 函数将换行符和制表符替换掉
    交通安排 = json.loads(matches[0].replace('\n', ' ').replace('\t', ' '))
    行程规划 = json.loads(matches[1].replace('\n', ' ').replace('\t', ' '))
    旅游活动 = json.loads(matches[2].replace('\n', ' ').replace('\t', ' '))

    print(交通安排["交通安排"])
    print(行程规划["行程规划"])
    print(旅游活动["旅游活动"])
    return 交通安排["交通安排"]


def analysis_location(input_str):
    context = '我想对在国内的出行做一些规划。'
    question = '请从以下输入请求中找到出发地和目的地，并严格按照如下格式填写返回，且不要出现其余无关内容：' \
               '{"出发省":"","出发市":"","目的省":"","目的市":""}，如果输入的请求中不包含省或市的信息，' \
               '为该项填写"null"即可，输入请求如下：\n' + input_str
    result = qw_chat(context, question)
    return result


def analysis_task(input_str):
    context = '我想对在国内的出行做一些规划。'
    question = '请从任务全集中找到较符合以下输入请求的任务子集，' \
               '任务全集：{"检索车票","美食和景点推荐","规划自驾或步行路线","景点实时语音讲解","规划住宿"}，' \
               '并严格按照{...}的格式填写返回，不要出现其余无关内容，' \
               '如果输入的请求中不包含任务全集中的任一个，返回{null}即可，输入请求如下：\n' + input_str

    result = qw_chat(context, question)
    return result


if __name__ == '__main__':
    print(qw_jiaotong("成都", "理塘"))
    print(analysis_location("我想在五一假期期间从成都出发，前往理塘旅游。"))
    print(analysis_task("我想在五一假期期间从成都出发，前往理塘旅游。"))
