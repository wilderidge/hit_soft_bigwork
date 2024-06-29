import streamlit as st
from streamlit_option_menu import option_menu
from chatbot.chat_with_ass import Chatbot
from torchMap.Map_location import click_map_get_location, show_map_polyline
from TaskManager.TaskManager import Task_Manager
from chat_voice.my_gtts import gtts_text2sound
import pandas as pd
from torchMap.Gode_MAP import Tian_Qi, Get_jingdian
from datetime import datetime
import os
import re

st.set_page_config(layout="wide")


@st.experimental_dialog("驿演丁真可以做些什么？")
def show_task_detail():
    st.markdown("#### 1.在左边聊天框告诉丁真你想从哪里出发？走向哪里？")
    st.caption("*因为你不在理塘，丁真不会用小马驹载你*")
    st.caption("*你也可以用神秘妙妙工具中的地图规划功能进行选择*")
    st.markdown('#### 2.问问丁真目的地有哪些旅游景点和美食特产')
    st.caption('*理塘的特产是瑞克五代*')
    st.markdown("#### 3.导游丁真亲自为你讲解")
    st.caption('*在聊天框中召唤丁真，聆听丁真原声电音*')
    st.markdown('#### 4.丁真觉得出门在外你需要随时注意天气')
    st.caption("*雪豹不喜欢自己的毛被沾湿*")
    city_list = list(st.session_state["city_data_csv"]["地级市"].unique())
    city_select = st.selectbox("当前城市", city_list, index=city_list.index("哈尔滨市"))

    if st.button("确认你的方向，雪豹会一直陪着你！"):
        if city_select != st.session_state["city_weather"]["city_name"]:
            st.session_state["city_weather"] = analyse_city_weather(city_select)
        st.rerun()


def analyse_city_weather(city):
    my_TQ = Tian_Qi(city)
    data = my_TQ.get_tianqi_pre()
    dates = []
    day_weathers = []
    night_weathers = []
    day_temperatures = []
    night_temperatures = []
    day_wind_directions = []
    day_wind_powers = []
    night_wind_directions = []
    night_wind_powers = []

    # 遍历casts列表
    for cast in data[0]['casts']:
        # 添加到列表
        dates.append(cast['date'])
        day_weathers.append(cast['dayweather'])
        night_weathers.append(cast['nightweather'])
        day_temperatures.append(cast['daytemp'])
        night_temperatures.append(cast['nighttemp'])
        day_wind_directions.append(cast['daywind'])
        day_wind_powers.append(cast['daypower'])
        night_wind_directions.append(cast['nightwind'])
        night_wind_powers.append(cast['nightpower'])
    weather = {"city_name": city, "dates": dates, "day_weathers": day_weathers, "night_weathers": night_weathers,
               "day_temperatures": day_temperatures, "night_temperatures": night_temperatures,
               "day_wind_directions": day_wind_directions, "day_wind_powers": day_wind_powers,
               "night_wind_directions": night_wind_directions, "night_wind_powers": night_wind_powers}
    return weather


@st.experimental_fragment
def weather_slider():
    weather, chose_day = st.columns((3, 1))
    with chose_day:
        day = st.date_input(
            "出行前记得查看天气哦",
            datetime.strptime(st.session_state["city_weather"]["dates"][0], "%Y-%m-%d"),
            min_value=datetime.strptime(st.session_state["city_weather"]["dates"][0], "%Y-%m-%d"),
            max_value=datetime.strptime(st.session_state["city_weather"]["dates"][-1], "%Y-%m-%d"),
            format="YYYY-MM-DD"
        )

    # 找到 day对应的index
    index = st.session_state["city_weather"]["dates"].index(str(day))
    with weather:
        weather_srt, Temperature, Wind_day, Wind_night = st.columns(4)
        weather_srt.markdown(f"###### 白天：{st.session_state['city_weather']['day_weathers'][index]}")
        weather_srt.markdown(f"###### 夜晚：{st.session_state['city_weather']['night_weathers'][index]}")
        delta_T = float(st.session_state["city_weather"]["night_temperatures"][index]) - \
                  float(st.session_state["city_weather"]["day_temperatures"][index])
        Temperature.metric("Temperature", f"{st.session_state['city_weather']['day_temperatures'][index]}°C",
                           f"{delta_T}°C")
        Wind_day.metric(f"Wind_day:{st.session_state['city_weather']['day_wind_directions'][index]}",
                        f"{st.session_state['city_weather']['night_wind_powers'][index]}")
        Wind_night.metric(f"Wind_night:{st.session_state['city_weather']['night_wind_directions'][index]}",
                          f"{st.session_state['city_weather']['night_wind_powers'][index]}")


if "city_data_csv" not in st.session_state:
    st.session_state["city_data_csv"] = pd.read_csv('data/china_cities.csv')
