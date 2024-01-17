import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, TransformChain, SequentialChain
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
        with open("data/jyj.json", "r", encoding="utf8") as json_file:
            json_data = json_file.read()
    
        bot_data = json.loads(json_data)
        title = bot_data['title']
        bg = bot_data['bg']
        story = bot_data['story']
        line = bot_data['line']
        
        return {"title": title, "bg": bg, "story": story, "line": line}
    
    search_chain = TransformChain(input_variables=["chat"], output_variables=["title", "bg", "story", "line"], transform=get_data)
    return search_chain

def get_current_memory_chain(): # 현재 대화 기록을 가져오는 코드
    def transform_memory_func(input_variables):
        current_chat_history = input_variables["chat_history"].split("\n")[-10:]
        current_chat_history = "\n".join(current_chat_history)
        return{"current_chat_history": current_chat_history}
    
    current_memory_chain = TransformChain(input_variables=["chat_history"], output_variables=["current_chat_history"], transform=transform_memory_func)
    return current_memory_chain

def get_chatgpt_chain(): # 파인튜닝된 GPT-3.5를 사용하여 대화를 생성하는 코드
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.environ["OPENAI_API_KEY"])
    
    template = """
    SYSTEM: You('bot') are a chatbot who imitates a character and talks to the user('You').

    The character's characteristics are like this. {title}
    The character's introduction, personality, character background, and action are like this. {bg}, {story}
    Use examples of character lines to infer the words, habits, and thoughts of the character.
    Examples: {line}

    After reading the document above, give the answer that the character will likely do in the next conversation.
    1. In the style of the character, you have to say something that the character would say.
    2. You should naturally imitate the way the character talks and personality of the character. Don't use a translated tone, but answer in Korean.
    3. Don't make the user's words continuously, just give the character's words as a result.
    4. Please give me a short answer within three sentences.
    5. Please properly reflect the character's personality, character background, and actions. Don't make things up that you don't have.
    6. Don't say exactly same sentence with {line} that are provided as examples. Try to use a similar tone and talk with user naturally. 

    Previous conversation:
    {current_chat_history}
    You: {chat}
    bot: 
    """
    
    prompt_template = PromptTemplate(input_variables=["chat", "current_chat_history", "line", "bg",  "story", "title"], template=template)
    chatgpt_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="received_chat")
    
    return chatgpt_chain

class OverallChain_ft:
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
    overall_chain = OverallChain_ft()
    
    while True:
        received_chat = input("You: ")
        overall_chain.receive_chat(received_chat)
        print(overall_chain.memory.load_memory_variables({})['chat_history'])

if __name__ == "__main__":
    main() 