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

    # Initialize transcription service
    if 'live_transcription' not in st.session_state:
        st.session_state.live_transcription = LiveTranscription()
        st.session_state.live_transcription.start()

    # Initialize session state for storing messages
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display old messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Check if new transcription is available
    transcript, sample_length, inference_time, confidence = st.session_state.live_transcription.get_last_text()
    if transcript:
        if 'last_transcript' not in st.session_state or transcript != st.session_state.last_transcript:
            st.session_state.last_transcript = transcript
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)
            generate_response(transcript)

    # Listening feedback
    with st.chat_message("user"):
        st.write("🎤 Listening... please speak.")

def generate_response(prompt):
    if st.session_state.messages and st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_llm_response(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)

if __name__ == "__main__":
    run_app()
