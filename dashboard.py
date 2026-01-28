# dashboard.py
import streamlit as st
import pandas as pd
from datetime import datetime

from db import load_journals, update_journal_title, delete_journal
from expressions import analyze_expression


def format_timestamp(ts):
    try:
        dt = datetime.strptime(ts, "%Y-%m-%d %H:%M")
        return dt.strftime("%d/%m/%Y · %H:%M")
    except ValueError:
        dt = datetime.strptime(ts, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")


def show_dashboard():
    st.subheader("📓 Journal Dashboard")

    show_only_high_risk = st.checkbox("🚨 Show only high-risk journals")

    sort_order = st.radio(
        "Sort journals",
        ["Newest first", "Oldest first"],
        horizontal=True
    )

    journals = load_journals()

    # Count high risk entries
    high_risk_count = 0
    for _, _, _, content, _ in journals:
        if "High Risk" in analyze_expression(content):
            high_risk_count += 1

    st.metric("🚨 High Risk Entries", high_risk_count)

    if sort_order == "Oldest first":
        journals = list(reversed(journals))

    if not journals:
        st.info("No journals saved yet.")
        return

    dates = []

    for journal_id, timestamp, title, content, sentiment in journals:
        expressions = analyze_expression(content)
        is_high_risk = "High Risk" in expressions

        if show_only_high_risk and not is_high_risk:
            continue

        emoji = {
            "Positive": "😁",
            "Negative": "😔",
            "Neutral": "😐"
        }.get(sentiment, "📝")

        # Manage panel
        with st.expander("⚙️ Manage journal"):
            new_title = st.text_input(
                "Edit journal title",
                value=title,
                key=f"title_{journal_id}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Save title", key=f"save_{journal_id}"):
                    update_journal_title(journal_id, new_title)
                    st.success("Title updated")
                    st.rerun()

            with col2:
                if st.button("🗑️ Delete journal", key=f"delete_{journal_id}"):
                    delete_journal(journal_id)
                    st.warning("Journal deleted")
                    st.rerun()

        formatted_time = format_timestamp(timestamp)

        st.markdown(f"### 📅 {formatted_time} {emoji}")

        if is_high_risk:
            st.error(
                "⚠️ This journal shows signs of emotional distress.\n\n"
                "📞 Befrienders (Malaysia): 03-7627 2929\n"
                "🌐 https://www.befrienders.org.my",
                icon="🚨"
            )
            dates.append(timestamp[:10])

        st.markdown(f"#### **{title}**")
        st.markdown(f"→ Sentiment: **{sentiment}**")
        st.markdown(f"→ Expression: **{' + '.join(expressions)}**")
        st.markdown(content)
        st.markdown("---")
