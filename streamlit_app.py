import streamlit as st
import requests
import uuid

# App title
st.set_page_config(page_title="💬 LLM Chatbot")

# Set up the sidebar
with st.sidebar:
    st.title('💬 LLM Chatbot')
    st.write('This chatbot is powered by a custom LLM backend.')

def send_message(url, headers, model, content, temperature, session_id, stream=False):
    data = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "temperature": temperature,
        "session_id": session_id,
        "stream": stream  # Add stream parameter to the request
    }
    response = requests.post(url, headers=headers, json=data)  # Use json=data to ensure correct formatting
    return response

# Define a function to send requests to your LLM backend
def generate_llm_response(user_input):
    model = "tavily-search:latest"
    temperature = 0.7
    url = "https://llm-chatbot-e79778afdb58.herokuapp.com/v1/chat/completions"  # Update with your FastAPI endpoint
    headers = {
        'Content-Type': 'application/json'
    }

    # Retrieve or generate session_id
    if 'session_id' not in st.session_state:
        st.session_state.session_id = f"session-{uuid.uuid4()}"

    response = send_message(url, headers, model, user_input, temperature, st.session_state.session_id)

    if response.status_code == 200:
        return response.json().get('content', "Error in receiving response")
    else:
        return "Error: Could not fetch response from the backend."

# Initialize session state for storing messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt through chat input
prompt = st.chat_input("Enter your message:", disabled=False)
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages and st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_llm_response(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)
