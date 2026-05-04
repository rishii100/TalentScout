"""
Groq LLM Wrapper (Llama)
========================
Handles all communication with the Groq API running Llama models.
Provides a clean interface for the conversation manager to generate responses.
"""

from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, GROQ_MODEL_FAST, GROQ_TEMPERATURE, GROQ_MAX_TOKENS

# Singleton client — initialized once
_client: Groq | None = None


def _get_client() -> Groq:
    """Get or create the Groq client (singleton)."""
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def generate_response(
    conversation_history: list[dict],
    system_prompt: str,
) -> str:
    """
    Send a conversation to Groq (Llama) and return the assistant's reply.

    Parameters
    ----------
    conversation_history : list[dict]
        List of {"role": "user"|"assistant", "content": str} messages
        in OpenAI-compatible format.
    system_prompt : str
        The system-level instruction that defines chatbot behaviour.

    Returns
    -------
    str
        The model's text response, or a fallback message on error.
    """
    client = _get_client()

    # Build messages array with system prompt
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=GROQ_TEMPERATURE,
            max_tokens=GROQ_MAX_TOKENS,
        )
        return response.choices[0].message.content
    except Exception as e:
        return (
            "I apologize, but I'm experiencing a temporary issue. "
            "Could you please repeat your last message? "
            f"(Error: {type(e).__name__})"
        )


def generate_single_response(prompt: str, system_prompt: str = "") -> str:
    """
    One-shot generation without conversation history.
    Used for auxiliary tasks like sentiment analysis and language detection.
    Uses the faster/smaller Llama model to save rate-limit quota.

    Parameters
    ----------
    prompt : str
        The user prompt to send.
    system_prompt : str
        Optional system instruction.

    Returns
    -------
    str
        The model's text response.
    """
    client = _get_client()

    messages = [
        {"role": "system", "content": system_prompt or "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL_FAST,  # Use the faster model for auxiliary tasks
            messages=messages,
            temperature=0.3,  # Lower temperature for analytical tasks
            max_tokens=256,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return ""
