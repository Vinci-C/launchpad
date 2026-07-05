import streamlit as st
import asyncio
from app.agent import app

st.set_page_config(page_title="Launchpad", page_icon="🚀")

st.title("🚀 Launchpad: Employee Onboarding")
st.markdown("Welcome to your first day! I'm Launchpad, your AI onboarding assistant. How can I help you get started?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Launchpad (e.g. 'What are the company policies?')..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        async def get_response():
            # Run the ADK app
            # ADK App.run returns a string or an object with .text
            response = await app.run(prompt)
            if hasattr(response, "text"):
                return response.text
            return str(response)

        try:
            with st.spinner("Launchpad is thinking..."):
                response_text = asyncio.run(get_response())
            response_placeholder.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            st.error(f"Agent error: {e}")
