import streamlit as st
from db import create_tables
from chat_page import show_chat_page
from dashboard import show_dashboard
from analysis_page import show_analysis_page
from chat_ui import render_chat_bubble


def load_css():
    with open("styles/theme.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
create_tables()

st.title("📝 Conversational Journal with Sentiment Analysis")

page = st.sidebar.radio(
    "Navigation",
    ["Chat", "Journal Dashboard", "Writing Pattern Analysis"]
)

if page == "Chat":
    show_chat_page()

elif page == "Journal Dashboard":
    show_dashboard()

elif page == "Writing Pattern Analysis":
    show_analysis_page()
