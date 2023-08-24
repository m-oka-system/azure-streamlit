import os
import requests
import streamlit as st
from streamlit.web.server.websocket_headers import _get_websocket_headers

API_ENDPOINT = os.environ.get("API_ENDPOINT", "http://localhost:8000")

st.title('Streamlit app')
tab1, tab2 = st.tabs(["API Client", "Header list"])

with tab1:
    # 宛先APIの指定
    api_url = st.text_input('API URL', API_ENDPOINT)

    # Request Headersの設定
    st.subheader('Request Headers')
    content_type = st.text_input('Content-Type', 'application/json')
    authorization = st.text_input('Authorization', 'Bearer YOUR_TOKEN')  # 例: Bearer xxxxxx

    headers = {}
    if content_type:
        headers['Content-Type'] = content_type
    if authorization:
        headers['Authorization'] = authorization

    # POSTデータの設定
    st.subheader('POST Data (JSON format)')
    post_data = st.text_area('Input your JSON data here')

    # ボタンによるリクエストの実行
    if st.button('GET'):
        try:
            response = requests.get(api_url, headers=headers)
            st.write('Response:', response.json())
        except Exception as e:
            st.write('Error:', str(e))

    if st.button('POST'):
        try:
            response = requests.post(api_url, headers=headers, data=post_data)
            st.write('Response:', response.json())
        except Exception as e:
            st.write('Error:', str(e))

with tab2:
    headers = _get_websocket_headers()
    principal_name = headers.get("X-Ms-Client-Principal-Name")
    principal_id = headers.get("X-Ms-Client-Principal-Id")
    access_token = headers.get("X-Ms-Token-Aad-Access-Token")

    st.header("AzureAD's auth results")

    if principal_name is not None:
        st.markdown('X-Ms-Client-Principal-Name: ' + principal_name)
    if principal_id is not None:
        st.markdown('X-Ms-Client-Principal-Id: ' + principal_id)
    if access_token is not None:
        st.markdown('X-Ms-Token-Aad-Access-Token: ' + access_token)

    st.header('List http headers')
    if headers is not None:
        for key, value in headers.items():
            text = 'key={}, value={}'
            st.text(text.format(key, value))
