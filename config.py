"""
TalentScout Configuration
=========================
Central configuration for the TalentScout Hiring Assistant chatbot.
Loads environment variables and defines application-wide constants.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Groq API (Llama) ──────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"       # Primary model
GROQ_MODEL_FAST = "llama-3.1-8b-instant"     # Fast model for sentiment/language tasks
GROQ_TEMPERATURE = 0.7
GROQ_MAX_TOKENS = 2048

# ── Conversation Phases ───────────────────────────────────────────────
# Ordered phases the conversation progresses through
PHASES = [
    "GREETING",
    "COLLECTING_NAME",
    "COLLECTING_EMAIL",
    "COLLECTING_PHONE",
    "COLLECTING_EXPERIENCE",
    "COLLECTING_POSITION",
    "COLLECTING_LOCATION",
    "COLLECTING_TECH_STACK",
    "GENERATING_QUESTIONS",
    "ASKING_QUESTIONS",
    "FAREWELL",
]

# Human-readable labels for the sidebar progress tracker
PHASE_LABELS = {
    "GREETING": "👋 Welcome",
    "COLLECTING_NAME": "📝 Full Name",
    "COLLECTING_EMAIL": "📧 Email Address",
    "COLLECTING_PHONE": "📱 Phone Number",
    "COLLECTING_EXPERIENCE": "💼 Experience",
    "COLLECTING_POSITION": "🎯 Desired Position",
    "COLLECTING_LOCATION": "📍 Location",
    "COLLECTING_TECH_STACK": "🛠️ Tech Stack",
    "GENERATING_QUESTIONS": "⚙️ Preparing Questions",
    "ASKING_QUESTIONS": "❓ Technical Assessment",
    "FAREWELL": "✅ Complete",
}

# ── Exit Keywords ─────────────────────────────────────────────────────
EXIT_KEYWORDS = [
    "bye", "goodbye", "quit", "exit", "end", "stop",
    "thank you", "thanks", "that's all", "i'm done",
    "no more", "finish", "done", "see you",
]

# ── Data Storage ──────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "candidates")

# ── UI Constants ──────────────────────────────────────────────────────
APP_TITLE = "TalentScout"
APP_SUBTITLE = "Intelligent Hiring Assistant"
APP_ICON = "🎯"
ASSISTANT_AVATAR = "🤖"
USER_AVATAR = "👤"
