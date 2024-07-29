import requests
import streamlit as st

from utils import generate_session_id


def send_message(url, headers, model, content, temperature, session_id, stream=False):
    data = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "temperature": temperature,
        "session_id": session_id,
        "stream": stream
    }
    response = requests.post(url, headers=headers, json=data)
    return response


def generate_llm_response(user_input):
    model = "tavily-search:latest"
    temperature = 0.7
    url = "https://llm-chatbot-e79778afdb58.herokuapp.com/v1/chat/completions"  # Update with your FastAPI endpoint
    headers = {
        'Content-Type': 'application/json'
    }

    # Retrieve or generate session_id
    if 'session_id' not in st.session_state:
        st.session_state.session_id = generate_session_id()

    response = send_message(url, headers, model, user_input, temperature, st.session_state.session_id)

    if response.status_code == 200:
        return response.json().get('content', "Error in receiving response")
    else:
        return "Error: Could not fetch response from the backend."