import datetime
import hashlib

# ══════════════════════════════════════════════
#  FAKE AUTH DATABASE — Lumina Green City
#  Tables: users_db (registered users)
# ══════════════════════════════════════════════


def _hash(password):
    """Simple password hashing (like a real DB would store)."""
    return hashlib.sha256(password.encode()).hexdigest()


# ── Users Table ─────────────────────────────
#  Fields: id, name, cnic, password, email, registered_date, is_active

users_db = [
    {
        "id": 1,
        "name": "Sheema",
        "cnic": "3550103767554",
        "password": _hash("123456"),
        "email": "sheema@gmail.com",
        "registered_date": "2026-01-15 10:22:00",
        "is_active": True,
    },
    {
        "id": 2,
        "name": "Robin",
        "cnic": "1234567890123",
        "password": _hash("123456"),
        "email": "robin@gmail.com",
        "registered_date": "2026-02-08 14:35:00",
        "is_active": True,
    },
    {
        "id": 3,
        "name": "Ayesha Malik",
        "cnic": "4210112345678",
        "password": _hash("ayesha2026"),
        "email": "ayesha.malik@hotmail.com",
        "registered_date": "2026-03-20 09:10:00",
        "is_active": True,
    },
    {
        "id": 4,
        "name": "Usman Tariq",
        "cnic": "3740567891234",
        "password": _hash("usman@789"),
        "email": "usman.tariq@yahoo.com",
        "registered_date": "2026-04-11 17:55:00",
        "is_active": False,   # banned / inactive account
    },
]


# ══════════════════════════════════════════════
#  HELPER FUNCTIONS
# ══════════════════════════════════════════════

def _next_id():
    return max(u["id"] for u in users_db) + 1


# ── REGISTER ─────────────────────────────────

def register(name, cnic, password, email=""):
    """
    Register a new user.
    Returns (True, user)  on success.
    Returns (False, error_message) if CNIC already exists.
    """
    # Check if CNIC already registered
    if get_user_by_cnic(cnic):
        msg = f"CNIC {cnic} is already registered."
        print(f"[AUTH] Register failed → {msg}")
        return False, msg

    new_user = {
        "id":               _next_id(),
        "name":             name,
        "cnic":             cnic,
        "password":         _hash(password),
        "email":            email,
        "registered_date":  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "is_active":        True,
    }
    users_db.append(new_user)
    print(f"[AUTH] Registered → {name} (ID {new_user['id']})")
    return True, new_user


# ── LOGIN ─────────────────────────────────────

def login(cnic, password):
    """
    Login with CNIC + password.
    Returns (True, user)   on success.
    Returns (False, reason) on failure.
    """
    user = get_user_by_cnic(cnic)

    if not user:
        print(f"[AUTH] Login failed → CNIC {cnic} not found")
        return False, "No account found with this CNIC."

    if not user["is_active"]:
        print(f"[AUTH] Login failed → Account inactive ({user['name']})")
        return False, "Your account has been deactivated."

    if user["password"] != _hash(password):
        print(f"[AUTH] Login failed → Wrong password ({user['name']})")
        return False, "Incorrect password."

    print(f"[AUTH] Login success → Welcome, {user['name']}!")
    return True, user


# ── READ ──────────────────────────────────────

def get_user_by_cnic(cnic):
    for u in users_db:
        if u["cnic"] == cnic:
            return u
    return None


def get_user_by_id(user_id):
    for u in users_db:
        if u["id"] == user_id:
            return u
    return None


def get_all_users():
    return users_db


# ── UPDATE ────────────────────────────────────

def change_password(cnic, old_password, new_password):
    """Change password after verifying the old one."""
    user = get_user_by_cnic(cnic)
    if not user:
        return False, "User not found."
    if user["password"] != _hash(old_password):
        return False, "Old password is incorrect."
    user["password"] = _hash(new_password)
    print(f"[AUTH] Password changed → {user['name']}")
    return True, "Password updated successfully."


def deactivate_account(cnic):
    """Ban / deactivate a user."""
    user = get_user_by_cnic(cnic)
    if user:
        user["is_active"] = False
        print(f"[AUTH] Account deactivated → {user['name']}")
        return True
    return False


# ── DISPLAY ───────────────────────────────────

def print_all_users():
    """Pretty-print the users table."""
    print(f"\n{'ID':<4} {'Name':<15} {'CNIC':<15} {'Email':<30} {'Active':<7} {'Registered'}")
    print("─" * 85)
    for u in users_db:
        print(f"{u['id']:<4} {u['name']:<15} {u['cnic']:<15} {u['email']:<30} {'✅' if u['is_active'] else '❌':<7} {u['registered_date']}")


# ══════════════════════════════════════════════
#  QUICK DEMO  (python database_auth.py)
# ══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 55)
    print("  LUMINA GREEN CITY — Auth Database Demo")
    print("=" * 55)

    # Show all users
    print_all_users()

    # Test: successful login
    print("\n🔐 Login Tests:")
    print("  Sheema  →", login("3550103767554", "123456"))
    print("  Robin   →", login("1234567890123", "123456"))

    # Test: wrong password
    print("  Wrong pw→", login("3550103767554", "wrongpass"))

    # Test: inactive account
    print("  Usman   →", login("3740567891234", "usman@789"))

    # Test: register new user
    print("\n➕ Register new user:")
    register("Fatima Noor", "5550198765432", "fatima2026", "fatima@gmail.com")

    # Test: duplicate CNIC
    print("\n⚠️  Duplicate CNIC test:")
    register("Fake Sheema", "3550103767554", "abc123")

    # Show updated table
    print_all_users()
    print()