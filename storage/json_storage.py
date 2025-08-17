# storage/json_storage.py

import json
import os
from events.event import Event

DATA_FILE = "events.json"

def load_events():
    """Load events from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        return [Event.from_dict(e) for e in data]

def save_events(events):
    """Save list of Event objects to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump([e.to_dict() for e in events], f, indent=4)
