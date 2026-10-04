from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

# load env variables
load_dotenv()

st.set_page_config(
    page_title="ChatBot",
    page_icon="🤖",
    layout="centered"
)


st.title("💬 Generative AI ChatBot")

with st.sidebar:
    st.title("Settings")

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# initiate chat history

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# show chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# llm initiate
llm = ChatGroq(
    model = "openai/gpt-oss-20b",
    temperature = 0.0,
)
# input box
user_prompt = st.chat_input("Ask ChatBot ...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role":"user","content":user_prompt})
    # for sudden response
    response = llm.invoke(
        input = [{"role":"system","content":"You are a helpful assistant"},*st.session_state.chat_history]
    )

    # for streaming
#     messages = [
#     {"role": "system", "content": "You are a helpful assistant"},
#     *st.session_state.chat_history
# ]
#     response = llm.stream(messages)

#     with st.chat_message("assistant"):
#         assistant_response = st.write_stream(
#             chunk.content for chunk in response
#         )


    assistant_response = response.content
    st.session_state.chat_history.append({"role":"assistant","content":assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)