import streamlit as st
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
import requests


# 获取用户访问的IP地址
def get_remote_ip() -> str:
    """Get remote ip."""
    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None
    return session_info.request.remote_ip


def get_location(ip):
    try:
        response = requests.get(f'http://ipinfo.io/{ip}/json')
        data = response.json()

        if 'error' in data:
            return f"Error: {data['error']['message']}"

        location = {
            'IP': data.get('ip'),
            'City': data.get('city'),
            'Region': data.get('region'),
            'Country': data.get('country'),
            'Location': data.get('loc'),
            'Organization': data.get('org'),
            'Timezone': data.get('timezone')
        }

        return location

    except Exception as e:
        return f"Error: {str(e)}"


#get_remote_ip()
# 示例IP地址
# ip_address = "206.237.0.215"
# location_info = get_location(ip_address)
#
# st.write(location_info)


def page1():
    st.write(st.session_state.foo)


def page2():
    st.write(st.session_state.bar)


# Widgets shared by all the pages
st.sidebar.selectbox("Foo", ["A", "B", "C"], key="foo")
st.sidebar.checkbox("Bar", key="bar")

pg = st.navigation([st.Page(page1), st.Page(page2)])
pg.run()
