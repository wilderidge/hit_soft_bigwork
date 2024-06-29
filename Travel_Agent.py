import re

import streamlit as st

from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import DuckDuckGoSearchRun
from langchain.prompts import PromptTemplate
from langchain.agents import tool
from langchain.chains import LLMChain
from torchMap.Query12306 import *
from torchMap.Gode_MAP import *


class PromptsTemplateForTask:
    Analysis_Task = PromptTemplate(
        template="请从任务全集中找到较符合以下输入请求的任务子集，{UserMessage}，并严格按照{...}的格式填写返回，不要出现其余无关内容，如果输入的请求中不包含任务全集中的任一个，返回{null}即可",
        input_variables=["UserMessage"]
    )
    Analysis_location = PromptTemplate(
        template="请从以下输入请求中找到日期，出发地和目的地，{UserMessage}，并严格按照元组进行返回，不要输出任何其他信息，：" \
                 '返回值格式应该形如("2024-06-10", "天津", "哈尔滨")，如果输入的请求中缺乏信息，' \
                 '为该项填写"None"即可',
        input_variables=["UserMessage"]
    )
    Analysis_transportation = PromptTemplate(
        template="我想在从{departure_city}出发，前往{arrival_city}旅游。",
        input_variables=["departure_city", "arrival_city"]
    )
    REQ_location = PromptTemplate(
        template="现在用户在咨询交通方式，但用户缺少下面信息，你需要生成对用户的回复去请求这些信息：{missing_info}",
        input_variables=["missing_info"]
    )


class TravelAgent():
    def __init__(self, Tools, USE_Memory=None, USE_STREAM=True):
        self.openai_api_key = st.secrets["openai_api_key"]
        self.openai_base_url = st.secrets["openai_base_url"]
        self.memory = ConversationBufferMemory(memory_key=USE_Memory, return_message=True)
        self.tools = Tools
        chatllm = ChatOpenAI(model_name="qwen-plus", openai_api_key=self.openai_api_key,
                             base_url=self.openai_base_url, streaming=True)
        self.conversation_agent = initialize_agent(self.tools, chatllm,
                                                   agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                                                   memory=self.memory,
                                                   handle_parsing_errors=True,
                                                   verbose=True)


@tool("Transportation_train_query")
def transportation_train_query(input: str) -> list:
    """这个函数可以查询12306在某一天的所有火车车次信息，并返回一个列表
    这个函数的输入信息应该包括日期。出发地和目的地
    比如2024-07-01, 天津, 哈尔滨"""
    llmTrain = LLMChain(llm=ChatOpenAI(model_name="qwen-plus", openai_api_key=st.secrets["openai_api_key"],
                                       base_url=st.secrets["openai_base_url"]),
                        prompt=PromptsTemplateForTask.Analysis_location)
    match = re.search(r'\((.*?)\)', llmTrain.run(input))
    if match:
        # try:
        matched_string = match.group(1)
        travel_plan = eval(f"[{matched_string}]")
        data, start, dest = travel_plan
        # start, dest = use_jingwei(get_jingwei(start)[0]),use_jingwei(get_jingwei(dest)[0])
        tmp = mmy_12306(data, start, dest)
        if type(tmp) == str:
            return tmp
        print(type(tmp))
        return tmp
        # except Exception as e:
        #     return "查询失败，请检查输入信息"
    else:
        return "查询失败，请检查输入信息"


@tool("Transportation_walk_query")
def transportation_walk_query(input: str) -> tuple:
    """这个函数可以查询从从出发点到目的地步行的方向和时间，用于用户需要步行规划
    接受的输入应该是包含出发地和目的地"""
    llmTrain = LLMChain(llm=ChatOpenAI(model_name="qwen-plus", openai_api_key=st.secrets["openai_api_key"],
                                       base_url=st.secrets["openai_base_url"]),
                        prompt=PromptsTemplateForTask.Analysis_location)
    match = re.search(r'\((.*?)\)', llmTrain.run(input))
    if match:
        matched_string = match.group(1)
        travel_plan = eval(f"[{matched_string}]")
        data, start, dest = travel_plan
        start, dest = use_jingwei(get_jingwei(start)[0])['formatted_address'], use_jingwei(get_jingwei(dest)[0])[
            'formatted_address']
        instructions = []
        route = Lu_Jing(start, dest)

        for step in route.Bu_Xing()[0][0]['steps']:
            instructions.append(step['instruction'])
        return route.Bu_Xing()[0][0]['distance'], instructions
    else:
        return ()


