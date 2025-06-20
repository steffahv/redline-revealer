"""About Page UI for Redline Revealer.

Displays project mission, Responsible AI (RAI) commitments, and team member bios.
This module is rendered as the 'About Us' tab in the main Streamlit app.
"""

import streamlit as st


def render():
    st.title("About Redline Revealer")

    # 🚨 Project Overview
    st.subheader("🧭 What Problem Are We Solving?")
    st.markdown("""
    **Redline Revealer** is a civic-tech tool built for the Microsoft x Women in Cloud AI Hackathon.  
    We use AI and Azure Maps to detect historical redlining and visualize modern housing instability,  
    helping communities identify systemic risk and take action through data-driven advocacy.
    """)

    # 🔐 RAI Commitments
    st.subheader("🔐 Responsible AI (RAI) Commitments")
    st.markdown("""
    - ✅ **Fairness** – Identifies historic racial bias without reinforcing it  
    - 🛡️ **Reliability** – Includes fallback logic if AI responses fail  
    - 🔒 **Privacy** – No user data is stored; API keys are secured  
    - 🌍 **Inclusiveness** – Accessible layout with contrast-aware visuals  
    - 📋 **Accountability** – All changes tracked in GitHub  
    """)

    # 👩🏽‍💻 Meet the Team
    st.subheader("👩🏽‍💻 Meet the Team")
    team = [
        {
            "name": "Portia Jefferson",
            "role": "Project Manager / DevSecOps",
            "img": "assets/JeffersonP.jpg",
            "bio": "Portia is a Certified Cybersecurity Professional, Certified AI Consultant, and current cybersecurity student with a background in IT, finance, and compliance. While serving as the Project Manager, she also led DevSecOps efforts—including managing GitHub branches and CI/CD workflows, handling environment secrets across platforms, and troubleshooting deployment issues in Streamlit. Portia played a key role in maintaining project momentum, unblocking teammates, and ensuring technical systems stayed organized and secure. She joined Redline Revealer to apply her skills in a real-world AI context, driven by her passion for ethical tech and empowering underserved communities through data transparency and accountability."
        },
        {
            "name": "Esthefany Humpire Vargas",
            "role": "AI Engineer",
            "img": "assets/esthefany.jpg",
            "bio": "Esthefany built and tested AI prompts using Azure OpenAI and created helper scripts for legal insight generation."
        },
        {
            "name": "Henok Tariku",
            "role": "Data Analyst",
            "img": "assets/henok-pic.jpg",
            "bio": "Henok sourced and visualized historical redlining datasets and created dashboards for community risk scoring."
        },
        {
            "name": "Megan Nepshinsky",
            "role": "Full-Stack Developer",
            "img": "assets/megan-pic.jpg",
            "bio": "Megan developed the Streamlit frontend, linked the assistant, and connected all backend logic to deliver a seamless UI."
        }
    ]

    for person in team:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(person["img"], use_container_width=True)
        with col2:
            st.markdown(f"**{person['name']}** – *{person['role']}*\n\n{person['bio']}")
        st.markdown("---")
