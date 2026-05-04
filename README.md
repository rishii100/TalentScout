# 🎯 TalentScout — Intelligent Hiring Assistant

An AI-powered chatbot that conducts initial candidate screenings for **TalentScout**, a technology recruitment agency. Built with **Streamlit** and **Google Gemini 2.0 Flash**, the assistant collects candidate information and generates tailored technical interview questions based on the candidate's declared tech stack.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?logo=streamlit)
![Gemini](https://img.shields.io/badge/Gemini_2.0_Flash-API-orange?logo=google)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Technical Details](#technical-details)
- [Prompt Design](#prompt-design)
- [Data Privacy & GDPR](#data-privacy--gdpr)
- [Bonus Features](#bonus-features)
- [Challenges & Solutions](#challenges--solutions)
- [Project Structure](#project-structure)

---

## Overview

TalentScout's Hiring Assistant ("Scout") automates the initial phase of candidate screening by:

1. **Greeting** the candidate and explaining the process
2. **Collecting** essential information (name, email, phone, experience, desired position, location, tech stack)
3. **Generating** 3-5 tailored technical questions per technology in the candidate's stack
4. **Evaluating** responses with professional, encouraging feedback
5. **Concluding** the session with a summary and next-steps information

The chatbot maintains full conversation context, validates inputs, handles edge cases gracefully, and stores session data securely.

---

## Features

### Core
- ✅ **Conversational Screening** — Natural, step-by-step information gathering
- ✅ **Dynamic Technical Questions** — Generated based on candidate's tech stack & experience level
- ✅ **Input Validation** — Email, phone, and field-specific validation with gentle correction prompts
- ✅ **Context Awareness** — Full conversation history maintained for coherent follow-ups
- ✅ **Fallback Handling** — Graceful redirect for off-topic or unexpected inputs
- ✅ **Exit Detection** — Keywords like "bye", "quit", "exit" trigger graceful conclusion
- ✅ **Session Persistence** — Candidate data saved as JSON for recruiter review

### Bonus
- 🎁 **Sentiment Analysis** — Real-time candidate mood tracking displayed in the sidebar
- 🎁 **Multilingual Support** — Auto-detects non-English input and provides bilingual responses
- 🎁 **Premium UI** — Custom dark theme with glassmorphism, animations, and gradient accents

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Streamlit UI                       │
│  ┌──────────┐  ┌────────────────────────────────┐   │
│  │ Sidebar  │  │        Chat Interface           │   │
│  │ - Brand  │  │  [User Message]                 │   │
│  │ - Progress│  │  [Assistant Response]           │   │
│  │ - Info   │  │  [Chat Input]                   │   │
│  │ - Mood   │  │                                 │   │
│  └──────────┘  └────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────┘
                        │
                ┌───────▼───────┐
                │ Conversation  │
                │   Manager     │ ← State Machine (11 phases)
                └───────┬───────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
   ┌──────▼──────┐ ┌───▼───┐  ┌─────▼─────┐
   │ Prompt      │ │  LLM  │  │   Data    │
   │ Engine      │ │Wrapper│  │   Store   │
   │ (Templates) │ │(Gemini│  │  (JSON)   │
   └─────────────┘ └───────┘  └───────────┘
          │
   ┌──────▼──────────────────┐
   │   Bonus Modules         │
   │ - Sentiment Analyzer    │
   │ - Language Detector     │
   └─────────────────────────┘
```

### Conversation State Machine

The conversation progresses through these ordered phases:

```
GREETING → NAME → EMAIL → PHONE → EXPERIENCE → POSITION → LOCATION → TECH STACK → QUESTIONS → ANSWERS → FAREWELL
```

Each phase has:
- A tailored prompt template
- Input validation rules
- Automatic phase transition on valid input
- Fallback handling for invalid input

---

## Installation

### Prerequisites
- Python 3.10+
- A Google Gemini API key ([Get one free here](https://aistudio.google.com/apikey))

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/talentscout.git
   cd talentscout
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser** — Navigate to `http://localhost:8501`

---

## Usage Guide

1. **Start** — The assistant greets you and begins the screening
2. **Provide Information** — Answer each question one at a time (name, email, phone, etc.)
3. **Declare Tech Stack** — List the languages, frameworks, and tools you know
4. **Answer Questions** — Respond to the generated technical questions
5. **Finish** — The session ends with a summary and next-steps info

### Tips
- You can type "bye", "exit", or "quit" at any time to end the session
- The sidebar shows your screening progress and collected information
- If you make a mistake, the assistant will gently ask for correction

---

## Technical Details

### Libraries & Tools

| Library | Version | Purpose |
|---------|---------|---------|
| `streamlit` | ≥1.30.0 | Frontend UI framework |
| `google-generativeai` | ≥0.5.0 | Gemini API SDK |
| `python-dotenv` | ≥1.0.0 | Environment variable management |

### Model: Gemini 2.0 Flash

**Why Gemini?**
- **Free tier** — No API costs for development and demo
- **Speed** — Flash variant optimized for low-latency responses
- **Quality** — Excellent instruction-following and context retention
- **Multilingual** — Native support for 100+ languages (bonus feature)

**Configuration:**
- Temperature: `0.7` (balanced creativity/consistency for conversations)
- Max tokens: `2048` (sufficient for detailed technical questions)
- Analytical tasks (sentiment, language): Temperature `0.3` for precision

### Design Patterns

- **State Machine** — `ConversationManager` drives the conversation through ordered phases
- **Template Method** — Phase-specific prompts injected into a consistent prompt structure
- **Strategy Pattern** — Validation rules differ per phase via `_extract_and_validate()`
- **Session State** — Streamlit's `st.session_state` for conversation persistence across rerenders

---

## Prompt Design

### Philosophy

Prompts are crafted with three principles:
1. **Specificity** — Each phase has a tailored prompt that tells the LLM exactly what to do
2. **Constraint** — Clear rules prevent the LLM from going off-topic or revealing system details
3. **Context** — Phase context is injected alongside user input so the LLM understands the current state

### System Prompt

The system prompt defines "Scout's" persona, rules, and behavioral constraints:
- Professional yet warm personality
- Strict topic adherence (hiring/screening only)
- One-field-at-a-time information gathering
- Input validation with gentle correction
- No code generation or tutoring — assessment only

### Phase Prompts

Each conversation phase has a dedicated prompt that:
- Tells the LLM what the candidate just provided
- Specifies what to validate
- Defines what to ask next
- Handles edge cases (invalid input, off-topic responses)

### Technical Question Generation

The tech question prompt dynamically adjusts based on:
- **Tech stack** — Questions cover the specific technologies listed
- **Experience level** — Difficulty scales with years of experience
- **Breadth** — Questions cover debugging, architecture, best practices, and trade-offs

### Fallback Prompt

When input doesn't match the expected phase:
- Acknowledges the candidate's message politely
- Redirects to the current screening step
- Never dismisses or ignores the candidate

---

## Data Privacy & GDPR

- **Local Storage** — All data stored locally in `data/candidates/` as JSON files
- **Anonymization** — Email and phone are masked in stored data (original kept for recruiter access)
- **Right to Erasure** — `delete_candidate_session(session_id)` function available
- **No External Transmission** — Data never leaves the local system (except API calls to Gemini for response generation)
- **Gitignored** — The `data/candidates/` directory is excluded from version control
- **Minimal Collection** — Only essential screening information is gathered

---

## Bonus Features

### 🧠 Sentiment Analysis
- Each candidate message is analyzed for emotional tone
- Categories: Positive, Neutral, Negative, Frustrated, Excited, Confused
- Displayed as a color-coded badge in the sidebar
- Logged in session data for recruiter insight

### 🌍 Multilingual Support
- Auto-detects the candidate's language from their messages
- Supports 20+ languages including Hindi, Spanish, French, German, and more
- When non-English is detected, responses include bilingual translations
- Language detection runs on early messages to minimize API calls

### 🎨 Premium UI
- Custom dark theme with Inter font
- Glassmorphism effects and gradient accents
- Smooth message slide-in animations
- Progress bar with gradient fill
- Responsive chat bubble design
- Custom scrollbar styling

---

## Challenges & Solutions

### 1. Maintaining Context Across Phases
**Challenge:** The LLM needed to understand which phase the conversation was in without confusing past context.
**Solution:** Phase-specific context is injected into each prompt call, then stripped from the stored history to keep it clean. The LLM sees `[SYSTEM CONTEXT — phase: X]` directives that are replaced with the user's actual message in the stored history.

### 2. Preventing Off-Topic Responses
**Challenge:** LLMs naturally want to be helpful with any question, even off-topic ones.
**Solution:** The system prompt includes strict rules about topic adherence, and the fallback mechanism provides a polite redirect template that the LLM follows consistently.

### 3. Input Validation Without Being Annoying
**Challenge:** Validating email/phone formats while keeping the conversation natural.
**Solution:** Two-layer validation — regex-based extraction in code, plus LLM-level validation prompts that ask for corrections conversationally rather than showing error messages.

### 4. Exit Keyword False Positives
**Challenge:** Phrases like "thank you for asking" would trigger exit detection.
**Solution:** Exit detection only triggers on short messages (≤5 words) containing exit keywords, preventing false positives from longer contextual sentences.

### 5. Technical Question Quality
**Challenge:** Generating questions that are neither too easy nor too hard.
**Solution:** The prompt includes the candidate's experience level and explicitly requests intermediate-to-advanced questions covering practical aspects (debugging, architecture, trade-offs), not just theoretical knowledge.

---

## Project Structure

```
talentscout/
├── app.py                      # Streamlit entry point
├── config.py                   # API keys, constants, model configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
│
├── core/                       # Core business logic
│   ├── __init__.py
│   ├── conversation.py         # Conversation state machine
│   ├── prompts.py              # All prompt templates
│   ├── llm.py                  # Gemini API wrapper
│   └── data_store.py           # JSON data persistence
│
├── modules/                    # Bonus feature modules
│   ├── __init__.py
│   ├── sentiment.py            # Sentiment analysis
│   └── language.py             # Language detection & bilingual support
│
├── ui/                         # UI layer
│   ├── __init__.py
│   ├── components.py           # Reusable Streamlit components
│   └── styles.py               # Custom CSS injection
│
├── data/
│   └── candidates/             # Stored session data (gitignored)
│
└── assets/
    └── logo.png                # TalentScout branding
```

---

## License

This project was built as part of an AI/ML internship assignment. All code is original and open for review.

---

<p align="center">
  Built with ❤️ using <a href="https://streamlit.io">Streamlit</a> & <a href="https://ai.google.dev">Google Gemini</a>
</p>
