from situation import Character
import streamlit as st
import os
import json

def character_page(intro, story, line, situations, sit_line):
    st.title("캐릭터랑 대화하기")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": sit_line}]
    elif len(st.session_state.messages) == 1:
        st.session_state.messages = [{"role": "assistant", "content": sit_line}]
    
    for message in st.session_state.messages:
        st.chat_message(message["role"]).write(message["content"])
        
    chatbot = Character(intro, story, line, situations)
        
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            assistant_response = chatbot.receive_chat(prompt)
            message_placeholder.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})        

def main():
    os.environ["OPENAI_API_KEY"] = st.secrets["openai_key"]
    
    st.sidebar.title("캐릭터 선택")
    
    with open("sit_data/chars.json", "r", encoding="utf-8") as f:
        json_data = f.read()
    
    chars = json.loads(json_data)
    bots = [entry["bot"] for entry in chars]
    bots.insert(0, "선택")
    
    selected_char = st.sidebar.selectbox(
        "대화할 캐릭터를 선택하세요.",
        bots,
    )
    
    if selected_char != "선택":
        bot_data = next((entry for entry in chars if entry["bot"] == selected_char), None)
        situations = bot_data["situations"]
        sit_titles = [entry["sit_title"] for entry in situations]
        sit_titles.insert(0, "선택")
        
        selected_sit = st.sidebar.selectbox(
            "대화할 상황을 선택하세요.",
            sit_titles,
        )
        
        if selected_sit != "선택":
            sit_data = next((entry for entry in situations if entry["sit_title"] == selected_sit), None)
            sit_line = sit_data["sit_line"]
            
            intro = bot_data["intro"]
            story = bot_data["story"]
            line = bot_data["line"]
            situations = sit_data
            character_page(intro, story, line, situations, sit_line)

if __name__ == "__main__":
    main()
            
        
    
    
        