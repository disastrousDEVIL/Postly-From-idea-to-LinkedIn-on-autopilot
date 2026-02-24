import json
import os

STATE_FILE = "state.json"


def load(chat_id: int) -> dict:
    """Load conversation state for a specific Telegram chat."""
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r") as f:
        data = json.load(f)
    return data.get(str(chat_id), {})


def save(chat_id: int, state: dict):
    """Save conversation state for a specific Telegram chat."""
    data = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
    data[str(chat_id)] = state
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)
