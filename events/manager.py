from datetime import datetime
from storage import read_events, write_events
from events.event import Event

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def validate_time(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def add_event():
    events = read_events()

    name = input("Enter event name: ").strip()
    date = input("Enter date (DD-MM-YYYY): ").strip()
    if not validate_date(date):
        print("❌ Invalid date format!")
        return

    time = input("Enter time (HH:MM): ").strip()
    if not validate_time(time):
        print("❌ Invalid time format!")
        return

    time = datetime.strptime(time, "%H:%M").strftime("%H:%M")
    date = datetime.strptime(date, "%d-%m-%Y").strftime("%d-%m-%Y")
    type_ = input("Enter event type: ").strip()
    location = input("Enter location (optional): ").strip() or "Not specified"

    # 🟢 Normalize date & time (convert to datetime objects for comparison)
    new_dt = datetime.strptime(f"{date} {time}", "%d-%m-%Y %H:%M")

    for e in events:
        existing_dt = datetime.strptime(f"{e.date} {e.time}", "%d-%m-%Y %H:%M")

        if e.name.lower().strip() == name.lower() and existing_dt == new_dt:
            print("⚠️ Duplicate event found! Not adding.")
            return

    # Create new event
    new_event = Event(name, date, time, type_, location)
    events.append(new_event)
    write_events(events)
    print("✅ Event added successfully!")



def edit_event():
    events = read_events()
    if not events:
        print("❌ No events to edit.")
        return

    target = input("Enter Event ID or Name to edit: ")
    found = None
    for e in events:
        if e.id == target or e.name.lower() == target.lower():
            found = e
            break

    if not found:
        print("❌ Event not found.")
        return

    print(f"Editing {found.name} ({found.date} {found.time})")
    new_name = input(f"New name (leave blank to keep {found.name}): ") or found.name
    new_date = input(f"New date (DD-MM-YYYY, blank to keep {found.date}): ") or found.date
    if new_date != found.date and not validate_date(new_date):
        print("❌ Invalid date format!")
        return

    new_time = input(f"New time (HH:MM, blank to keep {found.time}): ") or found.time
    if new_time != found.time and not validate_time(new_time):
        print("❌ Invalid time format!")
        return

    new_type = input(f"New type (blank to keep {found.type}): ") or found.type
    new_location = input(f"New location (blank to keep {found.location}): ") or found.location

    # Update fields
    found.name = new_name
    found.date = new_date
    found.time = new_time
    found.type = new_type
    found.location = new_location

    write_events(events)
    print("✅ Event updated successfully!")

def delete_event():
    events = read_events()
    if not events:
        print("❌ No events to delete.")
        return

    target = input("Enter Event ID or Name to delete: ")
    new_events = [e for e in events if not (e.id == target or e.name.lower() == target.lower())]

    if len(new_events) == len(events):
        print("❌ Event not found.")
    else:
        write_events(new_events)
        print("✅ Event deleted successfully!")
