import streamlit as st

from llm_api import generate_llm_response
from utils import generate_session_id
from speech_module.transcription import LiveTranscription

def run_app():
    # App title
    st.set_page_config(page_title="💬 LLM Chatbot")
    
    # Set up the sidebar
    with st.sidebar:
        st.title('💬 LLM Chatbot')
        st.write('This chatbot is powered by a custom LLM backend.')

    with st.spinner("Loading..."):
        live_transcription = LiveTranscription()
        live_transcription.start()

    # Initialize session state for storing messages
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    try:
        while True:
                # prompt = st.chat_input("Enter your message:", disabled=False)
                print("waiting for prompt")
                transcript, sample_length, inference_time, confidence = live_transcription.get_last_text()
                prompt = transcript
                print("prompt", prompt)
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
    except KeyboardInterrupt:
        live_transcription.stop()

if __name__ == "__main__":
    run_app()