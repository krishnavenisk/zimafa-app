import sqlite3

def get_connection():
    return sqlite3.connect("zimafa.db")

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # DON'T DELETE THE TABLE — Remove DROP statement permanently!
    
    # CREATE CLIENT TABLE (only if not exists)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            mobile TEXT,
            email TEXT,
            address TEXT
        )
    """)

    # USER TABLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # DEFAULT USER
    cur.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin')")

    conn.commit()
    conn.close()


def validate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user
