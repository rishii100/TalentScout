"""
TalentScout — Intelligent Hiring Assistant
==========================================
Main Streamlit application entry point.

This chatbot assists TalentScout, a technology recruitment agency,
in conducting initial candidate screenings. It collects candidate
information and generates tailored technical interview questions
based on the candidate's declared tech stack.

Run with: streamlit run app.py
"""

import streamlit as st
from config import APP_TITLE, APP_ICON, ASSISTANT_AVATAR, USER_AVATAR
from core.conversation import ConversationManager
from core.data_store import save_candidate_session
from modules.sentiment import analyze_sentiment
from modules.language import detect_language, get_bilingual_instruction
from core.prompts import SYSTEM_PROMPT
from ui.styles import get_custom_css
from ui.components import (
    render_brand_header,
    render_progress,
    render_candidate_info,
    render_sentiment_badge,
    render_new_session_button,
    render_main_header,
    render_admin_dashboard,
)

# ── Page Configuration ────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{APP_TITLE} : AI Hiring Assistant",
    page_icon=APP_ICON,
    layout="centered",
    initial_sidebar_state="expanded",
)

# Inject custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)


# ── Session State Initialization ──────────────────────────────────────

def init_session():
    """Initialize session state variables if they don't exist."""
    if "conversation_manager" not in st.session_state:
        st.session_state.conversation_manager = ConversationManager()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "initialized" not in st.session_state:
        st.session_state.initialized = False
    if "sentiment" not in st.session_state:
        st.session_state.sentiment = None
    if "sentiment_log" not in st.session_state:
        st.session_state.sentiment_log = []
    if "detected_language" not in st.session_state:
        st.session_state.detected_language = "English"
    if "session_saved" not in st.session_state:
        st.session_state.session_saved = False


init_session()
cm: ConversationManager = st.session_state.conversation_manager

# ── Sidebar ───────────────────────────────────────────────────────────
render_brand_header()
render_progress(cm.phase)
render_candidate_info(cm.candidate)
render_sentiment_badge(st.session_state.sentiment)
render_new_session_button()

st.sidebar.markdown("---")
if st.sidebar.toggle("🔐 Admin Mode"):
    render_admin_dashboard()
    st.stop()

# ── Main Chat Area ────────────────────────────────────────────────────
render_main_header()

# Generate greeting on first load
if not st.session_state.initialized:
    with st.spinner("Scout is getting ready..."):
        greeting = cm.get_greeting()
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    st.session_state.initialized = True

# Display conversation history
for message in st.session_state.messages:
    avatar = ASSISTANT_AVATAR if message["role"] == "assistant" else USER_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ── Chat Input Handler ────────────────────────────────────────────────
if not cm.ended:
    if user_input := st.chat_input("Type your message here..."):
        # Display user message
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Bonus: Detect language (only on first few messages to save API calls)
        if len(st.session_state.messages) <= 6:
            detected_lang = detect_language(user_input)
            if detected_lang != "English":
                st.session_state.detected_language = detected_lang

        # Bonus: Analyze sentiment
        sentiment_data = analyze_sentiment(user_input)
        st.session_state.sentiment = sentiment_data
        st.session_state.sentiment_log.append({
            "message": user_input[:100],  # Truncate for storage
            "sentiment": sentiment_data.get("sentiment", "neutral"),
        })

        # Generate assistant response
        with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
            with st.spinner("Scout is thinking..."):
                # Inject bilingual instruction if non-English detected
                bilingual_note = get_bilingual_instruction(
                    st.session_state.detected_language
                )

                response = cm.process_message(user_input)

                # If bilingual support is active, add note
                if bilingual_note and st.session_state.detected_language != "English":
                    response = response  # The LLM handles bilingual via system prompt

            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Save session data when conversation ends
        if cm.ended and not st.session_state.session_saved:
            try:
                session_id = save_candidate_session(
                    candidate=cm.candidate,
                    conversation_history=cm.history,
                    sentiment_log=st.session_state.sentiment_log,
                )
                st.session_state.session_saved = True
                st.toast(f"✅ Session saved (ID: {session_id})", icon="💾")
            except Exception:
                pass  # Silently handle save errors

        st.rerun()
else:
    # Show completion message
    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, rgba(108, 99, 255, 0.1), rgba(0, 212, 170, 0.1));
            border: 1px solid rgba(108, 99, 255, 0.2);
            border-radius: 16px;
            margin-top: 1rem;
        ">
            <p style="font-size: 2rem; margin-bottom: 8px;">✅</p>
            <p style="
                font-family: 'Inter', sans-serif;
                color: #A0A0C0;
                font-size: 0.95rem;
            ">
                Screening session complete. Click <b>🔄 New Session</b> in the sidebar to start a new screening.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
