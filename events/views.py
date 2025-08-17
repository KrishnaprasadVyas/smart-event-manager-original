# events/views.py

from datetime import datetime, timedelta
from storage import read_events

def list_events(events):
    """Helper: Print events in a nice format."""
    if not events:
        print("❌ No events found.")
        return

    for e in events:
        print(f"""
🆔 {e.id}
📌 {e.name}
📅 {e.date} ⏰ {e.time}
🏷️ {e.type} | 📍 {e.location}
Created: {e.created_at}
-----------------------
""")

def view_day():
    events = read_events()
    target_date = input("Enter date to view (DD-MM-YYYY): ")

    day_events = [e for e in events if e.date == target_date]
    print(f"\n📅 Events on {target_date}:")
    list_events(day_events)

def view_week():
    events = read_events()
    start_date = input("Enter week start date (DD-MM-YYYY): ")
    try:
        start_dt = datetime.strptime(start_date, "%d-%m-%Y")
    except ValueError:
        print("❌ Invalid date format!")
        return

    end_dt = start_dt + timedelta(days=6)

    week_events = [
        e for e in events
        if start_dt <= datetime.strptime(e.date, "%d-%m-%Y") <= end_dt
    ]
    print(f"\n📅 Events from {start_date} to {end_dt.strftime('%d-%m-%Y')}:")
    list_events(week_events)

def view_month():
    events = read_events()
    month = input("Enter month (MM): ")
    year = input("Enter year (YYYY): ")

    month_events = [
        e for e in events
        if e.date.split("-")[1] == month and e.date.split("-")[2] == year
    ]
    print(f"\n📅 Events in {month}/{year}:")
    list_events(month_events)

def search_event():
    events = read_events()
    keyword = input("Enter keyword to search: ").lower()

    results = [e for e in events if keyword in e.name.lower() or keyword in e.type.lower()]
    print(f"\n🔍 Search results for '{keyword}':")
    list_events(results)

def filter_event():
    events = read_events()
    type_filter = input("Enter event type to filter (e.g., birthday, meeting): ").lower()

    results = [e for e in events if e.type.lower() == type_filter]
    print(f"\n🔍 Filter results for type '{type_filter}':")
    list_events(results)

def sort_events(events):
    """Sort events by date and time."""
    try:
        return sorted(
            events,
            key=lambda e: datetime.strptime(f"{e.date} {e.time}", "%d-%m-%Y %H:%M")
        )
    except Exception as ex:
        print(f"⚠️ Sorting error: {ex}")
        return events

def upcoming_events(limit=5):
    events = read_events()
    if not events:
        print("❌ No events available.")
        return

    events = sort_events(events)

    print(f"\n⏳ Next {limit} Upcoming Events:")
    for e in events[:limit]:
        print(f"📅 {e.date} ⏰ {e.time} | {e.name} ({e.type})")

