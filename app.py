from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os

app = Flask(__name__)
DB = "inventory.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                unit_price REAL NOT NULL DEFAULT 0.0,
                low_stock_threshold INTEGER NOT NULL DEFAULT 10,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            seed = [
                ("Wireless Mouse", "Electronics", 45, 29.99, 10),
                ("USB-C Hub", "Electronics", 8, 49.99, 15),
                ("Desk Lamp", "Office", 22, 34.99, 5),
                ("Notebook A5", "Stationery", 3, 5.99, 20),
                ("Mechanical Keyboard", "Electronics", 12, 89.99, 8),
                ("Monitor Stand", "Office", 6, 24.99, 5),
                ("Gel Pens (Pack)", "Stationery", 60, 8.49, 15),
                ("Webcam HD", "Electronics", 2, 69.99, 10),
                ("Cable Organizer", "Accessories", 35, 12.99, 10),
                ("Sticky Notes", "Stationery", 4, 3.99, 25),
            ]
            conn.executemany(
                "INSERT INTO products (name, category, quantity, unit_price, low_stock_threshold) VALUES (?,?,?,?,?)",
                seed
            )

@app.route("/")
def index():
    with get_db() as conn:
        products = conn.execute("SELECT * FROM products ORDER BY created_at DESC").fetchall()
        total = len(products)
        low_stock = [p for p in products if p["quantity"] <= p["low_stock_threshold"]]
        total_value = sum(p["quantity"] * p["unit_price"] for p in products)
        categories = list(set(p["category"] for p in products))
    return render_template("index.html", products=products, total=total,
                           low_stock_count=len(low_stock), total_value=total_value,
                           categories=categories, low_stock=low_stock)

@app.route("/add", methods=["POST"])
def add_product():
    name = request.form["name"].strip()
    category = request.form["category"].strip()
    quantity = int(request.form["quantity"])
    unit_price = float(request.form["unit_price"])
    threshold = int(request.form.get("low_stock_threshold", 10))
    with get_db() as conn:
        conn.execute(
            "INSERT INTO products (name, category, quantity, unit_price, low_stock_threshold) VALUES (?,?,?,?,?)",
            (name, category, quantity, unit_price, threshold)
        )
    return redirect(url_for("index"))

@app.route("/edit/<int:pid>", methods=["GET", "POST"])
def edit_product(pid):
    with get_db() as conn:
        if request.method == "POST":
            name = request.form["name"].strip()
            category = request.form["category"].strip()
            quantity = int(request.form["quantity"])
            unit_price = float(request.form["unit_price"])
            threshold = int(request.form.get("low_stock_threshold", 10))
            conn.execute(
                "UPDATE products SET name=?, category=?, quantity=?, unit_price=?, low_stock_threshold=? WHERE id=?",
                (name, category, quantity, unit_price, threshold, pid)
            )
            return redirect(url_for("index"))
        product = conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
    return render_template("edit.html", product=product)

@app.route("/delete/<int:pid>", methods=["POST"])
def delete_product(pid):
    with get_db() as conn:
        conn.execute("DELETE FROM products WHERE id=?", (pid,))
    return redirect(url_for("index"))

@app.route("/api/products")
def api_products():
    with get_db() as conn:
        products = conn.execute("SELECT * FROM products ORDER BY name").fetchall()
    return jsonify([dict(p) for p in products])

@app.route("/api/stats")
def api_stats():
    with get_db() as conn:
        products = conn.execute("SELECT * FROM products").fetchall()
    total_items = sum(p["quantity"] for p in products)
    low_stock = sum(1 for p in products if p["quantity"] <= p["low_stock_threshold"])
    total_value = sum(p["quantity"] * p["unit_price"] for p in products)
    by_category = {}
    for p in products:
        by_category[p["category"]] = by_category.get(p["category"], 0) + p["quantity"]
    return jsonify({
        "total_products": len(products),
        "total_items": total_items,
        "low_stock": low_stock,
        "total_value": round(total_value, 2),
        "by_category": by_category
    })

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
