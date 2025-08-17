# main.py
from utils.emailer import (
    read_attendees_from_xlsx,
    send_reminders_for_events
)

from events.manager import add_event, edit_event, delete_event
from events.views import view_day, view_week, view_month, search_event, filter_event, upcoming_events
from storage import read_events, write_events
from utils.auth import Auth
from utils.analytics import Analytics

from datetime import datetime, timedelta


# --------------------------
# Helper function
# --------------------------
def select_upcoming_events(events, within_hours=None, specific_date=None):
    """Filter upcoming events based on hours or specific date"""
    now = datetime.now()
    selected = []

    for ev in events:
        try:
            ev_dt = datetime.strptime(f"{ev.date} {ev.time}", "%d-%m-%Y %H:%M")
        except Exception:
            continue  # agar parsing fail ho jaye to skip

        if within_hours is not None:
            end_time = now + timedelta(hours=within_hours)
            if now <= ev_dt <= end_time:
                selected.append(ev)

        elif specific_date is not None:
            if ev.date == specific_date:
                selected.append(ev)

    return selected


# --------------------------
# Reminder System (CLI)
# --------------------------
def send_reminders_cli():
    print("\n--- Send Reminders ---")
    try:
        all_events = read_events()
    except NameError:
        print("read_events() not found in storage. Make sure it exists.")
        return

    if not all_events:
        print("No events available to send reminders for.")
        return

    mode = input("Send for upcoming hours or a specific date? (type 'hours' or 'date'): ").strip().lower()
    selected = []
    if mode == "hours":
        val = input("Enter hours from now (e.g., 24): ").strip()
        try:
            hours = int(val)
        except ValueError:
            print("Invalid number.")
            return
        selected = select_upcoming_events(all_events, within_hours=hours)

    elif mode == "date":
        date = input("Enter date (DD-MM-YYYY): ").strip()
        try:
            datetime.strptime(date, "%d-%m-%Y")
        except Exception:
            print("Invalid date format.")
            return
        selected = select_upcoming_events(all_events, specific_date=date)

    else:
        print("Invalid option.")
        return

    if not selected:
        print("No events matched your selection.")
        return

    path = input("Path to attendees Excel (default 'attendees.xlsx'): ").strip() or "attendees.xlsx"
    try:
        attendees = read_attendees_from_xlsx(path)
    except Exception as ex:
        print(f"Error loading attendees: {ex}")
        return

    dry = input("Dry-run? (y/n) [y]: ").strip().lower() or "y"
    dry_run = dry.startswith("y")
    print(f"\nFound {len(selected)} event(s); {len(attendees)} attendee rows loaded. Dry-run={dry_run}")
    sent = send_reminders_for_events(selected, attendees, dry_run=dry_run)
    print(f"\nDone. {len(sent)} email entries processed (printed or sent).")


# --------------------------
# Analytics Dashboard
# --------------------------
def show_analytics():
    analytics = Analytics()
    print("\n📊 Event Analytics Report:")
    print("➡ Total Events:", analytics.event_count())
    print("➡ Events by Type:", analytics.events_by_type())
    print("➡ Events by Location:", analytics.location_stats())
    print("➡ Top 5 Upcoming Events:", analytics.upcoming_events())


# --------------------------
# Menu
# --------------------------
def show_menu():
    print("\n===== Smart Event Manager =====")
    print("1. Register")
    print("2. Login")
    print("3. Logout")
    print("4. Add Event")
    print("5. Edit Event")
    print("6. Delete Event")
    print("7. View Day")
    print("8. View Week")
    print("9. View Month")
    print("10. Search Event")
    print("11. Filter Events")
    print("12. Upcoming Events")
    print("13. Send Reminders")
    print("14. Analytics Report")
    print("15. Exit")


# --------------------------
# Main Loop
# --------------------------
def main():
    # (Optional Auth System) 
    # auth = Auth()
    # if not auth.login():
    #     print("Authentication failed. Exiting...")
    #     return

    while True:
        show_menu()
        choice = input("Enter choice: ")

        if choice == "1":  # Register
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(Auth.register(username, password))

        elif choice == "2":  # Login
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(Auth.login(username, password))

        elif choice == "3":  # Logout
            print(Auth.logout())

        elif choice == "4":
            if not Auth.logged_in_user:
                print("⚠️ Please login first!")
            else:
                add_event()

        elif choice == "5":
            if not Auth.logged_in_user:
                print("⚠️ Please login first!")
            else:
                edit_event()

        elif choice == "6":
            if not Auth.logged_in_user:
                print("⚠️ Please login first!")
            else:
                delete_event()

        elif choice == "7":
            view_day()

        elif choice == "8":
            view_week()

        elif choice == "9":
            view_month()

        elif choice == "10":
            search_event()

        elif choice == "11":
            filter_event()

        elif choice == "12":
            upcoming_events()

        elif choice == "13":
            send_reminders_cli()

        elif choice == "14":
            show_analytics()

        elif choice == "15":
            print("Exiting... 👋")
            break

        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
