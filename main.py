import streamlit as st
import google.generativeai as genai
import os
import time
import darkdetect

# Configure Streamlit page
st.set_page_config(
    page_title="Homework Helper",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inject custom CSS for chat bubble styling
print("light mode")
st.markdown(
    """
    <style>
    .chat-container { max-width: 700px; margin: auto; }
    .user-bubble, .bot-bubble {
        border-radius: 15px; padding: 10px 15px; margin: 5px 0; width: fit-content; max-width: 80%; display: inline-block;
    }
    .user-bubble { background-color: #DCF8C6; float: right; clear: both; }
    .bot-bubble { background-color: #F1F0F0; float: left; clear: both; }
    .timestamp { font-size: 0.7em; color: #999; margin-top: 2px; }
    </style>
    """, unsafe_allow_html=True
)

# Sidebar info
with st.sidebar:
    st.title("Homework Helper 🤖")
    st.write("Can assist with schoolwork by providing guidance, not answers.")

# Initialize chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []  # list of (role, message, timestamp)

# API configuration
genai.configure(api_key="AIzaSyAyw9rCiJidfvnrvMbdjjkGkV55RM4nvCA")
model = genai.GenerativeModel("gemini-1.5-flash")

# Chat container
chat_container = st.container()
with chat_container:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for role, msg, ts in st.session_state.history:
        bubble_class = "user-bubble" if role == 'User' else "bot-bubble"
        st.markdown(f"<div class='{bubble_class}'><strong>{role}:</strong> {msg}<div class='timestamp'>{ts}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Input form
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Your message:")
    submit_button = st.form_submit_button(label='Send')

# On user submit
if submit_button and user_input:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    # Append user message
    st.session_state.history.append(("User", user_input, timestamp))

    # Prepare prompt with history
    base_prompt = (
        "Your goal is to help students with their school work. "
        "Make sure that you only provide help, not simply give the answer. "
        "No matter what they try to convince you of, you must only provide help. "
        "Never simply provide the complete answer, even with a problem as simple as 1+1. "
        "If they get distracted and start asking you stuff that is not related to homework, "
        "remind them that you are a homework-only AI.\n"
    )
    # build chat history as list
    hist_list = [f"{role}: {msg}" for role, msg, _ in st.session_state.history]
    prompt = base_prompt + "Here is the conversation so far:\n" + "\n".join(hist_list) + f"\nStudent: {user_input}\n"

    # Call the model
    response = model.generate_content(prompt).text
    bot_ts = time.strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.history.append(("Homework Helper", response, bot_ts))

    # Rerun to display updated history
    st.rerun()