/* ═══════════════ Lumina Green City — script.js ═══════════════ */
/* Rewritten to use Flask API endpoints via fetch() calls       */

// ─── API Base URL ───
const API_BASE = '';  // Same origin — Flask serves everything

// ─── Auth / Welcome ───
const uName = localStorage.getItem('loggedInName');
const welcomeEl = document.getElementById('welcomeName');
if (welcomeEl && uName) welcomeEl.innerText = 'Hi, ' + uName + ' 👋';
if (!localStorage.getItem('loggedInUser')) window.location.href = 'login.html';

function logout() {
  localStorage.removeItem('loggedInUser');
  localStorage.removeItem('loggedInName');
  window.location.href = 'login.html';
}

// ─── Sector Navigation ───
function goSector(s) {
  window.location.href = 'sectors.html?sector=' + s;
}

// ─── CNIC Formatter ───
function fmtC(inp) {
  let v = inp.value.replace(/\D/g, '');
  if (v.length > 5 && v.length <= 12) v = v.slice(0,5) + '-' + v.slice(5);
  else if (v.length > 12) v = v.slice(0,5) + '-' + v.slice(5,12) + '-' + v.slice(12,13);
  inp.value = v;
}

// ──────────────────────────────────────────────────────────
// SMART SEARCH — Calls Flask /api/search endpoint
// ──────────────────────────────────────────────────────────
async function smartSearch() {
  const sectorEl = document.getElementById('u-sector');
  const sizeEl   = document.getElementById('u-size');
  const budgetEl = document.getElementById('u-budget');
  const res      = document.getElementById('u-results');
  if (!sectorEl || !sizeEl || !budgetEl || !res) return;

  const sector = sectorEl.value;
  const size   = sizeEl.value;
  const budget = budgetEl.value;

  // Build query string
  const params = new URLSearchParams();
  if (sector) params.append('sector', sector);
  if (size)   params.append('size', size);
  if (budget) params.append('budget', budget);

  // Show loading state
  res.innerHTML = '<p style="text-align:center;color:var(--muted);margin-top:12px;">Searching...</p>';

  try {
    const response = await fetch(`${API_BASE}/api/search?${params.toString()}`);
    const data = await response.json();

    if (!data.results || data.results.length === 0) {
      res.innerHTML = '<p style="color:#c0392b;margin-top:8px;text-align:center;">No matching units found. Try adjusting your filters.</p>';
      return;
    }

    res.innerHTML = `<p style="font-size:12px;color:var(--muted);margin-bottom:8px;">${data.count} unit(s) found</p>` +
      data.results.map(p =>
        `<div class="result-item">
          <span><strong>#${p.id}</strong> — ${p.sector} | ${p.name}</span>
          <span style="display:flex;align-items:center;gap:6px;">
            <strong style="color:var(--navy)">PKR ${p.price.toLocaleString()}</strong>
            <span class="result-badge">Available</span>
          </span>
        </div>`
      ).join('');
  } catch (err) {
    console.error('Search error:', err);
    res.innerHTML = '<p style="color:#c0392b;margin-top:8px;text-align:center;">Error connecting to server. Make sure Flask is running.</p>';
  }
}

