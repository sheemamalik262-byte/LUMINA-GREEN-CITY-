"""
═══════════════ Lumina Green City — Flask Backend (app.py) ═══════════════
NO databases. NO ML/AI libraries. Pure Python + Flask only.
"""

from flask import Flask, request, jsonify, send_from_directory, render_template_string
import json
import os
import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

# ──────────────────────────────────────────────────────────
# DATA STORAGE PATHS
# ──────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
CONTACTS_FILE = os.path.join(DATA_DIR, 'contacts.json')
APPLICATIONS_FILE = os.path.join(DATA_DIR, 'applications.json')

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize JSON files if they don't exist
for fpath in [CONTACTS_FILE, APPLICATIONS_FILE]:
    if not os.path.exists(fpath):
        with open(fpath, 'w') as f:
            json.dump([], f)


# ──────────────────────────────────────────────────────────
# HELPER: Read / Write JSON files
# ──────────────────────────────────────────────────────────
def read_json(filepath):
    """Read a JSON file and return its contents as a list."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def write_json(filepath, data):
    """Write data to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


# ──────────────────────────────────────────────────────────
# MODULE 1: PLOT DATABASE (In-Memory Python Lists/Dicts)
# ──────────────────────────────────────────────────────────
SECTORS = ['Sector A', 'Sector B', 'Sector C']

# Sector multipliers for price calculation
SECTOR_MULTIPLIERS = {
    'Sector A': 1.00,   # Base pricing
    'Sector B': 1.05,   # 5% premium
    'Sector C': 1.10,   # 10% premium
}

# Base prices by size
BASE_PRICES = {
    '5 Marla House':  7000000,
    '10 Marla House': 11500000,
    '1 Kanal House':  24000000,
    '5 Marla Plot':   3500000,
    '10 Marla Plot':  6000000,
    '1 Kanal Plot':   11000000,
}

# Generate the master property list
master_properties = []

for sec in SECTORS:
    sec_letter = sec[-1]   # 'A', 'B', or 'C'
    uid = 1

    # ── 5 Marla Houses (10 per sector) ──
    for i in range(1, 11):
        status = 'Sold' if uid % 4 == 0 else ('Reserved' if uid % 7 == 0 else 'Available')
        price = int((7000000 + uid * 45000) * SECTOR_MULTIPLIERS[sec])
        master_properties.append({
            'id': f'H-{sec_letter}-{str(uid).zfill(3)}',
            'sector': sec,
            'name': '5 Marla House',
            'type': 'House',
            'size': '5 Marla',
            'price': price,
            'status': status,
            'details': '2 Bed · 3 Bath · Drawing/Guest Room',
            'specs': {
                'Bedrooms': '2 Bedrooms',
                'Bathrooms': '3 Bathrooms',
                'Facilities': 'Kitchen, TV Lounge, Car Porch'
            },
            'distances': {
                'mosque': f'{i * 45}m',
                'school': f'{120 + i * 25}m',
                'park': f'{80 + i * 35}m'
            }
        })
        uid += 1

    # ── 10 Marla Houses (10 per sector) ──
    for i in range(1, 11):
        status = 'Sold' if uid % 3 == 0 else ('Reserved' if uid % 8 == 0 else 'Available')
        price = int((11500000 + uid * 65000) * SECTOR_MULTIPLIERS[sec])
        master_properties.append({
            'id': f'H-{sec_letter}-{str(uid).zfill(3)}',
            'sector': sec,
            'name': '10 Marla House',
            'type': 'House',
            'size': '10 Marla',
            'price': price,
            'status': status,
            'details': '4 Bed · 5 Bath · Garden & Balcony',
            'specs': {
                'Bedrooms': '4 Bedrooms',
                'Bathrooms': '5 Attached Baths',
                'Facilities': 'Garden, Balcony, Double Kitchen'
            },
            'distances': {
                'mosque': f'{30 + i * 50}m',
                'school': f'{90 + i * 40}m',
                'park': f'{60 + i * 30}m'
            }
        })
        uid += 1

    # ── 1 Kanal Houses (10 per sector) ──
    for i in range(1, 11):
        status = 'Sold' if uid % 5 == 0 else ('Reserved' if uid % 9 == 0 else 'Available')
        price = int((24000000 + uid * 95000) * SECTOR_MULTIPLIERS[sec])
        master_properties.append({
            'id': f'H-{sec_letter}-{str(uid).zfill(3)}',
            'sector': sec,
            'name': '1 Kanal House',
            'type': 'House',
            'size': '1 Kanal',
            'price': price,
            'status': status,
            'details': '5 Bed · Private Pool · Servant Quarters',
            'specs': {
                'Bedrooms': '5 Grand Bedrooms',
                'Bathrooms': '7 Attached Baths',
                'Luxury': 'Private Pool, Servant Quarters'
            },
            'distances': {
                'mosque': f'{100 + i * 30}m',
                'school': f'{200 + i * 20}m',
                'park': f'{40 + i * 25}m'
            }
        })
        uid += 1

    # ── Residential Plots (10 per sector) ──
    for i in range(1, 11):
        status = 'Sold' if i % 3 == 0 else 'Available'
        if i <= 5:
            sz = '5 Marla'
        elif i <= 8:
            sz = '10 Marla'
        else:
            sz = '1 Kanal'
        bp = BASE_PRICES.get(f'{sz} Plot', 3500000)
        price = int((bp + i * 20000) * SECTOR_MULTIPLIERS[sec])
        master_properties.append({
            'id': f'P-{sec_letter}-{str(i).zfill(3)}',
            'sector': sec,
            'name': f'{sz} Residential Plot',
            'type': 'Plot',
            'size': sz,
            'price': price,
            'status': status,
            'details': 'Ready for possession',
            'specs': {
                'Type': 'Residential Plot',
                'Development': '100% Ready'
            },
            'distances': {
                'mosque': f'{i * 75}m',
                'school': f'{150 + i * 45}m',
                'park': f'{100 + i * 50}m'
            }
        })


