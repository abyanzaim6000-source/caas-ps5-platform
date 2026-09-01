import sqlite3

def init_db():
    conn = sqlite3.connect("caas.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS console_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            status TEXT NOT NULL DEFAULT 'free',
            current_user_id TEXT,
            session_ends_at TIMESTAMP
        )
    """)
    c.execute("INSERT OR IGNORE INTO console_state (id, status) VALUES (1, 'free')")

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            contact TEXT PRIMARY KEY,   -- phone or email, acts as the user's unique ID
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_sessions INTEGER DEFAULT 0
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS session_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_contact TEXT NOT NULL,
            started_at TIMESTAMP,
            ended_at TIMESTAMP,
            minutes_booked INTEGER,
            FOREIGN KEY (user_contact) REFERENCES users (contact)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")