from datetime import datetime
import uuid     # universal unique identifier

class Event:
    def __init__(self, name, date, time, type_, location=None, event_id=None):   # ye constructor method h 
        self.id = event_id or str(uuid.uuid4())  # unique ID
        self.name = name   # event ka naam store krega

        # ✅ Normalize date   (Yahaan program validate karta hai ki date sahi format me hai ya nahi.)
        try:
            parsed_date = datetime.strptime(date, "%d-%m-%Y").strftime("%d-%m-%Y")
        except ValueError:
            parsed_date = date  # fallback if wrong
        self.date = parsed_date

        # ✅ Normalize time
        try:
            parsed_time = datetime.strptime(time, "%H:%M").strftime("%H:%M")
        except ValueError:
            try:
                parsed_time = datetime.strptime(time, "%I:%M").strftime("%H:%M")  # 4:00 -> 04:00
            except ValueError:
                parsed_time = time
        self.time = parsed_time

        self.type = type_
        self.location = location or "Not specified"
        self.created_at = datetime.now().strftime("%d-%m-%Y %H:%M")

    def to_dict(self):
        """Convert event object to dictionary (for JSON)."""
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "time": self.time,
            "type": self.type,
            "location": self.location,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data):
        """Rebuild Event object from dictionary."""
        return Event(
            name=data["name"],
            date=data["date"],
            time=data["time"],
            type_=data["type"],
            location=data.get("location"),
            event_id=data["id"]
        )
