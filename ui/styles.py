"""
Custom Styles
=============
CSS injection for the TalentScout Streamlit interface.
Provides a premium, modern look with dark theme, glassmorphism,
and smooth animations.
"""


def get_custom_css() -> str:
    """Return the complete custom CSS for the application."""
    return """
<style>
    /* ── Google Fonts ─────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Root Variables ───────────────────────────────────────────── */
    :root {
        --primary: #6C63FF;
        --primary-light: #8B83FF;
        --primary-dark: #4F46E5;
        --accent: #00D4AA;
        --accent-light: #33DDBB;
        --bg-dark: #0F0F1A;
        --bg-card: #1A1A2E;
        --bg-card-hover: #222240;
        --bg-glass: rgba(26, 26, 46, 0.7);
        --text-primary: #F0F0FF;
        --text-secondary: #A0A0C0;
        --text-muted: #6B6B8D;
        --border: rgba(108, 99, 255, 0.2);
        --border-light: rgba(108, 99, 255, 0.1);
        --shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        --shadow-glow: 0 0 20px rgba(108, 99, 255, 0.15);
        --radius: 16px;
        --radius-sm: 10px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ── Global ───────────────────────────────────────────────────── */
    .stApp {
        background: var(--bg-dark) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Hide default Streamlit elements */
    #MainMenu, footer, header {
        visibility: hidden !important;
    }

    .block-container {
        padding-top: 2rem !important;
        max-width: 900px !important;
    }

    /* ── Sidebar ──────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12122A 0%, #0F0F1A 100%) !important;
        border-right: 1px solid var(--border) !important;
    }

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown span {
        color: var(--text-secondary) !important;
        font-family: 'Inter', sans-serif !important;
    }

    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Chat Messages ────────────────────────────────────────────── */
    .stChatMessage {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: var(--radius) !important;
        padding: 1.2rem 1.5rem !important;
        margin-bottom: 1rem !important;
        box-shadow: var(--shadow) !important;
        animation: messageSlideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px) !important;
    }

    .stChatMessage:hover {
        border-color: var(--border) !important;
        box-shadow: var(--shadow), var(--shadow-glow) !important;
    }

    /* User messages — subtle purple tint */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(135deg, rgba(108, 99, 255, 0.08), rgba(26, 26, 46, 0.9)) !important;
    }

    .stChatMessage p, .stChatMessage li, .stChatMessage span {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
    }

    .stChatMessage ol, .stChatMessage ul {
        padding-left: 1.2rem !important;
    }

    /* ── Chat Input ───────────────────────────────────────────────── */
    .stChatInput {
        border-color: var(--border) !important;
    }

    .stChatInput > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        box-shadow: var(--shadow) !important;
    }

    .stChatInput textarea {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        caret-color: var(--primary) !important;
    }

    .stChatInput textarea::placeholder {
        color: var(--text-muted) !important;
    }

    /* ── Progress Bar ─────────────────────────────────────────────── */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary), var(--accent)) !important;
        border-radius: 10px !important;
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stProgress > div {
        background: var(--bg-card) !important;
        border-radius: 10px !important;
        height: 8px !important;
    }

    /* ── Buttons ──────────────────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.5rem !important;
        transition: var(--transition) !important;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(108, 99, 255, 0.4) !important;
    }

    /* ── Dividers ─────────────────────────────────────────────────── */
    hr {
        border-color: var(--border-light) !important;
    }

    /* ── Animations ───────────────────────────────────────────────── */
    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 5px rgba(108, 99, 255, 0.2); }
        50% { box-shadow: 0 0 15px rgba(108, 99, 255, 0.4); }
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ── Sentiment Badge ──────────────────────────────────────────── */
    .sentiment-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        animation: messageSlideIn 0.3s ease-out;
    }

    /* ── Info Cards in Sidebar ────────────────────────────────────── */
    .info-card {
        background: var(--bg-card);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-sm);
        padding: 12px 16px;
        margin-bottom: 8px;
        transition: var(--transition);
    }

    .info-card:hover {
        border-color: var(--border);
        background: var(--bg-card-hover);
    }

    .info-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--text-muted);
        margin-bottom: 2px;
    }

    .info-value {
        font-size: 0.95rem;
        color: var(--text-primary);
        font-weight: 500;
    }

    /* ── Logo / Brand Header ──────────────────────────────────────── */
    .brand-header {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
    }

    .brand-title {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary-light), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }

    .brand-subtitle {
        font-size: 0.85rem;
        color: var(--text-muted);
        font-weight: 400;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* ── Phase Indicator ──────────────────────────────────────────── */
    .phase-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 4px;
        font-size: 0.85rem;
        transition: var(--transition);
    }

    .phase-active {
        background: rgba(108, 99, 255, 0.15);
        color: var(--primary-light);
        font-weight: 600;
    }

    .phase-done {
        color: var(--accent);
    }

    .phase-pending {
        color: var(--text-muted);
    }

    /* ── Scrollbar ────────────────────────────────────────────────── */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary);
    }

    /* ── Expander ─────────────────────────────────────────────────── */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border-radius: var(--radius-sm) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .streamlit-expanderContent {
        background: var(--bg-card) !important;
        border-color: var(--border-light) !important;
    }
</style>
"""
