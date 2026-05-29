# StockPilot — Smart Inventory Management Dashboard

A web-based inventory management system built with Python, Flask, and SQLite. Track products, monitor stock levels, and get instant low-stock alerts through a clean, dark-themed dashboard.

**Tech Stack:** Python · Flask · SQLite · HTML/CSS · Vanilla JS · Git

---

## Features

- **CRUD Operations** — Add, edit, and delete products with a clean modal UI
- **Live Dashboard** — Total products, inventory value, category count at a glance
- **Low Stock Alerts** — Visual warnings when stock drops below threshold
- **Search/Filter** — Instant client-side table filtering
- **REST API** — `/api/products` and `/api/stats` endpoints
- **Seed Data** — 10 sample products pre-loaded on first run

---

## Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/your-username/inventory-dashboard.git
cd inventory-dashboard

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

The SQLite database (`inventory.db`) is created automatically on first run with sample data.

---

## Project Structure

```
inventory-dashboard/
├── app.py                  # Flask app — routes, DB logic
├── requirements.txt
├── .gitignore
├── templates/
│   ├── index.html          # Main dashboard
│   └── edit.html           # Edit product page
└── static/
    ├── css/style.css       # All styling
    └── js/main.js          # Modal, search, nav
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Dashboard UI |
| `/add` | POST | Add new product |
| `/edit/<id>` | GET/POST | Edit product |
| `/delete/<id>` | POST | Delete product |
| `/api/products` | GET | JSON list of all products |
| `/api/stats` | GET | JSON summary stats |

---

*May 2026 — Python \| Flask \| SQLite \| HTML/CSS \| Git*
