import sqlite3

def init_db():
    conn = sqlite3.connect("zimafa.db")
    cur = conn.cursor()

    # User table உருவாக்கம்
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )''')

    # Default admin user
    cur.execute("SELECT * FROM users WHERE username=?", ("admin",))
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    ("admin", "admin123", "admin"))

    # Client table உருவாக்கம்
    cur.execute('''CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT,
                    address TEXT
                )''')

    conn.commit()
    conn.close()


def validate_user(username, password):
    conn = sqlite3.connect("zimafa.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user
