import streamlit as st
import asyncio
from dotenv import load_dotenv

load_dotenv()
from app.agent import app, STATE

st.set_page_config(page_title="Launchpad", page_icon="🚀")

# Custom Styling & Typography
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
    /* Global Font - Carefully applied to avoid breaking Material Icons */
    html, body, .stApp, .stMarkdown, p, h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Explicitly protect Streamlit's icons */
    span.material-symbols-rounded, .material-icons {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    }

    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 2rem 0 3rem 0;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #4285f4, #d96570, #9b72cb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #888;
        font-weight: 300;
    }

    /* Suggestion Cards */
    .suggestions-grid {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 2rem;
    }
    .suggestion-card {
        background: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.1);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        width: 250px;
        text-align: left;
        transition: all 0.2s ease;
    }
    .suggestion-card:hover {
        background: rgba(128, 128, 128, 0.1);
        transform: translateY(-2px);
    }
    .card-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .card-title {
        font-weight: 500;
        font-size: 1rem;
        margin-bottom: 0.2rem;
        color: inherit;
    }
    .card-desc {
        font-size: 0.85rem;
        color: #888;
    }

    /* Chat Message Bubbles */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: transparent;
    }
    /* User message specific styling */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(66, 133, 244, 0.05) !important;
        border-left: 3px solid #4285f4;
    }

    /* Make the chat input more rounded */
    [data-testid="stChatInput"] {
        border-radius: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# Render Hero
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🚀 Launchpad</div>
    <div class="hero-subtitle">Your AI onboarding assistant. Let's get you set up for success.</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 Onboarding Status")
    st.write(f"**Name:** {STATE.name}")
    st.write(f"**Role:** {STATE.role}")
    st.markdown("---")
    st.write("**Completed Tasks:**")
    if STATE.completed_tasks:
        for task in STATE.completed_tasks:
            st.write(f"✅ {task}")
    else:
        st.write("None yet! Ask Launchpad what to do first.")

    st.markdown("---")
    with st.expander("🛠️ Developer Panel"):
        st.caption("Use this panel to simulate different employee states for the demo.")

        new_role = st.selectbox(
            "Employee Role",
            ["Software Engineer", "Product Manager", "Data Scientist", "HR Specialist", "Sales Representative"],
            index=["Software Engineer", "Product Manager", "Data Scientist", "HR Specialist", "Sales Representative"].index(STATE.role) if STATE.role in ["Software Engineer", "Product Manager", "Data Scientist", "HR Specialist", "Sales Representative"] else 0
        )
        if new_role != STATE.role:
            STATE.role = new_role
            st.rerun()

        # Core onboarding tasks applicable to everyone
        core_tasks = ["401(k) Enrollment", "Time Off & Workday", "Review Company Policies", "Introduce Yourself"]

        # Role-specific tasks matching role_guides.md
        role_tasks_map = {
            "Software Engineer": ["Local Development Setup", "Architecture Review", "First Commits", "AWS IAM Setup - MFA", "AWS IAM Setup - Federation", "AWS IAM Setup - Workload Roles", "AWS IAM Setup - Least Privilege"],
            "Product Manager": ["Product Roadmap", "Jira Access", "Stakeholder Meet & Greet", "Analytics Dashboard"],
            "Data Scientist": ["Data Warehouse Access", "Jupyter Setup", "Model Registry", "Data Privacy Training"],
            "HR Specialist": ["Workday Admin Setup", "Benefits Provider Sync", "Interview Training", "Onboarding Buddy"],
            "Sales Representative": ["Salesforce Setup", "Product Demo Training", "Territory Assignment", "Pitch Deck Review"]
        }

        role_tasks = role_tasks_map.get(STATE.role, [])

        # Separate the currently completed tasks into core and role buckets
        current_core = [t for t in STATE.completed_tasks if t in core_tasks]
        current_role = [t for t in STATE.completed_tasks if t in role_tasks]
        other_tasks = [t for t in STATE.completed_tasks if t not in core_tasks and t not in role_tasks]

        new_core = st.multiselect(
            "Core Tasks (All Employees)",
            options=core_tasks,
            default=current_core
        )

        new_role = st.multiselect(
            f"Role Tasks ({STATE.role})",
            options=role_tasks,
            default=current_role
        )

        new_tasks = new_core + new_role + other_tasks
        if set(new_tasks) != set(STATE.completed_tasks):
            STATE.completed_tasks = new_tasks
            st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 1. Capture new input BEFORE rendering UI
chat_prompt = st.chat_input("Ask Launchpad (e.g. 'What are my tasks to get started')...")

if chat_prompt:
    st.session_state.messages.append({"role": "user", "content": chat_prompt})

# 2. Render UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if len(st.session_state.messages) == 0:
    # Dynamically determine the 3rd suggestion card based on role
    role_suggestions = {
        "Software Engineer": {"icon": "💻", "title": "Tech Stack Setup", "desc": "Learn how to clone the repo and spin up local databases."},
        "Product Manager": {"icon": "📊", "title": "Product Roadmap", "desc": "Review the Q3/Q4 strategic objectives and Jira boards."},
        "Data Scientist": {"icon": "📈", "title": "Data Warehouse", "desc": "Request access to BigQuery and set up Jupyter."},
        "HR Specialist": {"icon": "👥", "title": "Workday Setup", "desc": "Complete the administrative onboarding to manage records."},
        "Sales Representative": {"icon": "🤝", "title": "Salesforce Profile", "desc": "Log into Salesforce and set up your initial profile."}
    }

    specific_card = role_suggestions.get(STATE.role, {"icon": "✨", "title": "Role Setup", "desc": "Find out what specific setup you need for your role."})

    st.markdown(f"""
    <div class="suggestions-grid">
        <div class="suggestion-card">
            <div class="card-icon">📋</div>
            <div class="card-title">What are my tasks?</div>
            <div class="card-desc">Find out what you need to do next based on your current role.</div>
        </div>
        <div class="suggestion-card">
            <div class="card-icon">📚</div>
            <div class="card-title">Summarize Policies</div>
            <div class="card-desc">Get a quick overview of our core hours and code of conduct.</div>
        </div>
        <div class="suggestion-card">
            <div class="card-icon">{specific_card['icon']}</div>
            <div class="card-title">{specific_card['title']}</div>
            <div class="card-desc">{specific_card['desc']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 3. Generate response if the last message was from the user
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    prompt = st.session_state.messages[-1]["content"]
    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        def get_response(user_prompt):
            from google.adk.runners import Runner
            from google.adk.sessions import InMemorySessionService
            from google.genai import types
            from app.agent import root_agent

            if "session_service" not in st.session_state:
                st.session_state.session_service = InMemorySessionService()
                st.session_state.session = st.session_state.session_service.create_session_sync(user_id="local_user", app_name="launchpad")
                st.session_state.runner = Runner(agent=root_agent, session_service=st.session_state.session_service, app_name="launchpad")

            message = types.Content(role="user", parts=[types.Part.from_text(text=user_prompt)])
            events = list(st.session_state.runner.run(
                new_message=message,
                user_id="local_user",
                session_id=st.session_state.session.id
            ))

            full_response = ""
            for event in events:
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            full_response += part.text

            return full_response if full_response else "No response generated."

        try:
            with st.spinner("Launchpad is thinking..."):
                response_text = get_response(prompt)
            response_placeholder.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            st.rerun() # Force a rerun to instantly update the sidebar state
        except Exception as e:
            st.error(f"Agent error: {e}")
