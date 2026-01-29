# chat_page.py
import streamlit as st
import pytz
from datetime import datetime

from db import save_chat, load_chat, save_journal, clear_chat
from nlp import analyze_sentiment
from chat_logic import handle_idle_input
from high_risk import high_risk_support_message
from chat_ui import render_chat_bubble

MY_TZ = pytz.timezone("Asia/Kuala_Lumpur")

# ============================
# Helper functions
# ============================
def now():
    return datetime.now(MY_TZ).strftime("%Y-%m-%d %H:%M")


def bot_say(message):
    save_chat("bot", message, now())


# ============================
# Main Chat Page
# ============================
def show_chat_page():

    st.subheader("Chat")

    # ---- Session state ----
    st.session_state.setdefault("mode", "idle")
    st.session_state.setdefault("greeted", False)
    st.session_state.setdefault("offer_journal", False)
    st.session_state.setdefault("journal_buffer", [])
    st.session_state.setdefault("rant_count", 0)
    st.session_state.setdefault("high_risk", False)

    # ---- Clear chat ----
    if st.button("🧹 Clear Chat"):
        clear_chat()
        st.session_state.mode = "idle"
        st.session_state.offer_journal = False
        st.session_state.journal_buffer = []
        st.session_state.rant_count = 0
        st.session_state.greeted = False
        st.rerun()

    # ---- Greeting ----
    if not st.session_state.greeted:
        bot_say("Hello, how are you today?")
        st.session_state.greeted = True
        st.rerun()

    # ---- Chat history ----
    for role, message, date in load_chat():
        render_chat_bubble(role, message, date)
    # ============================
    # Journaling offer buttons
    # ============================
    if st.session_state.offer_journal:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("✍️ Start journaling"):
                st.session_state.mode = "journaling"
                st.session_state.offer_journal = False
                bot_say("I'm here. Take your time. You can start sharing.")
                st.rerun()

        with col2:
            if st.button("Maybe later"):
                st.session_state.offer_journal = False

                if st.session_state.high_risk:
                    bot_say(high_risk_support_message("refuse"))
                    st.session_state.high_risk = False
                else:
                    bot_say("No worries. I'm here whenever you're ready.")

                st.rerun()

    # ============================
    # End journaling controls
    # ============================
    if st.session_state.mode == "journaling":
        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            if st.button("I think I'm done"):
                st.session_state.mode = "confirm_end"
                bot_say("Would you like to rename this journal?")
                st.rerun()

        with col2:
            if st.button("I want to keep writing"):
                bot_say("Go on.")
                st.rerun()

    # ============================
    # Finalize journal
    # ============================
    if st.session_state.mode == "confirm_end":
        st.subheader("Finalize Journal")

        rename = st.radio("Rename journal?", ["Use default title", "Rename"])
        journal_title = (
            st.text_input("New journal title") if rename == "Rename"
            else "Untitled Reflection"
        )

        journal_content = "\n".join(st.session_state.journal_buffer)

        if st.button("Save Journal"):
            sentiment = analyze_sentiment(journal_content)

            save_journal(now(), journal_title, journal_content, sentiment)

            clear_chat()
            st.session_state.mode = "idle"
            st.session_state.journal_buffer = []
            st.session_state.rant_count = 0
            st.session_state.greeted = False

            if st.session_state.high_risk:
                bot_say(high_risk_support_message("accept"))
                st.session_state.high_risk = False
            else:
                bot_say("Your journal has been saved. Thank you for sharing.")

            st.rerun()

    # ============================
    # Chat input (ALWAYS LAST)
    # ============================
    if st.session_state.mode != "confirm_end":
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("Write your thoughts here...")
            submitted = st.form_submit_button("Send")

        if submitted and user_input:
            save_chat("user", user_input, now())

            if st.session_state.mode == "journaling":
                st.session_state.journal_buffer.append(user_input)
                st.session_state.rant_count += 1

                if st.session_state.rant_count % 3 == 0:
                    bot_say("I'm here. Go on.")

            elif st.session_state.mode == "idle":
                handle_idle_input(user_input.lower(), bot_say, st.session_state)

            st.rerun()