@tool("Transportation_bus_query")
def transportation_bus_query(input: str) -> dict:
    """这个函数可以查询综合各类公共（公交、地铁）交通方式的通勤方案，并且返回通勤方案的数据。
    接受的输入应该是包含出发地和目的地"""
    llmTrain = LLMChain(llm=ChatOpenAI(model_name="qwen-plus", openai_api_key=st.secrets["openai_api_key"],
                                       base_url=st.secrets["openai_base_url"]),
                        prompt=PromptsTemplateForTask.Analysis_location)
    match = re.search(r'\((.*?)\)', llmTrain.run(input))
    if match:
        matched_string = match.group(1)
        travel_plan = eval(f"[{matched_string}]")
        data, start, dest = travel_plan
        start, dest = use_jingwei(get_jingwei(start)[0])['formatted_address'], use_jingwei(get_jingwei(dest)[0])[
            'formatted_address']
        route = Lu_Jing(start, dest)
        if route.Gong_Jiao() is not None:
            return route.Gong_Jiao()[0]
        else:
            return {}
    else:
        return {}


@tool("Transportation_car_query")
def transportation_car_query(input: str) -> dict:
    """这个函数可以查询驾车的通勤方案，并且返回通勤方案的数据。
    接受的输入应该是包含出发地和目的地"""
    llmTrain = LLMChain(llm=ChatOpenAI(model_name="qwen-plus", openai_api_key=st.secrets["openai_api_key"],
                                       base_url=st.secrets["openai_base_url"]),
                        prompt=PromptsTemplateForTask.Analysis_location)
    match = re.search(r'\((.*?)\)', llmTrain.run(input))
    if match:
        matched_string = match.group(1)
        travel_plan = eval(f"[{matched_string}]")
        data, start, dest = travel_plan
        start, dest = use_jingwei(get_jingwei(start)[0])['formatted_address'], use_jingwei(get_jingwei(dest)[0])[
            'formatted_address']
        route = Lu_Jing(start, dest)
        return route.Jia_Che()[0]
    else:
        return {}


@tool("accurate_address")
def accurate_address(input: str) -> list:
    """这个函数可以查询用户所说地址的模糊匹配,输入为一个比较模糊的地址，返回一个可选精确地址列表，需要在规划交通之前让用户进行筛选直到列表中只有一个精确地址，用于引导用户选择更为精确的地址"""
    return [use_jingwei(i)["formatted_address"] for i in get_jingwei(input)]


# @tool("F&Q")
# def faq(input: str) -> str:
#     """这个函数是和用户对话的总策略，每次遇到用户的消息时候应该第一时间调用这个函数获取策略，时刻按照这里的策略与用户进行对话"""
#     return "你是一个旅游助手，你应该回答各种关于旅游的问题" \
#            "你应该将用户的问题转化为任务，然后根据任务的描述，选择合适的工具完成任务：" \
#            "任务分为，交通方式建议和规划,美食和景点推荐,景点实时语音讲解,规划住宿，其余闲聊" \
#            "你应该根据工具的描述，选择合适的工具" \
#            "如果正在进行的某个任务需要更多的信息，你应该请求用户提供更多的信息"


if __name__ == '__main__':
    Tools = [
        DuckDuckGoSearchRun(name="Search"),
        transportation_train_query,
        faq,
    ]
    #     transportation_train_query,
    #     transportation_walk_query,
    #     transportation_bus_query,
    #     transportation_car_query,
    travel_agent = TravelAgent(Tools, "chat_history", True)
    ans = travel_agent.conversation_agent.run("你好，我想去哈尔滨")

    # while 1:
    #     print(ans)
    #     query = input("输入对话：")
    #     ans = travel_agent.conversation_agent.run(query)
    # # print(transportation_train_query("我想在2024年6月15日从天津到哈尔滨"))
