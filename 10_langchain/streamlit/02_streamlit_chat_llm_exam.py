from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st

@st.cache_resource
def get_model():
    # OpenAI GPT 모델 연동
    load_dotenv()
    return ChatOpenAI(model="gpt-5-mini")

@st.cache_resource
def get_prompt_teamplate():
    prompt = ChatPromptTemplate(
        [
            {"role":"system", "content":"당신은 유능한 인공지능 Assistant입니다."},
            MessagesPlaceholder("history"),
            {"role":"user","content":"{query}"}
        ]
    )
    return prompt

model = get_model()
prompt = get_prompt_teamplate()


if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []


st.title("Chatbot Service")

user_input = st.chat_input("User:")
if user_input:
    # AI에게 요청
    ## prompt template 이용해서 prompt 완성
    query = prompt.invoke({
        "query" : user_input, # 질문
        "history" : st.session_state['chat_history'] #대화 내역
    })
    ## prompt를 model에 넣어서 답변을 요청
    response = model.invoke(query)

    ## 질문과 답변을 session_state에 추가
    # 사용자 질문
    st.session_state['chat_history'].append(
        {"role":"user", "content":user_input}
    )

    # AI 답변 response : AIMessage 타입. content 속성으로 조회.
    st. session_state['chat_history'].append(
        {"role":"ai", "content":response.content}
    )
###################
# 출력 - session_state 저장된 대화내역을 chat_message()를 이용해 출력.

for chat_dict in st.session_state['chat_history']:
    with st.chat_message(chat_dict['role']):
        st.write(chat_dict['content'])

