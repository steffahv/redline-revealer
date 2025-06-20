"""Main Streamlit App Launcher for Redline Revealer.

Initializes session state and routes to modular pages: Welcome, Map, Assistant, About.
Serves as the entry point for Streamlit execution.
"""

import sys
import os

# Add /src to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
from pages import welcome, map, assistant, about

# Set page config
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
    map.render()
elif page == "🤖 LLM Assistant":
    assistant.render()
elif page == "💡 About Us":
    about.render()
