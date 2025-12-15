import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "inventory.db"

schema = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    qty INTEGER NOT NULL
);
"""

sample_items = [
    ("SKU-001", "Candle - Vanilla", 12.99, 25),
    ("SKU-002", "Candle - Lavender", 12.99, 18),
    ("SKU-003", "Sticker Pack", 4.50, 60),
    ("SKU-004", "Notebook", 9.99, 30),
    ("SKU-005", "Keychain", 6.00, 45),
]

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(schema)

    # Add sample data only if table is empty
    cur.execute("SELECT COUNT(*) FROM items;")
    count = cur.fetchone()[0]
    if count == 0:
        cur.executemany(
            "INSERT INTO items (sku, name, price, qty) VALUES (?, ?, ?, ?)",
            sample_items
        )
        conn.commit()

    conn.close()
    print("Database initialized:", DB_PATH)

if __name__ == "__main__":
    main()