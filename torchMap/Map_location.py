import folium
import streamlit as st
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
from torchMap.Gode_MAP import use_jingwei
from torchMap.Gode_MAP import Lu_Jing


# 创建 Streamlit 应用
@st.cache_data
def get_route(star_point, dest_point, city=None):
    instructions = []
    coordinates = []
    route = Lu_Jing(star_point, dest_point, city)
    for step in route.Bu_Xing()[0][0]['steps']:
        locations = step['polyline'].split(';')
        for location in locations:
            lng, lat = map(float, location.strip().split(','))
            coordinates.append([lat, lng])
        instructions.append(step['instruction'])
    return route.Bu_Xing()[0][0]['distance'], instructions, coordinates


def show_map():
    # 创建 Folium 地图
    folium_map = folium.Map(location=[45.743215, 126.632628],
                            tiles='https://webrd02.is.autonavi.com/appmaptile?lang=zh_en&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
                            attr='高德-中英文对照',
                            zoom_start=16)
    # folium.Marker([45.743215, 126.632628], popup='起始点：你将从这里出发',
    #               icon=folium.Icon(color='blue', icon='cloud')).add_to(folium_map)
    if "star_point" in st.session_state:
        folium.Marker(st.session_state["star_point"]["location"], popup='起始点：你将从这里出发',
                      icon=folium.Icon(color='blue', icon='cloud')).add_to(folium_map)
        st.write("你选择的出发点是：", st.session_state["star_point"]["name"])
    if "dest_point" in st.session_state:
        folium.Marker(st.session_state["dest_point"]["location"], popup='终点：你将到达这里',
                      icon=folium.Icon(color='blue', icon='cloud')).add_to(folium_map)
        st.write("你选择的目的地是：", st.session_state["dest_point"]["name"])
    # 在 Streamlit 中显示 Folium 地图
    st_folium(folium_map, width=1500, height=600)


def click_map_get_location():
    st.markdown('#### 你可以直接点击地图告诉丁真你的出发点和目的地，丁真会帮你规划路线')
    folium_map = folium.Map(location=[45.743215, 126.632628],
                            tiles='https://webrd02.is.autonavi.com/appmaptile?lang=zh_en&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
                            attr='高德-中英文对照',
                            zoom_start=16)
    folium_map.add_child(folium.ClickForMarker(popup='Waypoint'))
    # if "star_point" in st.session_state:
    #     folium.Marker(st.session_state["star_point"]["location"], popup='起始点：你将从这里出发').add_to(folium_map)
    # if "dest_point" in st.session_state:
    #     folium.Marker(st.session_state["dest_point"]["location"], popup='终点：你将到达这里').add_to(folium_map)
    output = st_folium(folium_map, width=1500, height=600)
    if output['last_clicked']:
        click_location = [output['last_clicked']['lng'], output['last_clicked']['lat']]
        location_name = use_jingwei(','.join(map(str, click_location)))["formatted_address"]
        click_location = [output['last_clicked']['lat'], output['last_clicked']['lng']]
        if "star_point" not in st.session_state:
            st.write("你选择的出发点是：", location_name)
            if st.button("确认"):
                st.session_state['star_point'] = {"name": location_name, "location": click_location}
                st.rerun()
        elif "dest_point" not in st.session_state:
            st.write("你选择的目的地是：", location_name)
            if st.button("确认"):
                st.session_state['dest_point'] = {"name": location_name, "location": click_location}
                st.rerun()
        if st.button("重新选择"):
            st.session_state.pop('star_point', None)
            st.session_state.pop('dest_point', None)
            st.rerun()


def show_map_polyline():
    # 创建 Folium 地图
    folium_map = folium.Map(location=[45.743215, 126.632628],
                            tiles='https://webrd02.is.autonavi.com/appmaptile?lang=zh_en&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
                            attr='高德-中英文对照',
                            zoom_start=16)
    # folium.Marker([45.743215, 126.632628], popup='起始点：你将从这里出发',
    #               icon=folium.Icon(color='blue', icon='cloud')).add_to(folium_map)
    if "star_point" in st.session_state:
        folium.Marker(st.session_state["star_point"]["location"], popup='起始点：你将从这里出发',
                      icon=folium.Icon(color='blue', icon='cloud')).add_to(folium_map)
        st.write("你选择的出发点是：", st.session_state["star_point"]["name"])
    if "dest_point" in st.session_state:
        folium.Marker(st.session_state["dest_point"]["location"], popup='终点：你将到达这里',
                      icon=folium.Icon(color='blue', icon='cloud')).add_to(folium_map)
        st.write("你选择的目的地是：", st.session_state["dest_point"]["name"])
    # 在 Streamlit 中显示 Folium 地图
    st_folium(folium_map, width=1500, height=600)
    # 画线
    with st.spinner('Wait for it...'):
        distance, instructions, coordinates = get_route(st.session_state["star_point"]["name"],
                                                        st.session_state["dest_point"]["name"])
    folium.PolyLine(
        locations=coordinates,
        color='blue',
        weight=5,
        opacity=0.8
    ).add_to(folium_map)
    distance = round(float(distance) / 1000, 2)
    st.write(f"总路程：{distance}km")
    st.write("路线规划：")
    for i, instruction in enumerate(instructions):
        st.write(f"{i + 1}. {instruction}")

    st_folium(folium_map, width=1500, height=600)


if __name__ == '__main__':
    click_map_get_location()
