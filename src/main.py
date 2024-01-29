import streamlit as st
import random
import time
from character import OverallChain
from ft_character import OverallChain_ft
from situation import OverallChain_st
import os

def display_chat_message(profile_image_url, sender_name, message, role):
    st.markdown(
        f'<div style="display: flex; align-items: center;">'
        f'<img src="{profile_image_url}" style="border-radius: 50%; width: 30px; height: 30px; margin-right: 10px;">'
        f'{message}'
        f'</div><br>',
        unsafe_allow_html=True
    )

def main():
    
    os.environ["OPENAI_API_KEY"] = st.secrets["openai_key"]
    
    st.title("전영중")
    st.subheader("전영중도 성준수를 따라 지상고로 전학하는 것을 선택한 상황")
    overall_chain = OverallChain_st()
    
    # 대화 기록 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # 이전 대화 기록 보여 주기
    for message in st.session_state.messages:
        display_chat_message(message["profile_image"], message["sender_name"], message["content"], message["role"])
    
    # 사용자 인풋 받기
    if prompt := st.chat_input("캐릭터에게 할 말을 입력하세요. 예: 너도 지상고로 간다고?"):
        # 사용자 입력 보여 주기
        st.session_state.messages.append({
            "role": "You", 
            "content": prompt, 
            "profile_image": "https://i.namu.wiki/i/QO-yP3Gfzf9APikLUAfx6qkGgC91EJIHsKiE4F1JxFo3BMyvt4VhuDkfiF4LcAWToP_B3RONBiu9zoguuaZj3Q.webp", 
            "sender_name": "성준수"})
        display_chat_message("https://i.namu.wiki/i/QO-yP3Gfzf9APikLUAfx6qkGgC91EJIHsKiE4F1JxFo3BMyvt4VhuDkfiF4LcAWToP_B3RONBiu9zoguuaZj3Q.webp", "성준수", prompt, "You")

        # 봇 대화 보여 주기
        assistant_response = overall_chain.receive_chat(prompt)
        st.session_state.messages.append({
            "role": "캐릭터",
            "content": assistant_response,
            "profile_image": "https://i.namu.wiki/i/ntOmy9_HyR4LJQaZ9BKM8kQvVMHQXjQRCdVwFCOhIBEpBPbwbjC__xPh5NRUxSzgD7mmV5V59tG-1d0jWEQXrw.webp",
            "sender_name": "전영중"})
        display_chat_message("https://i.namu.wiki/i/ntOmy9_HyR4LJQaZ9BKM8kQvVMHQXjQRCdVwFCOhIBEpBPbwbjC__xPh5NRUxSzgD7mmV5V59tG-1d0jWEQXrw.webp", "전영중", assistant_response, "assistant")
    

if __name__ == "__main__":
    main()