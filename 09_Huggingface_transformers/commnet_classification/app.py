# huggingface transformers.pipeline을 이용해서 한국어를 영어로 번역하는 app를 제작


import streamlit as st
from transformers import pipeline

# 처음 시작할 때 한번 실행하고 반환되는 리소스를 메모리에 저장해 놓고, 다음부터는 그것을 사용하겠다. 는 뜻!
@st.cache_resource
def get_model() :
    model = "Copycats/koelectra-base-v3-generalized-sentiment-analysis"
    pipe = pipeline(task = "text-classification", model=model)
    return pipe

classifier = get_model()

def classify_and_clear():
    # print(f'classify_and_clear() ------------ {st.session_state['input_text']}')
    # pipeline을 이용해서 입력된 댓글을 분류
    comment = st.session_state['input_text']
    if comment.strip():
        result = classifier(comment)[0]
        label = "긍정적 댓글" if result['label']=='1' else "부정적 댓글"
        score = result['score']
        # st.session_state의 history에 추가
        st.session_state['history'].append((comment,f"{label}-{score:.3f}"))
    # 댓글 입력 폼 지우기
    st.session_state['input_text'] = ''


if "history" not in st.session_state :
    st.session_state.history = [] #[(댓글1, 긍부정 분류1), (댓글2, 긍부정 분류2)]
# 긍부정 분류한 내역을 저장할 session_state를 생성
# 어떤 값들을 꼐속 유지해야 할 때 저장하는 공간(dict 타입) : session_state

st.title("댓글 분석기")
st.subheader("댓글의 내용이 긍정적인지 부정적인지 분류합니다.")

st.text_input(
    "분석할 댓글을 입력하세요.",
    on_change=classify_and_clear,
    key= "input_text" # session_state에 지정한 key로 등록되고 값은 입력폼의 value가 저장되어 동기화된다.
    # session_state값을 변경하면 입력 폼의 값이 변경되고 반대도 마찬가지! 
)
# on_change : event hanlder(어떤 변화가 발생하면 함수를 호출.) 
# → text 입력 폼에 값이 바뀌고 엔터가 입력되면 함수를 호출.


st.button("분석", on_click=classify_and_clear) # on_click : 마우스 클릭하면 함수 호출


# 댓글 분석 결과 출력
if st.session_state['history'] : 
    st.subheader("분석 결과")
    for comment, result in st.session_state['history'][::-1] : #[::-1] = 최신것부터 보겠다는 뜻.
        st.write(comment)
        st.write(result)
        st.write("---")