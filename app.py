import streamlit as st
from modules import welcome, map_page, assistant, about

# Configure page
st.set_page_config(page_title="Redline Revealer", layout="wide")

# Sidebar navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", [
    "👋 Welcome",
    "📍 Redlining Map",
    "🤖 LLM Assistant",
    "💡 About Us"
])

# Load selected page
if page == "👋 Welcome":
    welcome.render()
elif page == "📍 Redlining Map":
    map_page.render()
elif page == "🤖 LLM Assistant":
    assistant.render()
elif page == "💡 About Us":
    about.render()
