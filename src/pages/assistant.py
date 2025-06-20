# 🤖 LLM Assistant Page Logic

import streamlit as st
from agent.legal_agent import get_legal_answer

def render():
    st.title("AI Legal Assistant")
    st.markdown(
        "Ask questions about redlining, heirs’ property, title issues, or housing justice."
    )

    user_input = st.text_input("Ask me anything:")

    if user_input:
        st.write(f"🔍 You asked: {user_input}")
        with st.spinner("Thinking..."):
            try:
                answer = get_legal_answer(user_input)
                st.markdown(answer)
            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
