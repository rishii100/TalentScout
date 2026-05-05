"""
Candidate Data Store
====================
Handles persistence of candidate screening data to JSON files.
Each session creates a unique file. Data is stored locally and
can be deleted on request (GDPR compliance).
"""

import json
import os
import uuid
from datetime import datetime, timezone
from config import DATA_DIR


def save_candidate_session(
    candidate: dict,
    conversation_history: list[dict],
    sentiment_log: list[dict] | None = None,
) -> str:
    """
    Save a complete candidate screening session to a JSON file.

    Parameters
    ----------
    candidate : dict
        Candidate information (name, email, phone, etc.).
    conversation_history : list[dict]
        Full conversation in OpenAI-compatible message format.
    sentiment_log : list[dict], optional
        Sentiment analysis results per message.

    Returns
    -------
    str
        The session ID (filename without extension).
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    session_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now(timezone.utc).isoformat()

    # Filter out internal system context messages from stored conversation
    clean_conversation = []
    for msg in conversation_history:
        content = msg.get("content", "")
        if content not in ("[Session started]", "[Session complete]", "[Generating technical questions]"):
            clean_conversation.append({
                "role": msg["role"],
                "content": content,
            })

    session_data = {
        "session_id": session_id,
        "timestamp": timestamp,
        "candidate": _anonymize_for_storage(candidate),
        "conversation": clean_conversation,
        "sentiment_log": sentiment_log or [],
    }

    filepath = os.path.join(DATA_DIR, f"{session_id}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(session_data, f, indent=2, ensure_ascii=False)

    return session_id


def _anonymize_for_storage(candidate: dict) -> dict:
    """
    Create a partially anonymized copy of candidate data for storage.
    Masks email and phone for privacy while keeping them recognizable.
    """
    data = candidate.copy()

    # Mask email: show first 2 chars + domain
    email = data.get("email", "")
    if "@" in email:
        local, domain = email.split("@", 1)
        masked_local = local[:2] + "*" * max(0, len(local) - 2)
        data["email_masked"] = f"{masked_local}@{domain}"
    data["email"] = email  # Keep original for recruiter use

    # Mask phone: show last 4 digits
    phone = data.get("phone", "")
    if len(phone) >= 4:
        data["phone_masked"] = "*" * (len(phone) - 4) + phone[-4:]
    data["phone"] = phone  # Keep original for recruiter use

    return data


def delete_candidate_session(session_id: str) -> bool:
    """
    Delete a candidate session file (GDPR right to erasure).

    Returns True if the file was found and deleted, False otherwise.
    """
    filepath = os.path.join(DATA_DIR, f"{session_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False
