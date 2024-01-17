import streamlit as st
import random
import time
from character import OverallChain
from ft_character import OverallChain_ft
import os

def main():
    
    os.environ["OPENAI_API_KEY"] = st.secrets["openai_key"]
    
    st.title("캐릭터랑 대화하기")
    overall_chain = OverallChain_ft()
    
    # 대화 기록 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # 이전 대화 기록 보여 주기
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 사용자 인풋 받기
    if prompt := st.chat_input("캐릭터에게 할 말을 입력하세요."):
        # 사용자 입력 보여 주기
        st.session_state.messages.append({"role": "You", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 봇 대화 보여 주기
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            assistant_response = overall_chain.receive_chat(prompt)
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "캐릭터", "content": assistant_response})
    

if __name__ == "__main__":
    main()