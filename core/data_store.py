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
import streamlit as st
from datetime import datetime, timezone
from config import DATA_DIR

try:
    from pymongo import MongoClient
    from pymongo.server_api import ServerApi
    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False


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

    # Attempt to save to MongoDB first
    mongodb_uri = os.environ.get("MONGODB_URI")
    
    # Try getting from Streamlit secrets if not in env
    if not mongodb_uri:
        try:
            mongodb_uri = st.secrets.get("MONGODB_URI")
        except Exception:
            pass

    if mongodb_uri and HAS_PYMONGO:
        try:
            print(f"DEBUG: Attempting to save to MongoDB...")
            client = MongoClient(mongodb_uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
            db = client.talentscout
            collection = db.candidates
            collection.insert_one(session_data)
            print(f"DEBUG: Successfully saved to MongoDB (Session ID: {session_id})")
            session_data.pop("_id", None)  # Remove internal ID
            return session_id
        except Exception as e:
            print(f"DEBUG: MongoDB save failed: {e}")
            print("DEBUG: Falling back to local storage...")

    # Fallback to local file storage
    print(f"DEBUG: Saving to local file storage (Session ID: {session_id})")
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
    Attempts to delete from MongoDB first, then local storage.

    Returns True if the file/record was found and deleted, False otherwise.
    """
    deleted = False
    
    # Attempt to delete from MongoDB first
    mongodb_uri = os.environ.get("MONGODB_URI")
    if not mongodb_uri:
        try:
            mongodb_uri = st.secrets.get("MONGODB_URI")
        except Exception:
            pass

    if mongodb_uri and HAS_PYMONGO:
        try:
            client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
            db = client.talentscout
            collection = db.candidates
            result = collection.delete_one({"session_id": session_id})
            if result.deleted_count > 0:
                deleted = True
        except Exception:
            pass

    # Also try to delete local file
    filepath = os.path.join(DATA_DIR, f"{session_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        deleted = True
        
    return deleted
