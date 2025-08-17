import json
from collections import Counter

class Analytics:
    def __init__(self, storage_file="events.json"):
        self.storage_file = storage_file

    def load_events(self):
        try:
            with open(self.storage_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def event_count(self):
        """Total number of events"""
        events = self.load_events()
        return len(events)

    def events_by_type(self):
        """Count events by type"""
        events = self.load_events()
        types = [event["type"] for event in events]
        return dict(Counter(types))

    def upcoming_events(self):
        """List upcoming events"""
        events = self.load_events()
        return sorted(events, key=lambda x: (x["date"], x["time"]))[:5]  # Top 5 upcoming

    def location_stats(self):
        """Count events by location"""
        events = self.load_events()
        locations = [event.get("location", "Not specified") for event in events]
        return dict(Counter(locations))
