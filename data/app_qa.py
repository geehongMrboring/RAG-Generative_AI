import time
from rag import RagService
import streamlit as st
import config_data as config

st.title("Knowledge Base Q&A Service")
st.divider()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello, I am the Knowledge Base Q&A Service"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.spinner("Answering..."):
        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)
        full_response = st.chat_message("assistant").write_stream(res_stream)
        st.session_state["messages"].append({"role": "assistant", "content": full_response})