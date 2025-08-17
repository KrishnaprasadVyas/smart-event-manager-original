import os

def read_events():
    import json
    from events.event import Event
    
    try:
        with open("events.json", "r") as f:
            events_data = json.load(f)
            return [Event(
                e["name"], 
                e["date"], 
                e["time"], 
                e["type"], 
                e.get("location", "")
            ) for e in events_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []



import json

def write_events(events):
    with open("events.json", "w") as f:
        json.dump([event.__dict__ for event in events], f, indent=4)

