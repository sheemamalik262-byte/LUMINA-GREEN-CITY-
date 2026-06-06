import datetime
import json
import os

# ══════════════════════════════════════════════
#  FAKE DATABASE — Lumina Green City
#  Acts like a real database using Python lists.
#  Data is kept in memory while the app runs.
# ══════════════════════════════════════════════


# ── Applications Table ──────────────────────
applications_db = [
    {
        "id": 1,
        "name": "Ali Khan",
        "cnic": "12345-1234567-1",
        "type": "5 Marla House — Sector A",
        "phone": "0300-1234567",
        "status": "Pending",
        "date": "2026-05-30 18:29:18"
    },
    {
        "id": 2,
        "name": "ali",
        "cnic": "34433-3333333-3",
        "type": "10 Marla House — Sector C",
        "phone": "3333333333333333333333333",
        "status": "Pending",
        "date": "2026-05-30 18:35:33"
    },
    {
        "id": 3,
        "name": "sheema",
        "cnic": "12345-6789012-3",
        "type": "10 Marla House — Sector C",
        "phone": "1234567899",
        "status": "Pending",
        "date": "2026-06-01 15:16:20"
    },
    {
        "id": 4,
        "name": "haha",
        "cnic": "12345-6778900-9",
        "type": "1 Kanal House — Sector C",
        "phone": "03017265123",
        "status": "Pending",
        "date": "2026-06-01 21:35:16"
    },
    {
        "id": 5,
        "name": "strawberry pie",
        "cnic": "09887-6543210-9",
        "type": "5 Marla House — Sector A",
        "phone": "0000000000000",
        "status": "Approved",
        "date": "2026-06-02 00:15:05"
    },
    {
        "id": 6,
        "name": "Arooba",
        "cnic": "12345-6789012-3",
        "type": "1 Kanal House — Sector C",
        "phone": "9999999999",
        "status": "Pending",
        "date": "2026-06-02 05:02:11"
    },
]


# ── Contacts Table ──────────────────────────
contacts_db = [
    {
        "id": 1,
        "name": "Test User",
        "email": "test@test.com",
        "message": "This is a test message",
        "date": "2026-05-30 18:29:18"
    },
]



# ══════════════════════════════════════════════
#  HELPER FUNCTIONS  (simulate DB queries)
# ══════════════════════════════════════════════

def _next_id(table):
    """Auto-increment ID like a real DB."""
    return max((row["id"] for row in table), default=0) + 1


# ── CREATE ──────────────────────────────────

def add_application(name, cnic, property_type, phone):
    """Insert a new application (status defaults to Pending)."""
    new_app = {
        "id":     _next_id(applications_db),
        "name":   name,
        "cnic":   cnic,
        "type":   property_type,
        "phone":  phone,
        "status": "Pending",
        "date":   datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    applications_db.append(new_app)
    print(f"[DB] Application added → {name} (ID {new_app['id']})")
    return new_app


def add_contact(name, email, message):
    """Insert a new contact message."""
    new_msg = {
        "id":      _next_id(contacts_db),
        "name":    name,
        "email":   email,
        "message": message,
        "date":    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    contacts_db.append(new_msg)
    print(f"[DB] Contact message added → {name} (ID {new_msg['id']})")
    return new_msg


# ── READ ─────────────────────────────────────

def get_all_applications():
    """Return all applications."""
    return applications_db


def get_application_by_cnic(cnic):
    """Find a single application by CNIC."""
    for app in applications_db:
        if app["cnic"] == cnic:
            return app
    return None


def get_all_contacts():
    """Return all contact messages."""
    return contacts_db


def get_stats():
    """Return dashboard summary stats."""
    return {
        "total_applications": len(applications_db),
        "total_contacts":     len(contacts_db),
        "pending":            sum(1 for a in applications_db if a["status"] == "Pending"),
        "approved":           sum(1 for a in applications_db if a["status"] == "Approved"),
        "rejected":           sum(1 for a in applications_db if a["status"] == "Rejected"),
    }


# ── UPDATE ───────────────────────────────────

def update_status(cnic, new_status):
    """Change the status of an application by CNIC."""
    allowed = ("Pending", "Approved", "Rejected")
    if new_status not in allowed:
        print(f"[DB] ERROR: '{new_status}' is not a valid status. Use: {allowed}")
        return False

    app = get_application_by_cnic(cnic)
    if app:
        old = app["status"]
        app["status"] = new_status
        print(f"[DB] Status updated → {app['name']} : {old} → {new_status}")
        return True

    print(f"[DB] ERROR: No application found with CNIC {cnic}")
    return False


# ── DELETE ───────────────────────────────────

def delete_application(cnic):
    """Remove an application by CNIC."""
    global applications_db
    before = len(applications_db)
    applications_db = [a for a in applications_db if a["cnic"] != cnic]
    removed = before - len(applications_db)
    print(f"[DB] Deleted {removed} application(s) with CNIC {cnic}")
    return removed > 0


# ── EXPORT ───────────────────────────────────

def export_to_json(filepath="applications_export.json"):
    """Save current applications to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(applications_db, f, indent=2, ensure_ascii=False)
    print(f"[DB] Exported {len(applications_db)} applications → {filepath}")


def load_from_json(filepath="applications.json"):
    """Load/replace applications_db from a JSON file."""
    global applications_db
    if not os.path.exists(filepath):
        print(f"[DB] File not found: {filepath}")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Add IDs if missing
    for i, row in enumerate(data, start=1):
        row.setdefault("id", i)
    applications_db = data
    print(f"[DB] Loaded {len(applications_db)} applications from {filepath}")


# ══════════════════════════════════════════════
#  QUICK TEST  (runs only when you run this
#  file directly: python database.py)
# ══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 50)
    print("  LUMINA GREEN CITY — Fake Database Demo")
    print("=" * 50)

    # Show stats
    stats = get_stats()
    print(f"\n📊 Stats:")
    for k, v in stats.items():
        print(f"   {k}: {v}")

    # Add a new application
    print("\n➕ Adding new application...")
    add_application("Zara Ahmed", "11111-2222222-3", "5 Marla House — Sector A", "0321-9999999")

    # Update a status
    print("\n✏️  Updating status...")
    update_status("12345-1234567-1", "Approved")

    # Show all applications
    print(f"\n📋 All Applications ({len(applications_db)} total):")
    for a in applications_db:
        print(f"   [{a['id']}] {a['name']:<16} | {a['cnic']:<18} | {a['status']}")

    # Export to JSON
    print()
    export_to_json("applications_export.json")
    print("\nDone ✅")