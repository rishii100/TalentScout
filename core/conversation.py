"""
Conversation Manager
====================
State machine that drives the TalentScout hiring assistant conversation.
Tracks the current phase, candidate data, and conversation history,
and determines the appropriate prompt to send to the LLM at each step.
"""

import re
from config import PHASES, EXIT_KEYWORDS
from core.llm import generate_response
from core.prompts import (
    SYSTEM_PROMPT,
    GREETING_PROMPT,
    INFO_PROMPTS,
    TECH_QUESTION_PROMPT,
    EVALUATE_ANSWER_PROMPT,
    FAREWELL_PROMPT,
    EXIT_PROMPT,
    FALLBACK_PROMPT,
)


class ConversationManager:
    """
    Manages the state and flow of a candidate screening conversation.

    Attributes
    ----------
    phase : str
        Current phase of the conversation (from config.PHASES).
    candidate : dict
        Collected candidate information.
    history : list[dict]
        Full conversation history in OpenAI-compatible format.
    tech_questions : str
        Generated technical questions (stored for evaluation).
    questions_answered : bool
        Whether the candidate has responded to technical questions.
    ended : bool
        Whether the conversation has been concluded.
    """

    def __init__(self):
        self.phase = "GREETING"
        self.candidate = {
            "name": "",
            "email": "",
            "phone": "",
            "experience": "",
            "position": "",
            "location": "",
            "tech_stack": "",
        }
        self.history: list[dict] = []
        self.tech_questions = ""
        self.questions_answered = False
        self.ended = False

    # ── Public API ────────────────────────────────────────────────────

    def get_greeting(self) -> str:
        """Generate the initial greeting message from the assistant."""
        context_msg = f"[SYSTEM CONTEXT — phase: GREETING]\n{GREETING_PROMPT}"
        self.history.append({"role": "user", "content": context_msg})
        response = generate_response(self.history, SYSTEM_PROMPT)
        # Replace the context message with a clean user placeholder
        self.history[-1] = {"role": "user", "content": "[Session started]"}
        self.history.append({"role": "assistant", "content": response})
        self.phase = "COLLECTING_NAME"
        return response

    def process_message(self, user_input: str) -> str:
        """
        Process a user message and return the assistant's response.

        Handles exit detection, phase transitions, input validation,
        and context-aware prompt construction.
        """
        if self.ended:
            return "This screening session has ended. Please start a new session if you'd like to continue. 😊"

        # Check for exit intent
        if self._is_exit_intent(user_input):
            return self._handle_exit(user_input)

        # Add user message to history
        self.history.append({"role": "user", "content": user_input})

        # Route to the appropriate handler based on current phase
        if self.phase in INFO_PROMPTS:
            response = self._handle_info_phase(user_input)
        elif self.phase == "GENERATING_QUESTIONS":
            response = self._handle_question_generation()
        elif self.phase == "ASKING_QUESTIONS":
            response = self._handle_answer_evaluation(user_input)
        elif self.phase == "FAREWELL":
            response = self._handle_farewell()
        else:
            response = self._handle_fallback(user_input)

        self.history.append({"role": "assistant", "content": response})
        return response

    def get_progress(self) -> float:
        """Return a 0.0–1.0 progress value based on the current phase."""
        if self.phase not in PHASES:
            return 1.0
        idx = PHASES.index(self.phase)
        return idx / (len(PHASES) - 1)

    # ── Private Handlers ──────────────────────────────────────────────

    def _handle_info_phase(self, user_input: str) -> str:
        """Handle information-gathering phases with validation."""
        phase = self.phase
        prompt_injection = INFO_PROMPTS[phase]

        # Extract and validate data based on current phase
        extracted = self._extract_and_validate(phase, user_input)

        if extracted is not None:
            # Store the extracted data
            field_map = {
                "COLLECTING_NAME": "name",
                "COLLECTING_EMAIL": "email",
                "COLLECTING_PHONE": "phone",
                "COLLECTING_EXPERIENCE": "experience",
                "COLLECTING_POSITION": "position",
                "COLLECTING_LOCATION": "location",
                "COLLECTING_TECH_STACK": "tech_stack",
            }
            self.candidate[field_map[phase]] = extracted

            # Advance to next phase
            current_idx = PHASES.index(phase)
            self.phase = PHASES[current_idx + 1]

        # Build the context-enhanced prompt
        context = f"[SYSTEM CONTEXT — phase: {phase}]\n{prompt_injection}\n\nCandidate said: {user_input}"
        # Temporarily replace the last user message with context-enhanced version
        self.history[-1] = {"role": "user", "content": context}
        response = generate_response(self.history, SYSTEM_PROMPT)
        # Restore the clean user message
        self.history[-1] = {"role": "user", "content": user_input}

        # If we just collected tech stack, immediately generate questions
        if self.phase == "GENERATING_QUESTIONS":
            self.phase = "ASKING_QUESTIONS"
            questions_response = self._generate_tech_questions()
            response = response + "\n\n" + questions_response

        return response

    def _generate_tech_questions(self) -> str:
        """Generate technical questions based on the candidate's tech stack."""
        prompt = TECH_QUESTION_PROMPT.format(
            tech_stack=self.candidate["tech_stack"],
            experience=self.candidate["experience"],
            num_questions=5,
        )
        context = f"[SYSTEM CONTEXT — phase: GENERATING_QUESTIONS]\n{prompt}"
        self.history.append({"role": "user", "content": context})
        response = generate_response(self.history, SYSTEM_PROMPT)
        self.history[-1] = {"role": "user", "content": "[Generating technical questions]"}
        self.history.append({"role": "assistant", "content": response})
        self.tech_questions = response
        return response

    def _handle_question_generation(self) -> str:
        """Handle the question generation phase (shouldn't normally be reached directly)."""
        self.phase = "ASKING_QUESTIONS"
        return self._generate_tech_questions()

    def _handle_answer_evaluation(self, user_input: str) -> str:
        """Evaluate the candidate's answers to technical questions."""
        prompt = EVALUATE_ANSWER_PROMPT.format(
            questions=self.tech_questions,
            answer=user_input,
        )
        context = f"[SYSTEM CONTEXT — phase: ASKING_QUESTIONS]\n{prompt}"
        self.history[-1] = {"role": "user", "content": context}
        response = generate_response(self.history, SYSTEM_PROMPT)
        self.history[-1] = {"role": "user", "content": user_input}

        self.questions_answered = True
        self.phase = "FAREWELL"

        # Append farewell
        farewell = self._generate_farewell()
        return response + "\n\n" + farewell

    def _handle_farewell(self) -> str:
        """Handle the farewell phase."""
        return self._generate_farewell()

    def _generate_farewell(self) -> str:
        """Generate the farewell message with candidate summary."""
        prompt = FAREWELL_PROMPT.format(**self.candidate)
        context = f"[SYSTEM CONTEXT — phase: FAREWELL]\n{prompt}"
        self.history.append({"role": "user", "content": context})
        response = generate_response(self.history, SYSTEM_PROMPT)
        self.history[-1] = {"role": "user", "content": "[Session complete]"}
        self.history.append({"role": "assistant", "content": response})
        self.ended = True
        return response

    def _handle_exit(self, user_input: str) -> str:
        """Handle early exit from the conversation."""
        self.history.append({"role": "user", "content": user_input})
        context = f"[SYSTEM CONTEXT — phase: EXIT]\n{EXIT_PROMPT}"
        self.history[-1] = {"role": "user", "content": context}
        response = generate_response(self.history, SYSTEM_PROMPT)
        self.history[-1] = {"role": "user", "content": user_input}
        self.history.append({"role": "assistant", "content": response})
        self.ended = True
        return response

    def _handle_fallback(self, user_input: str) -> str:
        """Handle unexpected inputs with a graceful redirect."""
        prompt = FALLBACK_PROMPT.format(phase=self.phase)
        context = f"[SYSTEM CONTEXT]\n{prompt}\n\nCandidate said: {user_input}"
        self.history[-1] = {"role": "user", "content": context}
        response = generate_response(self.history, SYSTEM_PROMPT)
        self.history[-1] = {"role": "user", "content": user_input}
        return response

    # ── Validation Helpers ────────────────────────────────────────────

    def _extract_and_validate(self, phase: str, user_input: str) -> str | None:
        """
        Extract and validate data from user input based on the current phase.
        Returns the extracted value, or None if validation fails.
        """
        text = user_input.strip()

        if phase == "COLLECTING_NAME":
            # Accept if it has at least 2 alphabetic characters
            if len(text) >= 2 and any(c.isalpha() for c in text):
                return text
            return None

        elif phase == "COLLECTING_EMAIL":
            # Simple email regex
            match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
            return match.group(0) if match else None

        elif phase == "COLLECTING_PHONE":
            # Extract digits; accept if 7-15 digits are present
            digits = re.sub(r'[^\d]', '', text)
            if 7 <= len(digits) <= 15:
                return text
            return None

        elif phase == "COLLECTING_EXPERIENCE":
            # Extract a number from the response
            match = re.search(r'(\d+)', text)
            if match:
                return match.group(1)
            # Also accept text like "fresher", "fresh", "no experience"
            if any(kw in text.lower() for kw in ["fresh", "no experience", "none", "zero", "entry"]):
                return "0"
            return None

        elif phase == "COLLECTING_POSITION":
            if len(text) >= 2:
                return text
            return None

        elif phase == "COLLECTING_LOCATION":
            if len(text) >= 2:
                return text
            return None

        elif phase == "COLLECTING_TECH_STACK":
            # Accept if they mention at least one recognizable tech or have reasonable text
            if len(text) >= 3:
                return text
            return None

        return text if text else None

    def _is_exit_intent(self, user_input: str) -> bool:
        """Check if the user's message indicates they want to end the conversation."""
        lower = user_input.strip().lower()
        # Only trigger on short messages that are clearly exit-intent
        # Don't trigger if it's part of a longer sentence (e.g., "thank you for asking")
        if len(lower.split()) <= 5:
            for keyword in EXIT_KEYWORDS:
                if keyword in lower:
                    return True
        return False
