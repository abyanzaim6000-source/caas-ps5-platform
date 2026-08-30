import sqlite3

def init_db():
    conn = sqlite3.connect("caas.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS console_state (
            id INTEGER PRIMARY KEY CHECK (id = 1), -- only one row ever
            status TEXT NOT NULL DEFAULT 'free',    -- 'free' or 'occupied'
            current_user_id TEXT,
            session_ends_at TIMESTAMP
        )
    """)
    c.execute("INSERT OR IGNORE INTO console_state (id, status) VALUES (1, 'free')")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")