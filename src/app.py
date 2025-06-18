import streamlit as st

st.set_page_config(page_title="Redline Revealer", layout="wide")

st.title("🏙️ Redline Revealer")
st.markdown("Unearthing the past. Protecting the future.")

tab1, tab2, tab3, tab4 = st.tabs([
    "👋 Welcome", 
    "📍 Redlining Map", 
    "🧠 LLM Assistant", 
    "💖 About Us"
])

with tab1:
    st.subheader("Welcome to Redline Revealer")
    st.info(
        "Learn more about the project and purpose here."
    )

with tab2:
    st.subheader("Historical Redlining Visualization")
    st.info("Map overlay and risk scoring will appear here.")

with tab3:
    st.subheader("AI Legal Assistant")
    st.info(
        "Ask questions about heirs’ property, title issues, "
        "and stability strategies."
    )
    user_input = st.text_input("Ask me anything:")
    if user_input:
        st.write(f"🔍 You asked: {user_input}")
        st.success("Azure OpenAI answer placeholder.")

with tab4: 
    st.subheader("About Us")
    st.info(
        "Learn more about the team here."
    )
