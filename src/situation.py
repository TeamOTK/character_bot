import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, TransformChain, SequentialChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
import json


def get_memory(): # 대화 기록을 저장하는 메모리
    memory = ConversationBufferMemory(memory_key="chat_history", ai_prefix="bot", human_prefix="you")
    return memory

def get_search_chain(): # 인격을 지정하기 위해 데이터를 가져오는 코드
    def get_data(input_variables):
        chat = input_variables["chat"]
        with open("data/jyj_st.json", "r", encoding="utf8") as json_file:
            json_data = json_file.read()
    
        bot_data = json.loads(json_data)
        title = bot_data['title']
        bg = bot_data['bg']
        line = bot_data['line']
        
        with open("data/sjs_st.json", "r", encoding="utf8") as json_file:
            json_data = json_file.read()
        
        bot_data = json.loads(json_data)
        relation = bot_data['relation']
        situation = bot_data['situation']
        
        return {"title": title, "bg": bg, "line": line, "relation": relation, "situation": situation}
    
    search_chain = TransformChain(input_variables=["chat"], output_variables=["title", "bg", "line", "situation"], transform=get_data)
    return search_chain

def get_current_memory_chain(): # 현재 대화 기록을 가져오는 코드
    def transform_memory_func(input_variables):
        current_chat_history = input_variables["chat_history"].split("\n")[-10:]
        current_chat_history = "\n".join(current_chat_history)
        return{"current_chat_history": current_chat_history}
    
    current_memory_chain = TransformChain(input_variables=["chat_history"], output_variables=["current_chat_history"], transform=transform_memory_func)
    return current_memory_chain

def get_chatgpt_chain(): # GPT-4를 사용하여 대화를 생성하는 코드
    llm = ChatOpenAI(model_name="gpt-4", openai_api_key=os.environ["OPENAI_API_KEY"])
    
    template = """ 너는 'bot2'가 말을 했을 때, 'bot1'이 상황에 맞춰서 대답하는 것처럼 대화를 해 줘.
    
    'bot1'은 대체적으로 이런 인물이야. 이 문서를 참고하면 돼. {title}
    'bot1'의 성격, 인물 배경은 이 문서를 참고해. {bg}
    'bot1' 대사의 예시를 보여 줄 테니까, 'bot1'의 말과 습관, 생각을 잘 유추해 봐
    Examples: {line}
    'bot1'과 'bot2'는 현재 이런 상황이야. {situation}
    
    위에서 참고한 각 문서를 읽고 나서, 상황에 맞춰서 "bot1'의 말투와 성격을 잘 따라해 줘.
    다음 대화에서 'bot1'이 할 것 같은 답변을 해 봐.
    1. 'bot1'의 스타일대로, 'bot1'이 이 상황에서 할 것 같은 말을 해야 해.
    2. 자연스럽게 'bot1'의 말투와 성격을 따라해야 해. 번역한 것 같은 말투를 사용하지 마.
    3. 다섯 문장 이내로 짧게 대답하되, 'bot2'와 대화가 이어질 수 있도록 자연스럽게 말해 줘.
    4. 'bot1'의 성격, 인물 배경을 제대로 반영해 줘. 없는 말 지어내지 마.
    5. 주어진 상황에 맞춰서, 'bot2'한테 할 만한 말을 해 줘.
    6. 'bot2'의 말을 따라하지 마. 'bot1'의 말을 해 줘.
    
    이전 대화:
    {current_chat_history}
    bot2: {chat}
    bot1: 
    """
    
    prompt_template = PromptTemplate(input_variables=["chat", "current_chat_history", "line", "bg", "title", "situation"], template=template)
    chatgpt_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="received_chat")
    
    return chatgpt_chain

class OverallChain_st:
    def __init__(self) -> None:
        self.memory = get_memory()
        self.search_chain = get_search_chain()
        self.current_memory_chain = get_current_memory_chain()
        self.chatgpt_chain = get_chatgpt_chain()
        
        self.overall_chain = SequentialChain(
            memory=self.memory,
            chains=[self.search_chain, self.current_memory_chain, self.chatgpt_chain],
            input_variables=["chat"],
            output_variables=["received_chat"],
            verbose=True
        )
    
    def receive_chat(self, chat):
        review = self.overall_chain.invoke({"chat": chat})
        return review['received_chat']

def main() -> None:
    overall_chain = OverallChain_st()
    
    while True:
        received_chat = input("You: ")
        overall_chain.receive_chat(received_chat)
        print(overall_chain.memory.load_memory_variables({})['chat_history'])

if __name__ == "__main__":
    main() 