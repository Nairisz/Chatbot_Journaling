# analysis_page.py
import streamlit as st
import pandas as pd
import altair as alt

from db import load_journals
from cluster_analysis import cluster_journals


CLUSTER_NAMES = {
    1: "Cluster 1 (General Reflection)",
    2: "Cluster 2 (Personal thoughts & desires)",
    3: "Cluster 3 (Daily activities & interest)"
}


def show_analysis_page():
    st.subheader("🧠 Writing Pattern Analysis")

    st.caption(
        "Journal entries are grouped based on similar writing themes and emotional tone. "
        "This analysis is exploratory and does not assign fixed emotional labels."
    )

    journals = load_journals()

    if len(journals) < 3:
        st.info("Add at least 3 journals to enable writing pattern analysis.")
        return

    texts = [content for _, _, _, content, _ in journals]
    labels, coords_df, cluster_terms = cluster_journals(texts)

    # ---- Cluster previews ----
    for cluster_id in sorted(set(labels)):
        display_id = cluster_id + 1
        cluster_name = CLUSTER_NAMES.get(display_id, f"Cluster {display_id}")

        st.markdown(f"### {cluster_name}")
        st.caption(
            "This label is interpretive, not absolute. "
            "They represent groups of journals with similar language usage."
        )

        terms = ", ".join(cluster_terms.get(cluster_id, []))
        st.caption(f"Common terms: {terms}")

        idx = list(labels).index(cluster_id)
        preview = texts[idx][:300]
        st.markdown("> " + preview + "...")

    # ---- Visualization ----
    coords_df["ClusterName"] = coords_df["cluster"].apply(
        lambda x: CLUSTER_NAMES.get(x + 1)
    )

    st.subheader("📊 Cluster Visualization")
    st.scatter_chart(coords_df, x="x", y="y", color="ClusterName")

    # ---- Sentiment distribution ----
    df = pd.DataFrame({
        "ClusterName": [CLUSTER_NAMES[c + 1] for c in labels],
        "Sentiment": [s for _, _, _, _, s in journals]
    })

    sentiment_order = ["Negative", "Neutral", "Positive"]

    ct = pd.crosstab(df["ClusterName"], df["Sentiment"])
    ct = ct.reindex(columns=sentiment_order, fill_value=0)

    chart_df = (
        ct.reset_index()
        .melt(id_vars="ClusterName", var_name="Sentiment", value_name="Count")
    )

    st.subheader("📊 Sentiment Distribution by Writing Pattern")

    chart = alt.Chart(chart_df).mark_bar().encode(
        x=alt.X("ClusterName:N", title="Writing Pattern Cluster"),
        y=alt.Y("Count:Q"),
        color=alt.Color(
            "Sentiment:N",
            scale=alt.Scale(
                domain=["Negative", "Neutral", "Positive"],
                range=["#4C78A8", "#BFBFBF", "#54A24B"]
            )
        ),
        tooltip=["ClusterName", "Sentiment", "Count"]
    )

    st.altair_chart(chart, use_container_width=True)
