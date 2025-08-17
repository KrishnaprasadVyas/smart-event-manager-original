# Smart Event Manager

A lightweight Python CLI app to **create, view, search and manage events**, with **user auth, analytics, and email reminders**.

> Storage is JSON-based (`events.json`, `users.json`). Time & date are normalized, so duplicates like `1:5` and `01:05` are treated the same.

---

## ✨ Features

* 📅 **Manage Events**: Add, edit, delete, and list (Day / Week / Month).
* 🔎 **Search & Filter**: Search by keyword, filter by type.
* 🔐 **Authentication**: Register / Login / Logout (passwords hashed via SHA-256).
* 🧮 **Analytics**: Totals, by-type counts, location stats, top upcoming.
* 📧 **Email Reminders**: Send reminders to attendees loaded from `attendees.xlsx`.
* ✅ **Duplicate Guard**: Prevents duplicate events on the same **name + date + time** (e.g., `1:5` → normalized to `01:05`).

---

## 🗂️ Project Structure

```
smart-event-manager/
├─ config/
│  └─ settings.py
├─ events/
│  ├─ event.py          # Event model (normalizes date/time)
│  ├─ manager.py        # Add/Edit/Delete logic (duplicate checks)
│  └─ views.py          # Day/Week/Month/Search/Filter/Upcoming
├─ storage/
│  └─ json_storage.py   # (if used) load_events/save_events
├─ utils/
│  ├─ analytics.py      # Simple analytics on events.json
│  ├─ auth.py           # Register/Login/Logout (users.json)
│  └─ emailer.py        # SMTP + attendees.xlsx reminders
├─ events.json          # Event data (auto-created)
├─ users.json           # User data (auto-created)
├─ .env                 # SMTP + admin env vars (see below)
├─ requirements.txt
└─ main.py              # CLI entrypoint
```

> Your code currently calls `read_events/write_events` or `load_events/save_events` depending on file. Make sure you consistently import the ones you’re using (recommend: stick to one module, e.g., `storage/json_storage.py` with `load_events/save_events`).

---

## 🚀 Quickstart

1. **Create & activate venv**

```bash
# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Create `.env`**

```env
# SMTP (use real values; App Password recommended for Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_address@gmail.com
SMTP_PASSWORD=your_app_password
FROM_NAME=Smart Event Manager

# Optional admin password if you extend admin logic
ADMIN_PASSWORD=Krishna@22
```

4. **Run the app**

```bash
python main.py
```

---

## 🖥️ CLI Guide (Menus)

```
1. Register
2. Login
3. Logout
4. Add Event          (requires login)
5. Edit Event         (requires login)
6. Delete Event       (requires login)
7. View Day
8. View Week
9. View Month
10. Search Event
11. Filter Events
12. Upcoming Events
13. Send Reminders
14. Analytics Report
15. Exit
```

### Event Fields

* **name**: string
* **date**: `DD-MM-YYYY` (normalized)
* **time**: `HH:MM` 24h (normalized; `1:5` → `01:05`)
* **type**: your category (e.g., `MEETING`, `BIRTHDAY`)
* **location**: optional (defaults to “Not specified”)

### Duplicate Prevention

In `events/manager.py`:

* Inputs are normalized (`01:05`, `22-05-2005`).
* It checks for an **existing event with the same name + date + time**.
* If found → “Duplicate event found! Not adding.”

> Tip: If you want *time-slot* conflicts (regardless of name) to be blocked, also check just `date + time` before adding.

---

## 📧 Email Reminders

* Implemented in `utils/emailer.py`.
* Reads attendees from **Excel** (`attendees.xlsx` by default).

### Expected columns in `attendees.xlsx`

| name | email                                     | event\_id (optional) |
| ---- | ----------------------------------------- | -------------------- |
| Bob  | [bob@example.com](mailto:bob@example.com) | 3d2c...e8            |
| Ana  | [ana@example.com](mailto:ana@example.com) |                      |

* If `event_id` is present → reminder for **that** event only.
* If `event_id` is empty → the attendee gets a reminder for **all** selected events.

### How to send

Choose **13. Send Reminders** in the menu, then:

* Select **hours** (e.g., next 24 hours) or **date** (`DD-MM-YYYY`).
* Provide path to Excel (default is `attendees.xlsx`).
* Choose **dry-run** (prints emails instead of sending) or real send.

> For Gmail, use **App Passwords** (2FA required). Normal account passwords often fail due to security policies.

---

## 📊 Analytics

Menu **14. Analytics Report** prints:

* Total events
* Events by type
* Events by location
* Top 5 upcoming (sorted)

Code: `utils/analytics.py`

---

## 🔐 Authentication

* `utils/auth.py` stores users in `users.json`.
* Passwords are **hashed** using SHA-256.
* `main.py` currently **requires login** before Add/Edit/Delete.

### (Optional) Make Add/Edit/Delete **Admin-only**

If you want a real admin role, one simple option is to treat a fixed list of admin usernames as admins:

```python
# utils/auth.py (add inside the class)
admin_users = {"admin"}  # set any usernames you want as admins

@staticmethod
def is_admin():
    return Auth.logged_in_user in Auth.admin_users
```

Then in `main.py`, change the checks:

```python
elif choice == "4":
    if not Auth.logged_in_user:
        print("⚠️ Please login first!")
    elif not Auth.is_admin():
        print("⛔ Admin only operation.")
    else:
        add_event()
```

(Repeat the same pattern for **Edit** and **Delete**.)

> Alternatively, you can store a `"role": "admin"|"user"` in `users.json` during registration.

---

## 🗃️ Data Files

* **events.json** (auto-created), sample:

```json
[
  {
    "id": "3d2c...e8",
    "name": "Team Sync",
    "date": "22-05-2005",
    "time": "01:05",
    "type": "MEETING",
    "location": "Room 101",
    "created_at": "18-08-2025 01:52"
  }
]
```

* **users.json** (auto-created), sample:

```json
{
  "alice": "4a7d1ed414...<sha256>...",
  "admin": "ef92b778baf...<sha256>..."
}
```

---

## ⚙️ Requirements

`requirements.txt` should contain at least:

```
openpyxl
python-dotenv
```

(If you add anything else, keep this file in sync.)

---

## 🧪 Troubleshooting

* **Duplicate still adds when typing `1:5`**
  Ensure `Event` constructor **normalizes** time to `HH:MM` and `add_event()` compares using normalized values:

  * Normalize input via `datetime.strptime(...).strftime(...)`
  * Compare `name.lower().strip()` + normalized `date/time`.

* **SMTP fails (Gmail)**
  Use **App Password**, not the account password. Confirm `.env` values and port `587` (TLS).

* **File paths**
  Run from project root so `events.json` and `users.json` resolve correctly. If you use `storage/json_storage.py`, prefer absolute paths built with `Path(__file__).resolve().parent.parent`.

---

## 🛣️ Roadmap (ideas)

* Role-based access with persisted `role` in `users.json`
* ICS export / Google Calendar sync
* Better CLI UX (arrow menus) or a minimal TUI/GUI
* Unit tests for manager & views
* CSV import/export

---

## 📝 License

MIT (or your preference).

---

## 🙌 Thanks

Built with love & Python. Enjoy scheduling!
