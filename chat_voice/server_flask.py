import streamlit as st
import requests


def get_ip():
    response = requests.get('https://api.ipify.org?format=json')
    return response.json()['ip']


ip = get_ip()
st.write(f"User IP: {ip}")
