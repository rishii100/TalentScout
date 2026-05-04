"""
UI Components
=============
Reusable Streamlit UI components for the TalentScout interface.
Handles the sidebar, progress tracking, branding, and info display.
"""

import os
import json
import streamlit as st
from config import PHASES, PHASE_LABELS, DATA_DIR


def render_brand_header():
    """Render the TalentScout brand header in the sidebar."""
    st.sidebar.markdown(
        """
        <div class="brand-header">
            <div style="font-size: 3rem; margin-bottom: 8px;">🎯</div>
            <div class="brand-title">TalentScout</div>
            <div class="brand-subtitle">Intelligent Hiring Assistant</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_progress(current_phase: str):
    """
    Render the screening progress bar and phase indicators in the sidebar.

    Parameters
    ----------
    current_phase : str
        The current conversation phase.
    """
    st.sidebar.markdown("### 📊 Screening Progress")

    # Progress bar
    if current_phase in PHASES:
        progress = PHASES.index(current_phase) / (len(PHASES) - 1)
    else:
        progress = 1.0
    st.sidebar.progress(progress)

    percentage = int(progress * 100)
    st.sidebar.markdown(
        f"<p style='text-align:center; font-size:0.8rem; color:#A0A0C0;'>"
        f"{percentage}% complete</p>",
        unsafe_allow_html=True,
    )

    # Phase checklist
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Steps")

    current_idx = PHASES.index(current_phase) if current_phase in PHASES else len(PHASES)

    for i, phase in enumerate(PHASES):
        label = PHASE_LABELS.get(phase, phase)
        if i < current_idx:
            # Completed
            st.sidebar.markdown(
                f'<div class="phase-item phase-done">✅ {label}</div>',
                unsafe_allow_html=True,
            )
        elif i == current_idx:
            # Active
            st.sidebar.markdown(
                f'<div class="phase-item phase-active">▶️ {label}</div>',
                unsafe_allow_html=True,
            )
        else:
            # Pending
            st.sidebar.markdown(
                f'<div class="phase-item phase-pending">○ {label}</div>',
                unsafe_allow_html=True,
            )


def render_candidate_info(candidate: dict):
    """
    Display collected candidate information in the sidebar.

    Parameters
    ----------
    candidate : dict
        The candidate data dictionary.
    """
    # Only show if at least one field has been filled
    filled = {k: v for k, v in candidate.items() if v}
    if not filled:
        return

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👤 Candidate Profile")

    field_labels = {
        "name": ("📝", "Name"),
        "email": ("📧", "Email"),
        "phone": ("📱", "Phone"),
        "experience": ("💼", "Experience"),
        "position": ("🎯", "Position"),
        "location": ("📍", "Location"),
        "tech_stack": ("🛠️", "Tech Stack"),
    }

    for field, value in filled.items():
        emoji, label = field_labels.get(field, ("•", field.title()))
        display_value = f"{value} years" if field == "experience" else value
        st.sidebar.markdown(
            f"""<div class="info-card">
                <div class="info-label">{emoji} {label}</div>
                <div class="info-value">{display_value}</div>
            </div>""",
            unsafe_allow_html=True,
        )


def render_sentiment_badge(sentiment_data: dict):
    """
    Display the current sentiment indicator in the sidebar.

    Parameters
    ----------
    sentiment_data : dict
        Sentiment info with keys: emoji, color, label.
    """
    if not sentiment_data:
        return

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧠 Candidate Mood")

    emoji = sentiment_data.get("emoji", "😐")
    color = sentiment_data.get("color", "#9E9E9E")
    label = sentiment_data.get("label", "Neutral")

    st.sidebar.markdown(
        f"""<div class="sentiment-badge" style="background: {color}20; border: 1px solid {color}40; color: {color};">
            {emoji} {label}
        </div>""",
        unsafe_allow_html=True,
    )


def render_new_session_button():
    """Render the new session button in the sidebar."""
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 New Session", use_container_width=True):
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


def render_main_header():
    """Render the main chat area header."""
    st.markdown(
        """
        <div style="text-align: center; padding: 1rem 0 2rem 0;">
            <h1 style="
                font-family: 'Inter', sans-serif;
                font-weight: 800;
                font-size: 2.2rem;
                background: linear-gradient(135deg, #8B83FF, #00D4AA);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 8px;
            ">🎯 TalentScout</h1>
            <p style="
                font-family: 'Inter', sans-serif;
                color: #6B6B8D;
                font-size: 1rem;
                font-weight: 400;
            ">AI-Powered Candidate Screening Assistant</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_admin_dashboard():
    """Render the admin dashboard to view saved candidate JSON files."""
    st.markdown("## 🔐 Admin Dashboard")
    st.markdown("View all stored candidate screening sessions directly from the backend `data/candidates/` folder.")
    
    if not os.path.exists(DATA_DIR):
        st.info("No candidate data directory found.")
        return
        
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
    
    if not files:
        st.info("No candidate sessions saved yet.")
        return
        
    selected_file = st.selectbox("Select Candidate Session", sorted(files, reverse=True))
    
    if selected_file:
        file_path = os.path.join(DATA_DIR, selected_file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            st.markdown(f"### 📄 Session Data: `{selected_file}`")
            st.json(data)
        except Exception as e:
            st.error(f"Error reading file: {e}")