# ──────────────────────────────────────────────────────────
# MODULE 2: SMART SEARCH API
# ──────────────────────────────────────────────────────────
@app.route('/api/search', methods=['GET'])
def smart_search():
    """
    Search properties by sector, size, and max budget.
    Query params: sector, size, budget
    Returns only Available properties that match ALL given filters.
    """
    sector = request.args.get('sector', '').strip()
    size = request.args.get('size', '').strip()
    budget = request.args.get('budget', '').strip()

    # Parse budget to integer
    try:
        max_budget = int(budget) if budget else None
    except ValueError:
        max_budget = None

    results = []
    for prop in master_properties:
        # Filter by sector
        if sector and prop['sector'] != sector:
            continue
        # Filter by size (check if size string is in the property name)
        if size and size not in prop['name']:
            continue
        # Filter by budget
        if max_budget is not None and prop['price'] > max_budget:
            continue
        # Only return Available properties
        if prop['status'] != 'Available':
            continue
        results.append(prop)

    return jsonify({'count': len(results), 'results': results})


# ──────────────────────────────────────────────────────────
# MODULE 3: SMART RECOMMENDATION API
# ──────────────────────────────────────────────────────────
@app.route('/api/recommend', methods=['GET'])
def smart_recommend():
    """
    Score and return the top 3 best matching plots based on user input.
    Uses simple math scoring: budget closeness, sector match, size match.
    Query params: sector, size, budget
    """
    sector = request.args.get('sector', '').strip()
    size = request.args.get('size', '').strip()
    budget = request.args.get('budget', '').strip()

    try:
        target_budget = int(budget) if budget else None
    except ValueError:
        target_budget = None

    scored = []
    for prop in master_properties:
        if prop['status'] != 'Available':
            continue

        score = 0

        # Sector match: +30 points
        if sector and prop['sector'] == sector:
            score += 30

        # Size match: +40 points
        if size and size in prop['name']:
            score += 40

        # Budget closeness: up to +30 points
        # The closer the price is to (but under) the budget, the higher the score
        if target_budget is not None:
            if prop['price'] <= target_budget:
                # Percentage of budget used (higher = better match)
                ratio = prop['price'] / target_budget
                score += int(ratio * 30)
            else:
                # Over budget — penalize but don't exclude entirely
                over_ratio = target_budget / prop['price']
                score += int(over_ratio * 10)

        scored.append({'property': prop, 'score': score})

    # Sort by score descending, take top 3
    scored.sort(key=lambda x: x['score'], reverse=True)
    top3 = scored[:3]

    return jsonify({
        'count': len(top3),
        'recommendations': [
            {**item['property'], 'match_score': item['score']}
            for item in top3
        ]
    })


# ──────────────────────────────────────────────────────────
# MODULE 4: PRICE CALCULATOR
# ──────────────────────────────────────────────────────────
@app.route('/api/price', methods=['GET'])
def calculate_price():
    """
    Calculate plot/house price based on size, type, and sector multiplier.
    Query params: size (e.g. '5 Marla'), type (e.g. 'House' or 'Plot'), sector
    """
    size = request.args.get('size', '').strip()
    prop_type = request.args.get('type', 'House').strip()
    sector = request.args.get('sector', 'Sector A').strip()

    key = f'{size} {prop_type}'
    base = BASE_PRICES.get(key, 0)
    multiplier = SECTOR_MULTIPLIERS.get(sector, 1.0)

    if base == 0:
        return jsonify({'error': f'Unknown property type: {key}'}), 400

    calculated_price = int(base * multiplier)

    return jsonify({
        'size': size,
        'type': prop_type,
        'sector': sector,
        'base_price': base,
        'sector_multiplier': multiplier,
        'calculated_price': calculated_price,
        'formatted': f'PKR {calculated_price:,}'
    })


