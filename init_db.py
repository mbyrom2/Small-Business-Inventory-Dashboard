import sqlite3

connection = sqlite3.connect('inventory.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sku TEXT NOT NULL,
        quantity INTEGER DEFAULT 0,
        price REAL DEFAULT 0.0
    )
''')

connection.commit()
connection.close()

print("Database initialized.")
