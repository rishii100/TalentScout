"""
Multilingual Support Module (Bonus)
====================================
Detects the language of candidate messages and enables
bilingual responses when non-English input is detected.
"""

from core.llm import generate_single_response

_LANG_DETECT_SYSTEM = """You are a language detector. Given a text message, \
identify the primary language it is written in. \
Respond with ONLY the language name in English (e.g., "English", "Hindi", "Spanish", "French"). \
If the text is too short or ambiguous, respond with "English"."""

# Languages we support for bilingual responses
SUPPORTED_LANGUAGES = [
    "Hindi", "Spanish", "French", "German", "Portuguese",
    "Italian", "Dutch", "Japanese", "Chinese", "Korean",
    "Arabic", "Russian", "Turkish", "Bengali", "Tamil",
    "Telugu", "Marathi", "Gujarati", "Kannada", "Malayalam",
]


def detect_language(message: str) -> str:
    """
    Detect the language of a message.

    Parameters
    ----------
    message : str
        The text to analyze.

    Returns
    -------
    str
        The detected language name (e.g., "English", "Hindi").
    """
    if not message or len(message.strip()) < 5:
        return "English"

    prompt = f"What language is this text written in?\n\"{message}\""
    result = generate_single_response(prompt, _LANG_DETECT_SYSTEM).strip()

    # Clean up the response — extract just the language name
    for lang in SUPPORTED_LANGUAGES:
        if lang.lower() in result.lower():
            return lang

    if "english" in result.lower():
        return "English"

    return "English"


def get_bilingual_instruction(language: str) -> str:
    """
    Generate an instruction for the LLM to respond bilingually.

    Parameters
    ----------
    language : str
        The detected non-English language.

    Returns
    -------
    str
        An instruction string to append to the system prompt.
    """
    if language == "English":
        return ""

    return (
        f"\n\nIMPORTANT: The candidate appears to be communicating in {language}. "
        f"Please respond in BOTH English and {language}. "
        f"Write the English version first, then provide the {language} translation "
        f"below it, separated by a line break. Keep both versions concise."
    )