# ──────────────────────────────────────────────────────────
# MODULE 5: CHATBOT API (Keyword-Based)
# ──────────────────────────────────────────────────────────
@app.route('/api/chat', methods=['POST'])
def chatbot():
    """
    Simple keyword-based chatbot.
    Takes user message, splits into words, checks for keywords,
    returns a helpful string response.
    """
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'reply': 'Please send a message.'}), 400

    user_msg = data['message'].strip()
    if not user_msg:
        return jsonify({'reply': 'Please type something so I can help you!'})

    # Normalize to lowercase for keyword matching
    words = user_msg.lower().split()
    msg_lower = user_msg.lower()

    reply = ''

    # ── Greeting ──
    if any(w in words for w in ['hello', 'hi', 'hey', 'assalam', 'salam', 'aoa']):
        reply = ("Hello! Welcome to Lumina Green City 🏡\n"
                 "I'm your property assistant. I can help you with:\n"
                 "• Property prices and availability\n"
                 "• Sector information (A, B, C)\n"
                 "• Plot sizes (5 Marla, 10 Marla, 1 Kanal)\n"
                 "• Facilities & amenities\n"
                 "• Application process\n\n"
                 "What would you like to know?")

    # ── Price / Cost related ──
    elif any(w in words for w in ['price', 'cost', 'rate', 'pricing', 'kitna', 'qeemat']):
        reply = ("📊 Lumina Green City — Price Overview:\n\n"
                 "🏠 Houses:\n"
                 "• 5 Marla House: PKR 7.0M – 7.8M\n"
                 "• 10 Marla House: PKR 11.5M – 13.5M\n"
                 "• 1 Kanal House: PKR 24.0M – 29.5M\n\n"
                 "📐 Residential Plots:\n"
                 "• 5 Marla Plot: PKR 3.5M – 3.9M\n"
                 "• 10 Marla Plot: PKR 6.0M – 6.9M\n"
                 "• 1 Kanal Plot: PKR 11.0M – 12.3M\n\n"
                 "Prices vary by sector. Sector C has the highest premium (+10%).\n"
                 "Use our Smart Search to find properties within your budget!")

    # ── Cheap / Budget ──
    elif any(w in words for w in ['cheapest','cheap', 'budget', 'affordable', 'sasta', 'low']):
        # Find the 3 cheapest available properties
        available = [p for p in master_properties if p['status'] == 'Available']
        available.sort(key=lambda x: x['price'])
        cheapest = available[:3]
        reply = "💰 Most Affordable Options Available:\n\n"
        for p in cheapest:
            reply += f"• {p['name']} in {p['sector']} — PKR {p['price']:,} (ID: {p['id']})\n"
        reply += ("\nThese are residential plots — perfect for investment!\n"
                  "Visit the Apply page to submit your application.")

    # ── Expensive / Luxury ──
    elif any(w in words for w in ['expensive', 'Luxury', 'premium', 'best', 'top', 'mehenga']):
        available = [p for p in master_properties if p['status'] == 'Available']
        available.sort(key=lambda x: x['price'], reverse=True)
        top = available[:3]
        reply = "👑 Premium Luxury Options:\n\n"
        for p in top:
            reply += f"• {p['name']} in {p['sector']} — PKR {p['price']:,} (ID: {p['id']})\n"
        reply += ("\nThese 1 Kanal houses come with private pools, "
                  "servant quarters, and 7 attached baths!")

    # ── Sector A ──
    elif 'sector a' in msg_lower or ('sector' in words and 'a' in words):
        sec_props = [p for p in master_properties if p['sector'] == 'Sector A']
        avail = len([p for p in sec_props if p['status'] == 'Available'])
        reply =  (f"🏘️ Sector A — Block Alpha:\n\n"
                 f"• Total Units: {len(sec_props)}\n"
                 f"• Available: {avail}\n"
                 f"• Property Types: 5 Marla, 10 Marla, 1 Kanal Houses + Residential Plots\n"
                 f"• Facilities: Sector Masjid, School, Park\n")
 
    return jsonify({'reply': reply})


