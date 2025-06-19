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
        "Learn more about the team here.")
    st.html("<h1>Portia Jefferson</h1>"
        "<h2> Role: Project Manager & DevSecOps Lead </h2>")
    st.image("./assets/JeffersonP.jpg", height = 200)
    st.html(
        "<p> Portia is a Certified Cybersecurity Professional, Certified AI Consultant, and current cybersecurity student with a background in IT, finance, and compliance. </p>"
        "<p> She joined the Redline Revealer project to put her skills to the test in a hands-on setting—especially in exploring how AI can be used to address ethical challenges and support communities. </p>"
        "<p> As the team’s Project Manager and DevSecOps lead, she coordinated timelines, facilitated tool access, and ensured GitHub workflows stayed organized and secure. Portia is passionate about using technology to uncover systemic issues and empower communities—and saw this project as a meaningful way to contribute to that mission.</p>")
