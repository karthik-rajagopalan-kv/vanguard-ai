import streamlit as st
from agent import agent_executor
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.chat_history import InMemoryChatMessageHistory


def new_chat():
    if "init" not in st.session_state:
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.message_history = []

        st.session_state.messages[:] = []
        st.session_state.message_history[:] = []
        st.session_state.init = True


def generate_chat(prompt: str = None):
    result = agent_executor.invoke(
        {
            "input": prompt,
            "chat_history": InMemoryChatMessageHistory(messages=st.session_state.message_history).messages,
        }
    )
    return result["output"]


new_chat()

st.title("Chat")

# with st.sidebar:
#     st.button("Start new chat", on_click=st.rerun())

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter Input"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.message_history.append(HumanMessage(content=prompt))

    with st.spinner("Please Wait!"):
        message = generate_chat(prompt=prompt)

    with st.chat_message("assistant"):
        st.markdown(message)
        st.session_state.messages.append({"role": "assistant", "content": message})
        st.session_state.message_history.append(AIMessage(content=message))
