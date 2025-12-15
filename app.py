from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "dev-secret-key"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "inventory.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/inventory")
def inventory():
    conn = get_db_connection()
    items = conn.execute("SELECT * FROM items ORDER BY sku").fetchall()
    conn.close()
    return render_template("inventory.html", items=items)


@app.route("/add", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        sku = request.form.get("sku")
        name = request.form.get("name")
        price = request.form.get("price")
        qty = request.form.get("qty")

        if not sku or not name or not price or not qty:
            flash("All fields are required.")
            return redirect(url_for("add_item"))

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO items (sku, name, price, qty) VALUES (?, ?, ?, ?)",
                (sku, name, float(price), int(qty)),
            )
            conn.commit()
            flash("Item added successfully!")
        except sqlite3.IntegrityError:
            flash("SKU already exists.")
        finally:
            conn.close()

        return redirect(url_for("inventory"))

    return render_template("add_item.html")


if __name__ == "__main__":
    app.run(debug=True)