# ──────────────────────────────────────────────────────────
# MODULE 6: FORM HANDLERS (Contact + Apply)
# ──────────────────────────────────────────────────────────
@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Receive Contact Us form data, validate, and save to JSON file."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()

    # Validation
    errors = []
    if not name:
        errors.append('Name is required')
    if not email or '@' not in email:
        errors.append('Valid email is required')
    if not message:
        errors.append('Message is required')

    if errors:
        return jsonify({'error': ', '.join(errors)}), 400

    # Save to file
    contacts = read_json(CONTACTS_FILE)
    contacts.append({
        'name': name,
        'email': email,
        'message': message,
        'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    write_json(CONTACTS_FILE, contacts)

    return jsonify({'success': True, 'message': 'Message sent successfully!'})


@app.route('/api/apply', methods=['POST'])
def submit_application():
    """Receive Apply form data, validate, and save to JSON file."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    name = data.get('name', '').strip()
    cnic = data.get('cnic', '').strip()
    prop_type = data.get('type', '').strip()
    phone = data.get('phone', '').strip()

    # Validation
    errors = []
    if not name:
        errors.append('Name is required')
    if not cnic:
        errors.append('CNIC is required')
    if not prop_type:
        errors.append('Property type is required')
    if not phone:
        errors.append('Phone number is required')

    if errors:
        return jsonify({'error': ', '.join(errors)}), 400

    # Save to file
    applications = read_json(APPLICATIONS_FILE)
    applications.append({
        'name': name,
        'cnic': cnic,
        'type': prop_type,
        'phone': phone,
        'status': 'Pending',
        'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    write_json(APPLICATIONS_FILE, applications)

    return jsonify({
        'success': True,
        'message': 'Application submitted successfully!',
        'status': 'Pending'
    })


@app.route('/api/application-status', methods=['GET'])
def check_application_status():
    """Check application status by CNIC."""
    cnic = request.args.get('cnic', '').strip()
    if not cnic:
        return jsonify({'error': 'CNIC is required'}), 400

    applications = read_json(APPLICATIONS_FILE)
    # Find the most recent application for this CNIC
    found = None
    for app_entry in reversed(applications):
        if app_entry.get('cnic') == cnic:
            found = app_entry
            break

    if found:
        return jsonify({'found': True, 'application': found})
    else:
        return jsonify({'found': False, 'message': 'No application found for this CNIC.'})


# ──────────────────────────────────────────────────────────
# MODULE 7: GET ALL PROPERTIES (for sectors.html)
# ──────────────────────────────────────────────────────────
@app.route('/api/properties', methods=['GET'])
def get_all_properties():
    """Return all properties, optionally filtered by sector."""
    sector = request.args.get('sector', '').strip()
    if sector:
        filtered = [p for p in master_properties if p['sector'] == sector]
        return jsonify({'count': len(filtered), 'properties': filtered})
    return jsonify({'count': len(master_properties), 'properties': master_properties})


# ──────────────────────────────────────────────────────────
# MODULE 8: ADMIN PANEL
# ──────────────────────────────────────────────────────────
ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'


@app.route('/admin')
def admin_panel():
    """Serve the admin panel HTML page."""
    return send_from_directory('.', 'admin.html')


@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Validate admin credentials."""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if username == ADMIN_USER and password == ADMIN_PASS:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401


@app.route('/api/admin/data', methods=['GET'])
def admin_data():
    """Return all contacts and applications for the admin dashboard."""
    # Simple auth check via query param (for demo purposes)
    auth = request.args.get('auth', '')
    if auth != 'admin123':
        return jsonify({'error': 'Unauthorized'}), 401

    contacts = read_json(CONTACTS_FILE)
    applications = read_json(APPLICATIONS_FILE)

    return jsonify({
        'contacts': contacts,
        'applications': applications,
        'stats': {
            'total_contacts': len(contacts),
            'total_applications': len(applications),
            'pending': len([a for a in applications if a.get('status') == 'Pending']),
            'total_properties': len(master_properties),
            'available': len([p for p in master_properties if p['status'] == 'Available']),
        }
    })


# ──────────────────────────────────────────────────────────
# SERVE STATIC FILES (HTML, CSS, JS)
# ──────────────────────────────────────────────────────────
@app.route('/')
def serve_index():
    return send_from_directory('.', 'login.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)


# ──────────────────────────────────────────────────────────
# RUN THE APP
# ──────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  Lumina Green City — Flask Backend")
    print("=" * 60)
    print(f"  Properties loaded: {len(master_properties)}")
    print(f"  Available: {len([p for p in master_properties if p['status'] == 'Available'])}")
    print(f"  Data directory: {DATA_DIR}")
    print("=" * 60)
    print("  Open http://127.0.0.1:5000 in your browser")
    print("  Admin panel: http://127.0.0.1:5000/admin")
    print("=" * 60 + "\n")
    app.run(debug=True, port=5000)
