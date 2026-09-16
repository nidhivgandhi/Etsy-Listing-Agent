"""
Saves generated listings to a local JSON file. Simple now; swap for SQLite
later if you want querying (e.g. "show me all listings tagged 'walnut'").
"""

import json
from pathlib import Path

HISTORY_FILE = Path(__file__).parent.parent / "listing_history.json"


def save_listing(listing_dict: dict) -> None:
    history = load_history()
    history.append(listing_dict)
    HISTORY_FILE.write_text(json.dumps(history, indent=2))


def load_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []
    return json.loads(HISTORY_FILE.read_text())
