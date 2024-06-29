import streamlit as st

from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from Travel_Agent import *

prompt = """你是一个旅游助手，你应该回答各种关于旅游的问题 
           你应该将用户的问题转化为任务，然后根据任务的描述，选择合适的工具完成任务：
           任务分为，交通方式建议和规划,美食和景点推荐,景点实时语音讲解,规划住宿，其余闲聊" 
           你应该根据工具的描述，选择合适的工具" 
           如果正在进行的某个任务需要更多的信息，你应该请求用户提供更多的信息" 
           1.关于交通方式建议和规划，你应该引导用户选择出发地和目的地，并对出发地和目的地进行accurate_address tool 的确认(火车不需要这一步)，你应该根据用户的出发地和目的地的远近，引导用户选择合适的交通方式
           2.关于美食和景点推荐，你应该根据用户的目的地，推荐当地的美食和景点
           3.关于景点实时语音讲解，你应该在用户提出需要语音讲解时候，用search tool查找资料并生成回复
           你应该尽可能引导用户向上面的任务靠拢，而不是闲聊"""


class Chatbot:
    def __init__(self):
        # st.logo("logo.png")
        st.title("旅行向导-丁真")
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": prompt},
                {"role": "assistant", "content": "你好，我是你的旅游助手"}
            ]
        Tools = [
            DuckDuckGoSearchRun(name="Search"),
            transportation_train_query,
            transportation_train_query,
            transportation_walk_query,
            transportation_bus_query,
            transportation_car_query,
            accurate_address
        ]
        self.search_agent = TravelAgent(Tools, "chat_history", True)
        self.search_agent.conversation_agent.run(prompt)
        st.session_state.messages.append({"role": "assistant", "content": prompt})

    def show_history(self):
        for msg in st.session_state.messages:
            if msg["content"] != prompt:
                st.chat_message(msg["role"]).write(msg["content"])

    def chat(self, user_input):
        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = self.search_agent.conversation_agent.run(st.session_state.messages, callbacks=[st_cb])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
