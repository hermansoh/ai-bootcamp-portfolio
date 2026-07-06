"""
app.py

Streamlit web interface for chatbot.py
Run with: streamlit run app.py
"""

import streamlit as st
from chatbot import get_response as chat

st.title("My Local Chatbot")

# --- Session state: this is what makes it feel like a real conversation ----
# Every time you send a message, Streamlit re-runs this whole script from
# top to bottom. Without session_state, your history would reset to empty
# each time. session_state persists across those re-runs for as long as
# the browser tab stays open.
if "history" not in st.session_state:
    st.session_state.history = []  # list of {"role": ..., "content": ...} dicts

# --- Redraw all past messages as chat bubbles -------------------------------
# On every re-run, we redraw the full conversation so far. st.chat_message
# is a Streamlit component that renders a styled bubble for "user" or
# "assistant" roles automatically.
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- Input box at the bottom ------------------------------------------------
# st.chat_input renders the text box fixed at the bottom of the page.
# It returns None until the user actually submits something, then returns
# the text they typed.
user_input = st.chat_input("Type a message...")

if user_input:
    # Show the user's message immediately.
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.history.append({"role": "user", "content": user_input})

    # Call your existing chat() function, passing the history so it has
    # context from earlier in the conversation.
    with st.spinner("Thinking..."):
        reply = chat(user_input)    # Show the bot's reply.
    with st.chat_message("assistant"):
        st.write(reply)
    st.session_state.history.append({"role": "assistant", "content": reply})