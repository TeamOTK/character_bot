import streamlit as st
import random
import time
from character import OverallChain
from ft_character import OverallChain_ft
import os

def display_chat_message(profile_image_url, sender_name, message, role):
    st.markdown(
        f'<div style="display: flex; align-items: center;">'
        f'<img src="{profile_image_url}" style="border-radius: 50%; width: 30px; height: 30px; margin-right: 10px;">'
        f'<b>{sender_name}:</b> {message}'
        f'</div><br>',
        unsafe_allow_html=True
    )

def main():
    
    os.environ["OPENAI_API_KEY"] = st.secrets["openai_key"]
    
    st.title("전영중 채팅방")
    overall_chain = OverallChain_ft()
    
    # 대화 기록 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # 이전 대화 기록 보여 주기
    for message in st.session_state.messages:
        display_chat_message(message["profile_image"], message["sender_name"], message["content"], message["role"])
    
    # 사용자 인풋 받기
    if prompt := st.chat_input("캐릭터에게 할 말을 입력하세요."):
        # 사용자 입력 보여 주기
        st.session_state.messages.append({
            "role": "You", 
            "content": prompt, 
            "profile_image": "https://i.pinimg.com/564x/3f/ae/66/3fae66cb5f433d025def6a280b91bb19.jpg", 
            "sender_name": "나"})
        display_chat_message("https://i.pinimg.com/564x/3f/ae/66/3fae66cb5f433d025def6a280b91bb19.jpg", "나", prompt, "You")

        # 봇 대화 보여 주기
        assistant_response = overall_chain.receive_chat(prompt)
        st.session_state.messages.append({
            "role": "캐릭터",
            "content": assistant_response,
            "profile_image": "https://i.namu.wiki/i/JMgll0WHNbzp4ByuSeT0ZwrM1FehI36hqOIrfDyTTJeYhE10zpNAJ58Jm-bEUHLVT9sBObL5d8sDO5dkEyyv1pDSgYR492c4YrlGpBwxE1Fxvg65ph8oEmCdG3wmiryDG0LjRyGVbYSOCFvXc45g4A.webp",
            "sender_name": "전영중"})
        display_chat_message("https://i.namu.wiki/i/JMgll0WHNbzp4ByuSeT0ZwrM1FehI36hqOIrfDyTTJeYhE10zpNAJ58Jm-bEUHLVT9sBObL5d8sDO5dkEyyv1pDSgYR492c4YrlGpBwxE1Fxvg65ph8oEmCdG3wmiryDG0LjRyGVbYSOCFvXc45g4A.webp", "전영중", assistant_response, "assistant")
    

if __name__ == "__main__":
    main()