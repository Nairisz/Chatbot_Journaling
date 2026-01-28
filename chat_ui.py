import streamlit as st

def render_chat_bubble(role, message, date):
    if role == "user":
        bg = "#D6E4FF"   # soft blue
        align = "flex-end"
        radius = "15px 15px 0 15px"
    else:
        bg = "#EDE7F6"   # soft purple
        align = "flex-start"
        radius = "15px 15px 15px 0"

    st.markdown(f"""
    <div style="display:flex; justify-content:{align}; margin:6px 0;">
        <div style="
            background-color:{bg};
            padding:10px 14px;
            border-radius:{radius};
            max-width:70%;
            font-size:15px;
            box-shadow:0 1px 3px rgba(0,0,0,0.1);
        ">
            {message}
            <div style="font-size:10px; color:#555; text-align:right;">
                {date}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
