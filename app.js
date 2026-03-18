const API = 'https://neostrong.pythonanywhere.com';

// ── Check API status ──────────────────────────────────────────────
async function checkStatus() {
  try {
    const res = await fetch(`${API}/`);
    if (res.ok) {
      document.getElementById('statusDot').className = 'status-dot online';
      document.getElementById('statusText').textContent = 'API Online';
    } else {
      throw new Error();
    }
  } catch {
    document.getElementById('statusDot').className = 'status-dot offline';
    document.getElementById('statusText').textContent = 'API Offline';
  }
}

// ── Load locations into dropdown ──────────────────────────────────
async function loadLocations() {
  try {
    const res = await fetch(`${API}/locations`);
    const data = await res.json();
    const select = document.getElementById('location');

    data.locations.forEach(loc => {
      const opt = document.createElement('option');
      opt.value = loc;
      opt.textContent = loc.replace(/\b\w/g, c => c.toUpperCase());
      select.appendChild(opt);
    });
  } catch {
    console.error('Could not load locations. Is the Flask server running?');
  }
}

// ── Predict price ─────────────────────────────────────────────────
async function predict() {
  const location = document.getElementById('location').value;
  const sqft     = parseFloat(document.getElementById('sqft').value);
  const bhk      = parseInt(document.getElementById('bhk').value);
  const bath     = parseInt(document.getElementById('bath').value);

  // Validate inputs
  if (!location)        return showError('Please select a location.');
  if (!sqft || sqft<=0) return showError('Please enter a valid area in sq ft.');
  if (!bhk  || bhk<=0)  return showError('Please enter a valid BHK value.');
  if (!bath || bath<=0) return showError('Please enter a valid number of bathrooms.');

  // Show loading state
  const btn = document.getElementById('predictBtn');
  btn.classList.add('loading');
  btn.textContent = 'Estimating...';
  hideAll();

  try {
    const res = await fetch(`${API}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ location, total_sqft: sqft, bath, bhk })
    });

    const data = await res.json();

    if (!res.ok) {
      showError(data.error || 'Prediction failed. Please try again.');
    } else {
      showResult(data, location, sqft, bhk, bath);
    }

  } catch (err) {
    showError('Cannot connect to API. Make sure your Flask server is running on port 5000.');
  } finally {
    btn.classList.remove('loading');
    btn.textContent = 'Estimate Price';
  }
}

// ── Show result card ──────────────────────────────────────────────
function showResult(data, location, sqft, bhk, bath) {
  hideAll();

  const price = data.predicted_price_lakhs;
  const ppsf  = Math.round((price * 100000) / sqft).toLocaleString();

  document.getElementById('resultLocation').textContent = location.replace(/\b\w/g, c => c.toUpperCase());
  document.getElementById('resultPrice').textContent    = `₹ ${price.toLocaleString()}`;
  document.getElementById('detailSqft').textContent     = `${sqft.toLocaleString()} sq ft`;
  document.getElementById('detailConfig').textContent   = `${bhk} BHK`;
  document.getElementById('detailBath').textContent     = `${bath}`;
  document.getElementById('detailPpsf').textContent     = `₹ ${ppsf}`;

  document.getElementById('resultCard').classList.add('visible');
}

// ── Show error card ───────────────────────────────────────────────
function showError(msg) {
  hideAll();
  document.getElementById('errorMsg').textContent = msg;
  document.getElementById('resultError').classList.add('visible');
}

// ── Hide all result states ────────────────────────────────────────
function hideAll() {
  document.getElementById('emptyState').style.display = 'none';
  document.getElementById('resultCard').classList.remove('visible');
  document.getElementById('resultError').classList.remove('visible');
}

// ── Allow Enter key to trigger prediction ─────────────────────────
document.addEventListener('keydown', e => {
  if (e.key === 'Enter') predict();
});

// ── Initialise on page load ───────────────────────────────────────
checkStatus();
loadLocations();