if "tasklist" not in st.session_state:
    st.session_state["tasklist"] = Task_Manager()
    st.session_state["task_refresh"] = False
if "spots_locate" not in st.session_state:
    st.session_state["spots_locate"] = {}
if "city_weather" not in st.session_state:
    st.session_state["city_weather"] = analyse_city_weather("哈尔滨市")
with st.sidebar:
    st.logo("logo.png")
    if "chatbot" not in st.session_state:
        st.session_state["chatbot"] = Chatbot()
    Chat_box = st.session_state["chatbot"]
    Chat_box.show_history()
    if prompt := st.chat_input(placeholder="芝士雪豹⛷"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        Chat_box.chat(prompt)

# Menu_function

weather_slider()
selected = option_menu(None, ['Start', "丁真激情语音", "向导地图", "任务列表"],
                       icons=['house', 'cloud-upload', "list-task", 'gear'],
                       key='menu', default_index=0, orientation="horizontal")
if st.session_state["menu"] == "向导地图":
    if "star_point" not in st.session_state or "dest_point" not in st.session_state:
        click_map_get_location()
    else:
        show_map_polyline()
        if st.button("重新选择"):
            st.session_state.pop('star_point', None)
            st.session_state.pop('dest_point', None)
if st.session_state["menu"] == "任务列表":
    st.header("这里是你的旅游小助手，驿演丁真，你可以在左侧栏和丁真聊天", divider="rainbow")
    st.markdown("*丁真小助手会把你话中的任务进行归档管理并展示在任务栏中，快说，谢谢雪豹*")
    st.divider()
    if st.button("更新任务列表"):
        with st.spinner('Wait for loading...'):
            st.session_state["tasklist"].refresh()
            st.session_state["task_refresh"] = True
        st.session_state["tasklist"].show_task_list()
        print(st.session_state["tasklist"].tasks)
    elif st.session_state["task_refresh"]:
        st.session_state["tasklist"].show_task_list()

if st.session_state["menu"] == "Start":
    st.header("雪豹TV首席导游-驿演丁真", divider="rainbow")
    col1, col2 = st.columns(2)
    with col1:
        st.image("logo.png", width=400, caption="雪豹TV首席导游-驿演丁真")
    with col2:
        st.write("##### 你好，我是你的旅游向导丁真，虽然你现在不在理塘，但人间处处是理塘")
        st.write("##### 雪豹是多才多艺的，你可以和我边抽瑞克五代边聊")
        st.write("##### 你可以在左侧聊天框和我聊天，我会帮你逐步制定一个完美的旅行计划")
        st.write("##### 现在开始吧，让我们骑着小马驹出发吧")
        st.divider()
        if st.button("雪豹才艺展示"):
            show_task_detail()

if st.session_state["menu"] == "丁真激情语音":
    st.header("丁真激情语音", divider="rainbow")
    st.markdown("*你可以在这里召唤丁真，让丁真为你讲解当地的风土人情*")

    province, city, spots = st.columns(3)
    with province:
        city_data = st.session_state["city_data_csv"]
        provinces = city_data['所属省份'].unique()
        selected_province = st.selectbox('选择你的省份', provinces)

    with city:
        cities = city_data[city_data['所属省份'] == selected_province]['地级市'].unique()
        selected_city = st.selectbox('选择你的地级市', cities)

    with spots:
        if selected_city not in st.session_state["spots_locate"]:
            st.session_state["spots_locate"][selected_city] = Get_jingdian(selected_city)
        spots = st.session_state["spots_locate"][selected_city]
        spot_names = [spot['name'] for spot in spots]
        selected_spot_name = st.selectbox('选择你想了解的景点', spot_names)
    # 显示选择的省份和地级市
    if st.button("召唤丁真"):

        selected_spot = next(spot for spot in spots if spot['name'] == selected_spot_name)
        for photo in selected_spot['photos']:
            st.image(photo['url'], use_column_width=True)
        print(os.listdir("data/audio"))
        if f"{selected_spot_name}.mp3" not in os.listdir("data/audio"):
            st.session_state.messages.append(
                {"role": "user", "content": f"我想知道{selected_spot_name}的旅游景点的介绍"})
            prompt =  f"生成一段{selected_city}{selected_spot_name}的旅游景点的介绍导游词，不要超过八十字"
            print(prompt)
            Chat_box.chat(prompt)
            audio_text = st.session_state.messages[-1]["content"]
            audio_text = re.sub(r'\*+', '', audio_text)
            with st.spinner('Wait for generate audio...'):
                gtts_text2sound(audio_text, f"data/audio/{selected_spot_name}.mp3", 1)
            st.audio(f"data/audio/{selected_spot_name}.mp3", format='audio/mp3', start_time=0)
        else:
            st.audio(f"data/audio/{selected_spot_name}.mp3", format='audio/mp3', start_time=0)
