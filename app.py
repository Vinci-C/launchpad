import streamlit as st
import asyncio
from dotenv import load_dotenv

load_dotenv()
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

        def get_response():
            from google.adk.runners import Runner
            from google.adk.sessions import InMemorySessionService
            from google.genai import types
            from app.agent import root_agent

            if "session_service" not in st.session_state:
                st.session_state.session_service = InMemorySessionService()
                st.session_state.session = st.session_state.session_service.create_session_sync(user_id="local_user", app_name="launchpad")
                st.session_state.runner = Runner(agent=root_agent, session_service=st.session_state.session_service, app_name="launchpad")

            message = types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
            events = list(st.session_state.runner.run(
                new_message=message,
                user_id="local_user",
                session_id=st.session_state.session.id
            ))

            # Combine all text chunks from the response events
            full_response = ""
            for event in events:
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            full_response += part.text

            return full_response if full_response else "No response generated."

        try:
            with st.spinner("Launchpad is thinking..."):
                # Call synchronously
                response_text = get_response()
            response_placeholder.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            st.error(f"Agent error: {e}")