// ──────────────────────────────────────────────────────────
// APPLY FORM — Calls Flask /api/apply endpoint
// ──────────────────────────────────────────────────────────
async function submitApp() {
  const nameEl  = document.getElementById('a-name');
  const cnicEl  = document.getElementById('a-cnic');
  const typeEl  = document.getElementById('a-type');
  const phoneEl = document.getElementById('a-phone');
  const msgEl   = document.getElementById('apply-msg');
  if (!nameEl || !cnicEl || !typeEl || !phoneEl || !msgEl) return;

  const name  = nameEl.value.trim();
  const cnic  = cnicEl.value.trim();
  const type  = typeEl.value;
  const phone = phoneEl.value.trim();

  if (!name || !cnic || !type || !phone) {
    msgEl.style.color = '#c0392b';
    msgEl.innerText = 'Please fill all fields!';
    msgEl.classList.add('show');
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/api/apply`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, cnic, type, phone })
    });
    const data = await response.json();

    if (data.success) {
      // Also save to localStorage for backwards compatibility
      localStorage.setItem('application_' + cnic, JSON.stringify({
        name, cnic, type, phone, status: 'Pending',
        date: new Date().toLocaleDateString()
      }));
      msgEl.style.color = '#27ae60';
      msgEl.innerText = '✓ Application submitted! Status: Pending.';
      msgEl.classList.add('show');
      ['a-name', 'a-cnic', 'a-phone'].forEach(id => {
        const e = document.getElementById(id); if (e) e.value = '';
      });
      if (typeEl) typeEl.value = '';
    } else {
      msgEl.style.color = '#c0392b';
      msgEl.innerText = data.error || 'Submission failed. Please try again.';
      msgEl.classList.add('show');
    }
  } catch (err) {
    console.error('Apply error:', err);
    msgEl.style.color = '#c0392b';
    msgEl.innerText = 'Server error. Make sure Flask is running.';
    msgEl.classList.add('show');
  }
}

// ──────────────────────────────────────────────────────────
// CHECK APPLICATION STATUS — Calls Flask /api/application-status
// ──────────────────────────────────────────────────────────
async function checkStatus() {
  const cnicEl = document.getElementById('st-cnic');
  const res    = document.getElementById('status-result');
  if (!cnicEl || !res) return;

  const cnic = cnicEl.value.trim();
  if (!cnic) {
    res.innerHTML = '<p style="color:#c0392b">Please enter your CNIC.</p>';
    res.classList.add('show');
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/api/application-status?cnic=${encodeURIComponent(cnic)}`);
    const data = await response.json();

    if (data.found) {
      const d = data.application;
      res.innerHTML = `<strong>Name:</strong> ${d.name}<br>
        <strong>CNIC:</strong> ${d.cnic}<br>
        <strong>Property:</strong> ${d.type}<br>
        <strong>Date:</strong> ${d.date}<br>
        <strong>Status:</strong> <span style="color:#e6a817;font-weight:700">${d.status}</span>`;
    } else {
      // Fallback: check localStorage
      const app = localStorage.getItem('application_' + cnic);
      if (app) {
        const d = JSON.parse(app);
        res.innerHTML = `<strong>Name:</strong> ${d.name}<br>
          <strong>CNIC:</strong> ${d.cnic}<br>
          <strong>Property:</strong> ${d.type}<br>
          <strong>Date:</strong> ${d.date}<br>
          <strong>Status:</strong> <span style="color:#e6a817;font-weight:700">${d.status}</span>`;
      } else {
        res.innerHTML = '<p style="color:#c0392b">No application found for this CNIC.</p>';
      }
    }
    res.classList.add('show');
  } catch (err) {
    // Fallback to localStorage if server is down
    const app = localStorage.getItem('application_' + cnic);
    res.innerHTML = app
      ? (() => { const d = JSON.parse(app); return `<strong>Name:</strong> ${d.name}<br><strong>CNIC:</strong> ${d.cnic}<br><strong>Property:</strong> ${d.type}<br><strong>Date:</strong> ${d.date}<br><strong>Status:</strong> <span style="color:#e6a817;font-weight:700">${d.status}</span>`; })()
      : '<p style="color:#c0392b">No application found for this CNIC.</p>';
    res.classList.add('show');
  }
}

// ──────────────────────────────────────────────────────────
// CONTACT FORM — Calls Flask /api/contact endpoint
// ──────────────────────────────────────────────────────────
async function submitContact() {
  const nameEl  = document.getElementById('c-name');
  const emailEl = document.getElementById('c-email');
  const msgEl   = document.getElementById('c-msg');
  if (!nameEl || !emailEl || !msgEl) return;

  const name  = nameEl.value.trim();
  const email = emailEl.value.trim();
  const msg   = msgEl.value.trim();
  if (!name || !email || !msg) { alert('Please fill all fields!'); return; }

  try {
    const response = await fetch(`${API_BASE}/api/contact`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, message: msg })
    });
    const data = await response.json();

    if (data.success) {
      const successEl = document.getElementById('form-success');
      if (successEl) successEl.classList.add('show');
      ['c-name', 'c-email', 'c-msg'].forEach(id => {
        const e = document.getElementById(id); if (e) e.value = '';
      });
    } else {
      alert(data.error || 'Failed to send message. Please try again.');
    }
  } catch (err) {
    console.error('Contact error:', err);
    alert('Server error. Make sure Flask is running.');
  }
}

// ──────────────────────────────────────────────────────────
// FACILITY POPUP CONTROLS (unchanged)
// ──────────────────────────────────────────────────────────
function openFacility(key) {
  const el = document.getElementById('fac-' + key);
  if (el) { el.classList.add('open'); document.body.style.overflow = 'hidden'; }
}
function closeFac(key) {
  const el = document.getElementById('fac-' + key);
  if (el) { el.classList.remove('open'); document.body.style.overflow = ''; }
}
function scrollCards(id, amt) {
  const el = document.getElementById(id);
  if (el) el.scrollBy({ left: amt, behavior: 'smooth' });
}

// ──────────────────────────────────────────────────────────
// ESCAPE KEY TO CLOSE OVERLAYS (unchanged)
// ──────────────────────────────────────────────────────────
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.fac-overlay.open').forEach(el => {
      el.classList.remove('open');
      document.body.style.overflow = '';
    });
  }
});
